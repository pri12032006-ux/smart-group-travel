# MEMBER 1: STORAGE
# Handles the CSV file: creating it and reading expenses from it.

import csv
import os

# Always use the CSV that sits next to this script
FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.csv")
HEADERS = ["Payer", "Amount", "Category", "Description"]


def create_file():
    """Ensure the expenses CSV exists with proper headers."""
    if not os.path.isfile(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            csv.writer(file).writerow(HEADERS)


def read_expenses():
    """Read all valid expense rows (Amount converted to float)."""
    create_file()
    expenses = []

    with open(FILE_NAME, "r", newline="") as file:
        for row in csv.DictReader(file):
            try:
                row["Amount"] = float(row["Amount"])
                expenses.append(row)
            except (ValueError, KeyError, TypeError):
                continue  # skip malformed rows

    return expenses


def append_expense(payer, amount, category, description):
    """Append one expense row to the CSV."""
    create_file()
    with open(FILE_NAME, "a", newline="") as file:
        csv.writer(file).writerow([payer, amount, category, description])
