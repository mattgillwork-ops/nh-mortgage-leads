# NH Mortgage Lead Engine (Standalone)

This is an independent, sovereign lead generation system for the New Hampshire mortgage market. It is designed to run externally on any server with Python or Docker.

## 🏛️ Infrastructure
- **API**: FastAPI (Uvicorn)
- **Database**: Local SQLite (`db/mortgage_leads.db`)
- **Container**: Docker Support (see `Dockerfile`)
- **Frontend**: Premium Multi-Step Funnel (Vanilla JS/CSS)

## 🧠 Intelligence (The Model)
The system is built to integrate with its own local LLM (via Ollama) or a cloud model for lead nurturing and automated follow-up. 
- Lead scoring logic is encapsulated in `api/lead_manager.py`.

## 🚀 Independent Deployment
1.  **Clone this repo** (Separate from Anti-Gravity).
2.  **Install Dependencies**: `pip install -r requirements.txt`
3.  **Run with Docker**: 
    ```bash
    docker build -t nh-mortgage-leads .
    docker run -p 8001:8001 nh-mortgage-leads
    ```
4.  **Run Manually**:
    ```bash
    python api/server.py
    ```

## 📋 Lead Management
- Access the funnel at `index.html`.
- Export leads to CSV via the `http://localhost:8001/export` endpoint.

---
*Standalone Sovereignty Initialized.*
