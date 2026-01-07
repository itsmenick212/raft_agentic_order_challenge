import logging
from agent import run_agent

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print("AI Order Parser — Raft Challenge")
    query = input("Enter your query: ")
    result = run_agent(query)
    print("\nRESULT JSON:")
    print(result)
