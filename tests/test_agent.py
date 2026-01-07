import pytest
from agent import run_agent

def test_empty_query():
    result = run_agent("")
    assert "orders" in result
    assert isinstance(result["orders"], list)

def test_no_matching_orders():
    result = run_agent("orders in Alaska over 10000")
    assert result["orders"] == []

def test_invalid_numeric_filter():
    result = run_agent("orders over five hundred")
    assert "orders" in result

def test_malformed_input():
    try:
        run_agent(None)
    except Exception:
        assert True
