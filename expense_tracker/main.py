from __future__ import annotations

from pathlib import Path

from .utils import (
    ask_choice,
    ask_date,
    ask_nonempty,
    ask_positive_float,
    ask_optional,
    fmt_money,
    prompt,
)
from .logic import add_transaction, make_tx, filter_transactions
from .reports import totals, expense_by_category
from .storage import load_csv, save_csv

DATA_PATH = Path(__file__).resolve().parent / "data" / "ledger.csv"

#
def print_tx(tx: dict, i: int | None = None) -> None:
    prefix = f"{i:>3}. " if i is not None else ""
    note = tx.get("note", "")
    note_part = f" | {note}" if note else ""
    print(
        f"{prefix}{tx.get('date',''):<10} | {tx.get('type',''):<7} | "
        f"{tx.get('category',''):<12} | {fmt_money(float(tx.get('amount',0.0))):>12}{note_part}"
    )

def menu() -> str:
    print("\n=== Expense Tracker (CLI) ===")
    print("1) Add transaction")
    print("2) List transactions")
    print("3) Summary report")
    print("4) Save and quit")
    return prompt("Choose an option (1-4): ")

def add_flow(ledger: list[dict]) -> None:
    date = ask_date("Date")
    tx_type = ask_choice("Type", ["income", "expense"])
    category = ask_nonempty("Category: ")
    amount = ask_positive_float("Amount")
    note = ask_optional("Note (optional): ")
    add_transaction(ledger, make_tx(date, tx_type, category, amount, note))
    print("Added.")

def list_flow(ledger: list[dict]) -> None:
    if not ledger:
        print("No transactions yet.")
        return
    f_type = prompt("Filter type (income/expense or blank): ").lower() or None
    if f_type not in (None, "income", "expense"):
        print("Invalid type filter; ignoring.")
        f_type = None
    f_cat = prompt("Filter category (exact match or blank): ") or None
    rows = filter_transactions(ledger, tx_type=f_type, category=f_cat)
    if not rows:
        print("No transactions match your filters.")
        return
    print("\ndate       | type    | category     |       amount | note")
    print("-" * 66)
    for idx, tx in enumerate(rows, 1):
        print_tx(tx, idx)

def report_flow(ledger: list[dict]) -> None:
    if not ledger:
        print("No transactions yet.")
        return
    t = totals(ledger)
    print("\n--- Summary ---")
    print(f"Total income  : {fmt_money(t['income'])}")
    print(f"Total expenses: {fmt_money(t['expenses'])}")
    print(f"Balance       : {fmt_money(t['balance'])}")
    print("\n--- Expenses by category ---")
    per_cat = expense_by_category(ledger)
    if not per_cat:
        print("(no expenses recorded)")
        return
    for cat, amt in per_cat.items():
        print(f"{cat:<20} {fmt_money(amt):>12}")

def main() -> None:
    ledger = load_csv(DATA_PATH)
    if ledger:
        print(f"Loaded {len(ledger)} transactions from disk.")
    else:
        print("No saved ledger found (starting new).")

    while True:
        choice = menu()
        if choice == "1":
            add_flow(ledger)
        elif choice == "2":
            list_flow(ledger)
        elif choice == "3":
            report_flow(ledger)
        elif choice == "4":
            save_csv(DATA_PATH, ledger)
            print(f"Saved {len(ledger)} transactions to {DATA_PATH}. Bye!")
            break
        else:
            print("Invalid option. Please choose 1-4.")

if __name__ == "__main__":
    main()
