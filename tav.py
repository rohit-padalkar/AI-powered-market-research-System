import os
from functools import lru_cache

from flask import Flask, jsonify, render_template, request
from tavily import TavilyClient


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


app = Flask(__name__, template_folder="templates", static_folder="static")


@app.get("/")
def index():
    """Serve the single-page UI."""
    return render_template("index.html")


@app.post("/api/search")
def search():
    """
    Proxy endpoint that forwards search requests to Tavily and returns JSON that
    the frontend can render. All validation happens here to keep the client
    light-weight and to avoid exposing the API key.
    """
    payload = request.get_json(force=True, silent=True) or {}
    query = (payload.get("query") or "").strip()
    search_depth = payload.get("searchDepth", "advanced")
    include_answer = payload.get("includeAnswer", "advanced")
    include_images = bool(payload.get("includeImages", False))

    if not query:
        return jsonify({"success": False, "error": "Query cannot be empty."}), 400

    try:
        client = get_tavily_client()
        response = client.search(
            query=query,
            search_depth=search_depth,
            include_answer=include_answer,
            include_images=include_images,
        )
        return jsonify({"success": True, "data": response})
    except Exception as exc:  # pragma: no cover - passthrough for manual runs
        return (
            jsonify(
                {
                    "success": False,
                    "error": f"Search failed: {exc}",
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)