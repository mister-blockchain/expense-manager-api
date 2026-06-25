from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Path, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from .database import Base, engine, get_db
from .models import Expense
from .schemas import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    SummaryResponse,
    DeleteResponse,
    UpdateResponse
)


# ==========================================
# Startup / Shutdown
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up...")
    Base.metadata.create_all(bind=engine)
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title="Expense Manager API",
    description="CRUD API with SQLAlchemy + SQLite",
    version="3.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# GET /
# ==========================================
@app.get("/")
def root(db: Session = Depends(get_db)):
    count = db.query(func.count(Expense.id)).scalar()
    return {
        "message": "Welcome to Expense Manager API v3",
        "total_expenses": count,
        "docs": "/docs"
    }


# ==========================================
# POST /expenses
# ==========================================
@app.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(
        description=expense.description,
        amount=expense.amount
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


# ==========================================
# GET /expenses
# ==========================================
@app.get("/expenses", response_model=List[ExpenseResponse])
def get_all_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).order_by(Expense.id.desc()).all()


# ==========================================
# GET /expenses/{expense_id}
# ==========================================
@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail=f"Expense {expense_id} not found")
    return expense


# ==========================================
# PUT /expenses/{expense_id}
# ==========================================
@app.put("/expenses/{expense_id}", response_model=UpdateResponse)
def update_expense(
    expense_id: int = Path(..., ge=1),
    expense_data: ExpenseUpdate = ...,
    db: Session = Depends(get_db)
):
    expense = db.query(Expense).filter(Expense.id == expense_id).one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail=f"Expense {expense_id} not found")

    expense.description = expense_data.description
    expense.amount = expense_data.amount
    db.commit()
    db.refresh(expense)

    return {"message": f"Expense {expense_id} updated", "expense": expense}


# ==========================================
# DELETE /expenses/{expense_id}
# ==========================================
@app.delete("/expenses/{expense_id}", response_model=DeleteResponse)
def delete_expense(expense_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail=f"Expense {expense_id} not found")

    db.delete(expense)
    db.commit()

    return {"message": f"Expense {expense_id} deleted", "deleted_expense": expense}


# ==========================================
# GET /summary
# ==========================================
@app.get("/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    count = db.query(func.count(Expense.id)).scalar()
    total = db.query(func.sum(Expense.amount)).scalar() or 0.0
    average = round(total / count, 2) if count > 0 else 0.0

    return {
        "total_expenses": count,
        "total_amount": round(total, 2),
        "average_amount": average
    }