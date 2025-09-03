from cachetools import TTLCache
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import engine  # adjust import as needed

# Cache with maxsize 100 and TTL (expiration) of 600 seconds (10 minutes)
cache = TTLCache(maxsize=100, ttl=600)

# result = session.execute(text("EXEC get_credit_card_sp")).fetchall()

def get_credit_card(force_refresh=False):
    if force_refresh or "credit_card" not in cache:
        with Session(engine) as session:
            result = session.execute(text("SELECT \"Id\", \"CardNumber\" FROM credit_card WHERE \"Active\" = true")).fetchall()
            cache["credit_card"] = result
    return cache["credit_card"]

def get_category(force_refresh=False):
    if force_refresh or "category" not in cache:
        with Session(engine) as session:
            result = session.execute(text("SELECT \"Id\", \"Name\" FROM category")).fetchall()
            cache["category"] = result
    return cache["category"]

def get_type(force_refresh=False):
    if force_refresh or "type" not in cache:
        with Session(engine) as session:
            result = session.execute(text("SELECT \"Id\", \"Name\" FROM type")).fetchall()
            cache["type"] = result
    return cache["type"]

def load_cache():
    get_credit_card()
    get_category()
    get_type()
    # print(f"Cached credit_card: {cache['credit_card']}")