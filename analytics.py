# MEMBER 4: ANALYTICS
# Totals, breakdowns, highest category, and the text bar chart.

from storage import read_expenses


def _totals_by(field):
    totals = {}
    for record in read_expenses():
        totals[record[field]] = totals.get(record[field], 0) + record["Amount"]
    return totals


def total_expenses():
    total = sum(r["Amount"] for r in read_expenses())
    print("\n===== TOTAL GROUP EXPENSES =====")
    print(f"Total Expenses: Rs. {total:.2f}")


def category_breakdown():
    totals = _totals_by("Category")
    print("\n===== CATEGORY-WISE EXPENSES =====")

    if not totals:
        print("No expenses available.")
        return

    for category, amount in totals.items():
        print(f"{category}: Rs. {amount:.2f}")


def member_summary():
    totals = _totals_by("Payer")
    print("\n===== INDIVIDUAL PAYMENT SUMMARY =====")

    if not totals:
        print("No payment records found.")
        return

    for payer, amount in totals.items():
        print(f"{payer}: Rs. {amount:.2f}")


def highest_spending_category():
    totals = _totals_by("Category")
    print("\n===== HIGHEST SPENDING CATEGORY =====")

    if not totals:
        print("No expenses available.")
        return

    highest = max(totals, key=totals.get)
    print("Category:", highest)
    print(f"Amount: Rs. {totals[highest]:.2f}")


def expense_chart(max_width=40):
    """Text bar chart, scaled so the biggest category is max_width characters."""
    totals = _totals_by("Category")
    print("\n===== EXPENSE BAR CHART =====")

    if not totals:
        print("No expenses available.")
        return

    biggest = max(totals.values())

    for category, amount in totals.items():
        bar_length = max(1, round(amount / biggest * max_width))
        print(f"{category:15} | {'#' * bar_length} Rs. {amount:.2f}")


def run_analytics():
    while True:
        print("\n===== GROUP TRAVEL ANALYTICS =====")
        print("1. Total Group Expenses")
        print("2. Category-wise Breakdown")
        print("3. Individual Member Summary")
        print("4. Highest Spending Category")
        print("5. Expense Bar Chart")
        print("6. Complete Analytics Report")
        print("7. Back to Main Menu")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            total_expenses()
        elif choice == "2":
            category_breakdown()
        elif choice == "3":
            member_summary()
        elif choice == "4":
            highest_spending_category()
        elif choice == "5":
            expense_chart()
        elif choice == "6":
            total_expenses()
            category_breakdown()
            member_summary()
            highest_spending_category()
            expense_chart()
        elif choice == "7":
            break
        else:
            print("Invalid choice! Please select from 1 to 7.")
