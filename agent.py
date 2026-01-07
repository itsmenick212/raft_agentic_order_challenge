import json
import logging
import re
from typing import Dict, List, Any

from utils import fetch_orders
from parser import parse_orders
from predictor import train_state_regression

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AgentError(Exception):
    """Explicit agent failure."""
    pass


def _fallback_parse_orders(raw_orders: List[str]) -> List[Dict[str, Any]]:
    """
    Deterministic, regex-based fallback parser.
    Used ONLY if LLM output is invalid or malformed.

    This guarantees the system remains functional even when
    the probabilistic component fails.
    """
    orders = []

    pattern = re.compile(
        r"Order\s+(?P<orderId>\d+):\s+Buyer=(?P<buyer>[^,]+),\s+"
        r"Location=[^,]+,\s+(?P<state>[A-Z]{2}),\s+Total=\$(?P<total>[\d.]+)"
    )

    for text in raw_orders:
        match = pattern.search(text)
        if not match:
            continue

        orders.append({
            "orderId": match.group("orderId"),
            "buyer": match.group("buyer"),
            "state": match.group("state"),
            "total": float(match.group("total")),
        })

    return orders


def _validate_orders(orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Validates normalized orders to ensure schema correctness.
    Fails loudly if required fields are missing or malformed.
    """
    validated = []

    for o in orders:
        try:
            order = {
                "orderId": str(o["orderId"]),
                "buyer": str(o["buyer"]),
                "state": str(o["state"]).upper(),
                "total": float(o["total"]),
            }
            validated.append(order)
        except (KeyError, ValueError, TypeError) as e:
            logger.error("Invalid order schema: %s | error=%s", o, e)
            raise AgentError("Schema validation failed")

    return validated


def _apply_filters(
    orders: List[Dict[str, Any]],
    query: str,
) -> List[Dict[str, Any]]:
    """
    Applies deterministic filtering based on simple intent extraction.
    This is intentionally conservative and explicit.
    """
    if not query:
        return orders

    q = query.lower()
    filtered = []

    # very simple intent signals (deliberate)
    state_filter = None
    min_total = None

    if "ohio" in q:
        state_filter = "OH"
    elif "texas" in q:
        state_filter = "TX"
    elif "washington" in q:
        state_filter = "WA"

    if "over" in q:
        for token in q.split():
            try:
                min_total = float(token)
                break
            except ValueError:
                continue

    for o in orders:
        if state_filter and o["state"] != state_filter:
            continue
        if min_total is not None and o["total"] <= min_total:
            continue
        filtered.append(o)

    return filtered


def run_agent(natural_language_query: str) -> Dict[str, Any]:
    """
    Entry point for the agent.

    Steps:
      1. Fetch raw orders from customer API
      2. Normalize messy text via constrained LLM
      3. Validate schema deterministically
      4. Apply explicit filtering logic
      5. Produce structured JSON output

    The LLM is an optimization, not a single point of failure.
    """

    logger.info("Agent started with query: %s", natural_language_query)

    # Step 1: Fetch raw data
    raw_orders = fetch_orders(limit=50)
    if not raw_orders:
        logger.warning("No orders returned from API")
        return {"orders": []}

    logger.debug("Raw orders: %s", raw_orders)

    # Step 2: Normalize with LLM
    normalized_json = parse_orders(raw_orders)

    try:
        parsed_orders = json.loads(normalized_json)
    except json.JSONDecodeError as e:
        logger.error("LLM returned invalid JSON, falling back: %s", e)
        parsed_orders = _fallback_parse_orders(raw_orders)

    # Step 3: Schema validation
    validated_orders = _validate_orders(parsed_orders)

    # Step 4: Deterministic filtering
    filtered_orders = _apply_filters(validated_orders, natural_language_query)

    # Step 5: Optional analytics (explainable, deterministic)
    state_model = train_state_regression(validated_orders)

    result = {
        "orders": filtered_orders,
        "predicted_average_by_state": state_model,
    }

    logger.info(
        "Agent completed | total=%d | returned=%d",
        len(validated_orders),
        len(filtered_orders),
    )

    return result
