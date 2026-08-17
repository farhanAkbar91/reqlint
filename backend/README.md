# ReqLint Backend API Workspace

Welcome, **Backend Engineer**! This folder contains the FastAPI backend REST API server integrated with PostgreSQL and Redis.

## Quickstart

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Local Dev Server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. **Interactive Swagger API Docs**:
   Open browser at: `http://localhost:8000/docs`

4. **Run Backend API Tests**:
   ```bash
   pytest tests/
   ```
