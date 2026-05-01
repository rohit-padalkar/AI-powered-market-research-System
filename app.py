import os
from typing import Any, Dict

from flask import Flask, jsonify, render_template, request
from serpapi import GoogleSearch

app = Flask(__name__)


def run_serpapi_search(query: str, location: str, start: int) -> Dict[str, Any]:
    # API key is set permanently
    api_key = "0142b19667b167a550fe1a5d7d895f2c51db912a102cbb8b1cd6797c4915472a"

    params = {
        "engine": "google",
        "q": query,
        "location": location or "Seattle-Tacoma, WA, Washington, United States",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "start": start,
        "safe": "active",
        "api_key": api_key,
    }

    search = GoogleSearch(params)
    return search.get_dict()


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/search")
def search():
    data = request.get_json(force=True, silent=True) or {}
    query = (data.get("query") or "").strip()
    location = (data.get("location") or "").strip()
    start = max(int(data.get("start") or 0), 0)

    if not query:
        return jsonify({"error": "Query is required."}), 400

    try:
        results = run_serpapi_search(query, location, start)
        organic = results.get("organic_results", [])
        return jsonify(
            {
                "query_time": results.get("search_metadata", {}).get("total_time_taken"),
                "results": organic,
            }
        )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)

