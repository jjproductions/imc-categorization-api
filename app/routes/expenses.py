from fastapi import APIRouter, UploadFile, BackgroundTasks
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Expense
from app.schema import ExpensesSP
import pandas as pd
import httpx
import asyncio


router = APIRouter(
    prefix="/expenses",
    tags=['Expenses']
)


active_connections = []

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

# Upload expenses via csv for categorization and saving to DB
@router.post("/", response_model=dict[str, str], summary="Upload the expenses")
async def upload_expenses(file: UploadFile, background_tasks: BackgroundTasks):
    df = pd.read_csv(file.file)
    background_tasks.add_task(process_expenses, df)
    return {"message": "Upload received. Processing in background."}

@router.get("/", response_model=list[ExpensesSP], summary="Get all expenses")
def get_expenses():
    db: Session = SessionLocal()
    result = db.execute(text("SELECT * FROM get_all_statements()"))
    rows = result.mappings().all()  # <-- returns list of dict-like objects
    db.close()
    expenses = [ExpensesSP(**row) for row in rows]
    return expenses
    