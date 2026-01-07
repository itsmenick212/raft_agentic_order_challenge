from flask import Flask, request, jsonify
from agent import run_agent
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/query", methods=["POST"])
def query_orders():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' field"}), 400

    try:
        result = run_agent(data["query"])
        return jsonify(result)
    except Exception as e:
        logging.exception("Agent failure")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
