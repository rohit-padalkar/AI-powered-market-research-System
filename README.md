
# 🔍 Unified Search API (Flask + SerpApi + Tavily)

A lightweight Flask application that provides a **single API endpoint** to perform web searches using either **SerpApi (Google Search)** or **Tavily AI Search**.

---

## 🚀 Features

* 🔗 **Unified API Endpoint**
  Switch between search engines (`serpapi` or `tavily`) using a single route.

* 🌐 **Google Search via SerpApi**
  Fetch real-time search results with metadata.

* 🤖 **AI-Powered Search via Tavily**
  Get enriched answers with advanced search capabilities.

* ⚡ **Fast & Simple Flask Backend**
  Minimal setup with clean architecture.

* 🔐 **Environment-Based API Keys**
  Secure handling of API credentials.

---

## 🏗️ Project Structure

```bash
.
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── (CSS/JS files)
├── README.md
```

---

## ⚙️ Requirements

* Python 3.8+
* Flask
* SerpApi
* Tavily

### Install dependencies

```bash
pip install flask google-search-results tavily-python
```

---

## 🔑 API Key Setup

### 1. SerpApi Key

Replace in code (or better: move to env variable):

```python
SERPAPI_KEY = "your_serpapi_key"
```

Get key from: [https://serpapi.com](https://serpapi.com)

---

### 2. Tavily API Key

Set as environment variable:

```bash
export TAVILY_API_KEY="your_tavily_key"
```

> ⚠️ The app includes a fallback demo key, but **do not use it in production**.

---

## 🚀 Running the App

```bash
python app.py
```

App will run on:

```
http://localhost:5000
```

---

## 📡 API Usage

### Endpoint

```
POST /api/search
```

---

### Request Body

```json
{
  "engine": "serpapi",   // or "tavily"
  "query": "latest AI trends"
}
```

---

### 🔎 SerpApi Response

```json
{
  "success": true,
  "engine": "serpapi",
  "query_time": 0.45,
  "results": [
    {
      "title": "...",
      "link": "...",
      "snippet": "..."
    }
  ]
}
```

---

### 🤖 Tavily Response

```json
{
  "success": true,
  "engine": "tavily",
  "data": {
    "answer": "...",
    "results": [...]
  }
}
```

---

## 🧠 How It Works

1. Client sends query + engine type
2. Flask route `/api/search` processes request
3. Based on engine:

   * **SerpApi** → Google search results
   * **Tavily** → AI-enhanced search
4. Returns structured JSON response

---

## 🔧 Configuration

### Default Engine

```python
engine = payload.get("engine", "serpapi")
```

---

### Tavily Client Caching

```python
@lru_cache(maxsize=1)
```

* Ensures only one Tavily client instance is created
* Improves performance

---

## ⚠️ Important Notes

* Do **NOT** hardcode API keys in production
* Use `.env` or environment variables
* Debug mode is enabled (`debug=True`) — disable in production

---

## 📌 Example Use Cases

* AI-powered search apps
* Meta search engines
* Research assistants
* Chatbot integrations
* Developer tools for search aggregation

---

## 🧑‍💻 Author

Built using Flask with integration of SerpApi and Tavily for flexible search capabilities.

---

If you want, I can also:

* 🔥 Add a **frontend UI README section**
* 💼 Make this **resume/project description**
* ⭐ Add **GitHub badges + deployment steps (Render/Vercel/Docker)**
