# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from typing import List
import os

NEON_DATABASE_URL = "postgresql://neondb_owner:npg_MV1GnBLW7EQX@ep-restless-mud-adje84ce-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
engine = create_engine(NEON_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Allow React frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/kpis/{rep_id}")
def get_kpis(rep_id: int, month: str = "2026-03-01", db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            SUM(target_amount) as total_target_revenue,
            SUM(actual_amount) as total_actual_revenue,
            SUM(target_qty) as total_target_qty,
            SUM(actual_qty) as total_actual_qty
        FROM monthly_targets
        WHERE rep_id = :rep_id AND month_year = :month
    """)
    result = db.execute(query, {"rep_id": rep_id, "month": month}).fetchone()
    
    return {
        "targetRevenue": float(result[0] or 0),
        "actualRevenue": float(result[1] or 0),
        "targetQty": float(result[2] or 0),
        "actualQty": float(result[3] or 0)
    }

@app.get("/api/products/{rep_id}")
def get_products(rep_id: int, month: str = "2026-03-01", db: Session = Depends(get_db)):
    query = text("""
        SELECT model_name, target_qty, actual_qty, target_amount, actual_amount
        FROM monthly_targets
        WHERE rep_id = :rep_id AND month_year = :month
        ORDER BY actual_amount DESC
    """)
    results = db.execute(query, {"rep_id": rep_id, "month": month}).fetchall()
    
    return [
        {
            "model": r[0],
            "targetQty": r[1],
            "actualQty": r[2],
            "targetAmount": float(r[3]),
            "actualAmount": float(r[4])
        } for r in results
    ]