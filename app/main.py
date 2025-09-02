from fastapi import FastAPI, UploadFile, WebSocket, WebSocketDisconnect, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Expense
import pandas as pd
import httpx
import asyncio

app = FastAPI()
active_connections = []

@app.websocket("/ws/progress")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def send_progress(message: str):
    for connection in active_connections:
        await connection.send_text(message)

async def get_category(description: str) -> str:
    prompt = f'Categorize the following expense: "{description}"\nCategory:'
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:11434/api/generate", json={
                "model": "codellama:instruct",
                "prompt": prompt,
                "stream": False
            })
            return response.json().get('response', '').strip() or "Uncategorized"
    except Exception:
        return "Uncategorized"

async def process_expenses(df: pd.DataFrame):
    db: Session = SessionLocal()
    for i, row in df.iterrows():
        category = await get_category(row['Description'])
        await send_progress(f"[{i+1}/{len(df)}] {row['Description']} → {category}")
        expense = Expense(description=row['Description'], amount=row['Amount'], category=category)
        db.add(expense)
    db.commit()
    db.close()
    await send_progress("✅ All expenses processed.")

@app.post("/upload-expenses/")
async def upload_expenses(file: UploadFile, background_tasks: BackgroundTasks):
    df = pd.read_csv(file.file)
    background_tasks.add_task(process_expenses, df)
    return {"message": "Upload received. Processing in background."}

@app.get("/expenses")
def get_expenses():
    db: Session = SessionLocal()
    expenses = db.query(Expense).all()
    db.close()
    return [
        {
            "description": e.description,
            "amount": e.amount,
            "category": e.category
        } for e in expenses
    ]
