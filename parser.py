import logging
from llm_client import get_llm
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
You are a data normalization system.

You will be given messy, unstructured order text.
Each line represents exactly one order.

Your task:
- Parse each line into a JSON object
- Follow the schema exactly
- Do NOT add extra fields
- Do NOT explain your reasoning
- Output ONLY valid JSON (no markdown, no prose)

Schema:
[
  {
    "orderId": "string",
    "buyer": "string",
    "state": "string",
    "total": number
  }
]

Input text:
<<<RAW_ORDERS>>>
"""

def parse_orders(raw_orders):
    llm = get_llm()

    if not raw_orders:
        return "[]"

    raw_text = "\n".join(raw_orders)
    prompt = PROMPT_TEMPLATE.replace("<<<RAW_ORDERS>>>", raw_text)

    messages = [HumanMessage(content=prompt)]

    try:
        response = llm.invoke(messages)
        return response.content.strip()
    except Exception:
        logger.exception("LLM normalization failed")
        raise
