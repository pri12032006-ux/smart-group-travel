from storage import create_file, read_expenses, append_expense

CATEGORIES = {
    "1": "Transport",
    "2": "Food",
    "3": "Hotel",
    "4": "Other Expenses",
}

DESCRIPTION_OPTIONS = {
    "Transport": {"1": "Car", "2": "Bus", "3": "Train"},
    "Food": {"1": "Veg", "2": "Non-Veg"},
    "Hotel": {"1": "4 Star", "2": "5 Star", "3": "7 Star"},
}

# Budget thresholds for rule-based alerts
CATEGORY_BUDGET_LIMITS = {
    "Transport": 5000.0,
    "Food": 4000.0,
    "Hotel": 10000.0,
    "Other Expenses": 3000.0,
}


def choose_category():
    print("\nSelect Expense Category:")
    for key, value in CATEGORIES.items():
        print(f"{key}. {value}")

    while True:
        choice = input("Enter category number (1-4): ").strip()
        if choice in CATEGORIES:
            return CATEGORIES[choice]
        print("Invalid choice. Please select from 1 to 4.")


def choose_description(category):
    if category == "Other Expenses":
        while True:
            text = input("Enter expense description: ").strip()
            if text:
                return text
            print("Description cannot be empty.")

    options = DESCRIPTION_OPTIONS[category]

    print("\nSelect Description:")
    for key, value in options.items():
        print(f"{key}. {value}")

    while True:
        choice = input("Enter your choice: ").strip()
        if choice in options:
            return options[choice]
        print("Invalid choice. Please select a listed option.")


def get_category_total(category_name):
    """Total spending so far for one category."""
    return sum(r["Amount"] for r in read_expenses() if r["Category"] == category_name)


def check_budget_rules(category, new_amount):
    """Warn if adding new_amount pushes the category over its budget limit."""
    current_total = get_category_total(category)
    projected_total = current_total + new_amount
    limit = CATEGORY_BUDGET_LIMITS.get(category, float("inf"))

    print(f"\n[Budget Check] Current total for {category}: Rs. {current_total:.2f} "
          f"(Limit: Rs. {limit:.2f})")

    if projected_total > limit:
        print(f"⚠️  [BUDGET ALERT] This expense will exceed the budget limit for '{category}'!")
        print(f"Projected Total: Rs. {projected_total:.2f} | Limit: Rs. {limit:.2f}")
    else:
        print(f"✅ Spending is within the safe limit for '{category}'.")


def save_expense():
    """Ask for a new expense, run budget check, and append it to the CSV."""
    create_file()

    while True:
        payer = input("Enter payer name: ").strip()
        if payer:
            break
        print("Payer name cannot be empty.")

    while True:
        try:
            amount = float(input("Enter expense amount (Rs.): "))
            if amount > 0:
                break
            print("Amount must be greater than zero.")
        except ValueError:
            print("Please enter a valid numerical amount.")

    category = choose_category()
    description = choose_description(category)

    check_budget_rules(category, amount)

    append_expense(payer, amount, category, description)

    print(f"\n[SUCCESS] Recorded expense: Rs. {amount:.2f} paid by {payer} "
          f"for '{description}' ({category}).")


def show_expenses():
    expenses = read_expenses()

    print("\n===== STORED EXPENSE RECORDS =====")

    if not expenses:
        print("No expense records found.")
        return

    for record in expenses:
        print("Payer:", record["Payer"])
        print(f"Amount: Rs. {record['Amount']:.2f}")
        print("Category:", record["Category"])
        print("Description:", record["Description"])
        print("----------------------------------")
