# Selenium UI Automation Service (PostgreSQL + Single Worker Queue)

A production-ready asynchronous API built with FastAPI, PostgreSQL, and Selenium. Designed specifically for long-running UI data-entry workflows (10-20 minutes).

## Architecture Highlights
- **Strict Sequential Single-Worker Queue**: Ensures only one Selenium browser instance runs at any given moment to protect server memory and CPU.
- **PostgreSQL Row-Level Locking**: Uses `FOR UPDATE SKIP LOCKED` for atomic FIFO task dispatching.
- **Dual Safe Authentication**: Supports both timing-safe API Key (`X-API-Key`) and HTTP Basic Auth.
- **Categorized Outcomes**: Automatically distinguishes between successful runs (`case_notes`), business rule failures (`BusinessException`), and technical errors (`ApplicationException` with stack traces).

## Quick Start (Docker)
```bash
docker-compose up --build -d
```

## Quick Start (Local)
1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure `.env`:
   ```bash
   cp .env.example .env
   ```
3. Start the service:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## API Usage

### Enqueue Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/run" \
     -H "X-API-Key: prod-secret-api-key-replace-me" \
     -H "Content-Type: application/json" \
     -d '{"account_or_record_id": "REC-9901"}'
```

### Check Queue Overview
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/queue/status" \
     -H "X-API-Key: prod-secret-api-key-replace-me"
```

### Poll Task Status & Outcomes
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/{task_id}" \
     -H "X-API-Key: prod-secret-api-key-replace-me"
```
