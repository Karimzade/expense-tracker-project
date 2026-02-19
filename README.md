# Expense Tracker & Reporting (CLI)

Standard-library-only Python mini project (Unit 6).

## Run
From the folder that contains `expense_tracker/`:

```bash
python -m expense_tracker.main
```

Data is persisted to `expense_tracker/data/ledger.csv`:
- Loads automatically on start (if file exists)
- Saves automatically on quit

## Features (MVP)
- Add transaction (date, type, category, amount, optional note) with robust validation
- List transactions (optional filters by type/category)
- Summary report (income, expenses, balance, expenses per category)
- CSV persistence (no external libraries)
