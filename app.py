import os
from functools import lru_cache
from typing import Any, Dict

from flask import Flask, jsonify, render_template, request
from serpapi import GoogleSearch
from tavily import TavilyClient

app = Flask(__name__, template_folder="templates", static_folder="static")


# SerpApi Configuration
SERPAPI_KEY = "0142b19667b167a550fe1a5d7d895f2c51db912a102cbb8b1cd6797c4915472a"


# Tavily Configuration
@lru_cache(maxsize=1)
def get_tavily_client() -> TavilyClient:
    """
    Lazily instantiate the Tavily client so the API key is read once and shared
    across the app. Falls back to the demo key from the original script, but
    prefers the environment variable for safety.
    """
    api_key = os.environ.get(
        "TAVILY_API_KEY", "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"
    )
    if not api_key:
        raise RuntimeError(
            "TAVILY_API_KEY is not set and no fallback key is available."
        )
    return TavilyClient(api_key)


def run_serpapi_search(query: str) -> Dict[str, Any]:
    """
    Execute a Google search via the SerpApi client.
    
    Args:
        query: Search phrase
    
    Returns:
        Full response dictionary from SerpApi
    """
    params = {
        "engine": "google",
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "safe": "active",
        "api_key": SERPAPI_KEY,
    }

    search = GoogleSearch(params)
    return search.get_dict()


@app.get("/")
def index():
    """Serve the unified single-page UI."""
    return render_template("index.html")


@app.post("/api/search")
def search():
    """
    Unified search endpoint that handles both SerpApi and Tavily searches.
    The engine type is determined by the 'engine' parameter in the request.
    """
    payload = request.get_json(force=True, silent=True) or {}
    engine = payload.get("engine", "serpapi").lower()
    query = (payload.get("query") or "").strip()

    if not query:
        return jsonify({"success": False, "error": "Query cannot be empty."}), 400

    try:
        if engine == "tavily":
            # Tavily search
            client = get_tavily_client()
            response = client.search(
                query=query,
                search_depth="advanced",
                include_answer=True,
                include_images=False,
            )
            return jsonify({
                "success": True,
                "engine": "tavily",
                "data": response
            })

        else:
            # SerpApi search (default)
            results = run_serpapi_search(query)
            organic = results.get("organic_results", [])
            query_time = results.get("search_metadata", {}).get("total_time_taken")

            return jsonify({
                "success": True,
                "engine": "serpapi",
                "query_time": query_time,
                "results": organic
            })

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": f"Search failed: {str(exc)}"
        }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)

