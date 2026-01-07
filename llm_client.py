import os
import logging
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not set in environment")

def get_llm():
    """
    Deterministic OpenRouter-backed *chat* LLM.

    IMPORTANT:
    - OpenRouter models are chat-only
    - Must use ChatOpenAI (not OpenAI)
    """

    return ChatOpenAI(
        model="openai/gpt-oss-120b:exacto",
        temperature=0.0,
        max_tokens=512,
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": "https://teamraft.com",
            "X-Title": "Raft AI Engineer Coding Challenge",
        },
    )
