# Expense Manager API

Simple CRUD API with FastAPI. No database. Just a Python dictionary.

## How to run

pip install -r requirements.txt

uvicorn core.main:app --reload

## API Endpoints

| Method | URL | What it does |
|--------|-----|---------------|
| POST | /expenses | Add new expense |
| GET | /expenses | Show all expenses |
| GET | /expenses/1 | Show expense number 1 |
| PUT | /expenses/1 | Edit expense number 1 |
| DELETE | /expenses/1 | Delete expense number 1 |
| GET | /summary | Show total and average |

## Author

Mister Blockchain