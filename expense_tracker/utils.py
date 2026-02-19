from __future__ import annotations

from datetime import datetime

DATE_FMT = "%Y-%m-%d"

def prompt(text: str) -> str:
    return input(text).strip()

def ask_nonempty(text: str) -> str:
    while True:
        s = prompt(text)
        if s:
            return s
        print("Please enter a non-empty value.")

def ask_date(text: str) -> str:
    while True:
        s = prompt(text + f" (format {DATE_FMT}): ")
        try:
            datetime.strptime(s, DATE_FMT)
            return s
        except ValueError:
            print("Invalid date. Example: 2026-01-15")

def ask_choice(text: str, choices: list[str]) -> str:
    choices_lc = [c.lower() for c in choices]
    while True:
        s = prompt(text + f" ({'/'.join(choices)}): ").lower()
        if s in choices_lc:
            return s
        print(f"Invalid choice. Choose one of: {', '.join(choices)}")

def ask_positive_float(text: str) -> float:
    while True:
        s = prompt(text + " (positive number): ")
        try:
            x = float(s)
            if x > 0:
                return x
            print("Amount must be > 0.")
        except ValueError:
            print("Invalid number. Example: 12.50")

def ask_optional(text: str) -> str:
    return prompt(text)

def fmt_money(x: float) -> str:
    return f"{x:,.2f}"
