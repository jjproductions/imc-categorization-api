# FastAPI Expense Categorization

This project uses FastAPI to upload expense CSVs, categorize them using an LLM, and store results in a database. Progress is sent to clients via WebSocket.

## Features
- Upload CSV of expenses
- Categorize expenses using LLM (Ollama/codellama)
- Store expenses in PostgreSQL via SQLAlchemy
- Real-time progress updates via WebSocket

## Setup
1. Install dependencies:
   ```sh
   pip install fastapi uvicorn httpx pandas sqlalchemy psycopg2 websockets
   ```
2. Start Ollama server with codellama model.
3. Run FastAPI app:
   ```sh
   uvicorn main:app --reload
   ```

## Endpoints
- `POST /upload-expenses/` — Upload CSV file
- `GET /expenses` — List categorized expenses
- `WS /ws/progress` — WebSocket for progress updates

## Project Structure
- `main.py` — FastAPI app
- `models.py` — SQLAlchemy models
- `database.py` — DB session setup

---
Replace placeholder DB config and model details as needed for your environment.
