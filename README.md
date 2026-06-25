# Expense Manager API

Full-stack CRUD application for managing expenses. Built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **Vanilla JavaScript**.

---

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Pydantic validation with custom validators
- ✅ Alembic migrations
- ✅ Financial summary (total, average)
- ✅ Dark-themed frontend
- ✅ CORS enabled
- ✅ Swagger auto-docs

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python) |
| Database | SQLite + SQLAlchemy |
| Validation | Pydantic v2 |
| Migrations | Alembic |
| Frontend | HTML5 + CSS3 + Vanilla JS |

---

## Project Structure
## Project Structure

| File/Folder | Description |
|-------------|-------------|
| `core/main.py` | FastAPI application and routes |
| `core/models.py` | SQLAlchemy database models |
| `core/schemas.py` | Pydantic validation schemas |
| `core/database.py` | Database connection and session |
| `frontend/index.html` | Frontend user interface |
| `docs/database-schema.drawio` | Database diagram |
| `alembic/` | Database migration files |
| `alembic.ini` | Alembic configuration |
| `requirements.txt` | Python dependencies |
---

## Installation

```bash
git clone https://github.com/mister-blockchain/expense-manager-api.git
cd expense-manager-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn core.main:app --reload

---



