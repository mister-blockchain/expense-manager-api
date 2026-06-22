from fastapi import FastAPI, HTTPException, status

app = FastAPI(
    title="Expense Manager API",
    description="In-memory CRUD API for managing expenses",
    version="1.0.0"
)

# ==========================================
# In-memory storage (replaces a database)
# Key: expense_id (int), Value: expense dict
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
        "message": "Welcome to Expense Manager API",
        "total_expenses": len(expenses_db),
        "docs": "/docs"
    }


# ==========================================
# 2. POST /expenses — Create a new expense
# ==========================================
@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(description: str, amount: float):
    """
    Create a new expense.
    
    - **description**: What was the expense for? (e.g., "Groceries")
    - **amount**: How much did it cost? (e.g., 25.99)
    """
    global next_id

    new_expense = {
        "id": next_id,
        "description": description,
        "amount": amount
    }

    expenses_db[next_id] = new_expense
    next_id += 1

    return new_expense


# ==========================================
# 3. GET /expenses — Get all expenses
# ==========================================
@app.get("/expenses")
def get_all_expenses():
    """Return all expenses in the system"""
    return {
        "count": len(expenses_db),
        "expenses": list(expenses_db.values())
    }


# ==========================================
# 4. GET /expenses/{expense_id} — Get a single expense
# ==========================================
@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    """Return a single expense by its ID"""
    return find_or_404(expense_id)


# ==========================================
# 5. PUT /expenses/{expense_id} — Update an expense
# ==========================================
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, description: str, amount: float):
    """
    Fully update an existing expense.
    
    - **description**: New description
    - **amount**: New amount
    """
    find_or_404(expense_id)  # Ensure it exists first

    expenses_db[expense_id] = {
        "id": expense_id,
        "description": description,
        "amount": amount
    }

    return {
        "message": f"Expense {expense_id} updated successfully",
        "expense": expenses_db[expense_id]
    }


# ==========================================
# 6. DELETE /expenses/{expense_id} — Delete an expense
# ==========================================
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    """Delete an expense by its ID"""
    find_or_404(expense_id)  # Ensure it exists first
    deleted_expense = expenses_db.pop(expense_id)

    return {
        "message": f"Expense {expense_id} deleted successfully",
        "deleted_expense": deleted_expense
    }


# ==========================================
# 7. GET /summary — Financial summary
# ==========================================
@app.get("/summary")
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