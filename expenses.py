import csv
import os

FILE_NAME = "expenses.csv"

# Predefined categories for group travel
CATEGORIES = {
    "1": "Transport",
    "2": "Food",
    "3": "Hotel",
    "4": "Other Expenses"
}

# Sub-options for categories
DESCRIPTION_OPTIONS = {
    "Transport": {
        "1": "Car",
        "2": "Bus",
        "3": "Train"
    },
    "Food": {
        "1": "Veg",
        "2": "Non-Veg"
    },
    "Hotel": {
        "1": "4 Star",
        "2": "5 Star",
        "3": "7 Star"
    }
}

# Budget thresholds for rule-based alerts
CATEGORY_BUDGET_LIMITS = {
    "Transport": 5000.0,
    "Food": 4000.0,
    "Hotel": 10000.0,
    "Other Expenses": 3000.0
}


def create_file():
    """Ensure the expenses CSV file exists with proper headers."""
    if not os.path.isfile(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Payer", "Amount", "Category", "Description"])


def get_category_total(category_name):
    """Calculates total current spending for a specific category from the CSV file."""
    if not os.path.isfile(FILE_NAME):
        return 0.0
    
    total = 0.0
    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Category"] == category_name:
                try:
                    total += float(row["Amount"])
                except ValueError:
                    continue
    return total


def check_budget_rules(category, new_amount):
    """Evaluates spending against threshold rules and triggers alerts if exceeded."""
    current_total = get_category_total(category)
    projected_total = current_total + new_amount
    
    limit = CATEGORY_BUDGET_LIMITS.get(category, float('inf'))
    
    print(f"\n[Budget Check] Current total for {category}: Rs. {current_total:.2f} (Limit: Rs. {limit:.2f})")
    
    if projected_total > limit:
        print(f"⚠️ [BUDGET ALERT] Adding this expense will exceed the budget limit for '{category}'!")
        print(f"Projected Total: Rs. {projected_total:.2f} | Limit: Rs. {limit:.2f}")
    else:
        print(f"✅ Spending is within the safe limit for '{category}'.")


def choose_category():
    """Prompts user to select an expense category."""
    print("\nSelect Expense Category:")
    for key, value in CATEGORIES.items():
        print(f"{key}. {value}")
    while True:
        choice = input("Enter category number (1-4): ")
        if choice in CATEGORIES:
            return CATEGORIES[choice]
        print("Invalid choice. Please select from 1 to 4.")


def choose_description(category):
    """Prompts user for specific description options or custom entry."""
    if category == "Other Expenses":
        return input("Enter expense description: ")
    
    options = DESCRIPTION_OPTIONS[category]
    print("\nSelect Description:")
    for key, value in options.items():
        print(f"{key}. {value}")
    while True:
        choice = input("Enter your choice: ")
        if choice in options:
            return options[choice]
        print("Invalid choice. Please select a listed option.")


def save_expense():
    """Logs a new expense, checks budget rules, and appends it to the CSV storage."""
    create_file()
    payer = input("Enter payer name: ")
    
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
    
    # Rule Engine Check
    check_budget_rules(category, amount)
    
    # Save record
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([payer, amount, category, description])
        
    print(f"\n[SUCCESS] Recorded expense: Rs. {amount:.2f} paid by {payer} for '{description}' ({category}).")


def show_expenses():
    """Displays all recorded expenses from storage."""
    create_file()
    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        print("\n===== STORED EXPENSE RECORDS =====")
        found = False
        for record in reader:
            found = True
            print(f"Payer: {record['Payer']}")
            print(f"Amount: Rs. {record['Amount']}")
            print(f"Category: {record['Category']}")
            print(f"Description: {record['Description']}")
            print("-" * 34)
        if not found:
            print("No expense records found.")


# Interactive loop asking if the user wants to run again
create_file()
print("===== EXPENSE & RULE ENGINE MODULE =====")

while True:
    save_expense()
    show_expenses()
    
    # Ask user if they want to run again
    repeat = input("\nDo you want to add another expense? (y/n): ").strip().lower()
    if repeat != 'y':
        print("\nExiting Expense Module. Have a great trip!")
        break