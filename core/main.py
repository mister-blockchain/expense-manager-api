from fastapi import FastAPI, HTTPException, status, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import re

# Import our schemas
from .schemas import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    SummaryResponse,
    DeleteResponse,
    UpdateResponse
)

app = FastAPI(
    title="Expense Manager API",
    description="CRUD API for managing expenses with Pydantic validation",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# In-memory storage
# ==========================================
expenses_db: dict[int, dict] = {}
next_id: int = 1


# ==========================================
# Helper function
# ==========================================
def find_or_404(expense_id: int) -> dict:
    """Find an expense by ID or raise 404"""
    if expense_id not in expenses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )
    return expenses_db[expense_id]


# ==========================================
# 1. GET / — Root endpoint
# ==========================================
@app.get("/")
def root():
    """Welcome message and total expenses count"""
    return {
        "message": "Welcome to Expense Manager API v2",
        "total_expenses": len(expenses_db),
        "docs": "/docs"
    }


# ==========================================
# 2. POST /expenses — Create a new expense
# ==========================================
@app.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_expense(expense: ExpenseCreate):  # ← JSON body
    """
    Create a new expense with Pydantic validation.
    
    - **description**: Must be 2-100 chars, at least one letter
    - **amount**: Must be greater than 0, max 1,000,000
    """
    global next_id

    new_expense = {
        "id": next_id,
        "description": expense.description,
        "amount": expense.amount
    }

    expenses_db[next_id] = new_expense
    next_id += 1

    return new_expense


# ==========================================
# 3. GET /expenses — Get all expenses
# ==========================================
@app.get(
    "/expenses",
    response_model=List[ExpenseResponse]
)
def get_all_expenses():
    """Return all expenses in the system"""
    return list(expenses_db.values())


# ==========================================
# 4. GET /expenses/{expense_id} — Get a single expense
# ==========================================
@app.get(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse
)
def get_expense(expense_id: int = Path(..., ge=1)):
    """
    Return a single expense by its ID.
    
    - **expense_id**: Must be 1 or greater
    """
    return find_or_404(expense_id)


# ==========================================
# 5. PUT /expenses/{expense_id} — Update an expense
# ==========================================
@app.put(
    "/expenses/{expense_id}",
    response_model=UpdateResponse
)
def update_expense(
    expense_id: int = Path(..., ge=1),
    expense: ExpenseUpdate = ...
):
    """
    Fully update an existing expense.
    
    - **expense_id**: ID of the expense to update
    - **expense**: New description and amount
    """
    find_or_404(expense_id)

    expenses_db[expense_id] = {
        "id": expense_id,
        "description": expense.description,
        "amount": expense.amount
    }

    return {
        "message": f"Expense {expense_id} updated successfully",
        "expense": expenses_db[expense_id]
    }


# ==========================================
# 6. DELETE /expenses/{expense_id} — Delete an expense
# ==========================================
@app.delete(
    "/expenses/{expense_id}",
    response_model=DeleteResponse
)
def delete_expense(expense_id: int = Path(..., ge=1)):
    """
    Delete an expense by its ID.
    
    - **expense_id**: Must be 1 or greater
    """
    find_or_404(expense_id)
    deleted_expense = expenses_db.pop(expense_id)

    return {
        "message": f"Expense {expense_id} deleted successfully",
        "deleted_expense": deleted_expense
    }


# ==========================================
# 7. GET /summary — Financial summary
# ==========================================
@app.get(
    "/summary",
    response_model=SummaryResponse
)
def get_summary():
    """Return total amount, count, and average of all expenses"""
    count = len(expenses_db)
    total = sum(exp["amount"] for exp in expenses_db.values())
    average = round(total / count, 2) if count > 0 else 0.0

    return {
        "total_expenses": count,
        "total_amount": round(total, 2),
        "average_amount": average
    }