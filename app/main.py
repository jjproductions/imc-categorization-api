from contextlib import asynccontextmanager
import time
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import os
import psycopg
from psycopg.rows import dict_row
from app.utility.cache import load_cache
from .routes import expenses
from . import models
from .database import engine
import logging
from dotenv import load_dotenv
from .config import settings

load_dotenv()

logging.basicConfig(level=logging.ERROR)

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    dbConnectAttempts = 5
    DB_PW = os.getenv("db_iom_password")
    DB_USER = os.getenv("db_iom_user")

    print(f"DB_USER: {DB_USER}, DB_PW: {DB_PW}")

    while dbConnectAttempts > 0:
        try:
            conn = psycopg.connect(host=settings.DB_SERVER, dbname=settings.DB_IOM_DATABASE,
                                user=DB_USER, password=DB_PW, row_factory=dict_row)
            cursor = conn.cursor()
            logging.info("Database connection successful")
            break
        except Exception as error:
            print("Connecting to DB failed")
            print("Error: ", error)
            dbConnectAttempts -= 1
            time.sleep(3)

    load_cache()  # Call your cache loader here
    yield

app = FastAPI(lifespan=lifespan)

#Routes
app.include_router(expenses.router)


class Post(BaseModel):
    name: str
    price: float
    sale: Optional[bool] = False
    inventory: Optional[int] = 0





# active_connections = []

# @app.websocket("/ws/progress")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     active_connections.append(websocket)
#     try:
#         while True:
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         active_connections.remove(websocket)




