
import csv
import os

FILE_NAME = "expenses.csv"

CATEGORIES = {
    "1": "Transport",
    "2": "Food",
    "3": "Hotel",
    "4": "Other Expenses"
}

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


def create_file():
    if not os.path.isfile(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Payer", "Amount", "Category", "Description"]
            )


def choose_category():
    print("\nSelect Expense Category:")

    for key, value in CATEGORIES.items():
        print(key + ". " + value)

    while True:
        choice = input("Enter category number (1-4): ")

        if choice in CATEGORIES:
            return CATEGORIES[choice]

        print("Invalid choice. Please select from 1 to 4.")


def choose_description(category):
    if category == "Other Expenses":
        return input("Enter expense description: ")

    options = DESCRIPTION_OPTIONS[category]

    print("\nSelect Description:")

    for key, value in options.items():
        print(key + ". " + value)

    while True:
        choice = input("Enter your choice: ")

        if choice in options:
            return options[choice]

        print("Invalid choice. Please select a listed option.")


def save_expense():
    payer = input("Enter payer name: ")

    while True:
        try:
            amount = float(input("Enter expense amount (Rs.): "))

            if amount > 0:
                break

            print("Amount must be greater than zero.")

        except ValueError:
            print("Please enter a valid amount.")

    category = choose_category()
    description = choose_description(category)

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([payer, amount, category, description])

    print("\nExpense saved successfully!")


def show_expenses():
    create_file()

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        print("\n===== STORED EXPENSE RECORDS =====")

        found = False

        for record in reader:
            found = True
            print("Payer:", record["Payer"])
            print("Amount: Rs.", record["Amount"])
            print("Category:", record["Category"])
            print("Description:", record["Description"])
            print("----------------------------------")

        if not found:
            print("No expense records found.")


def main():
    create_file()

    while True:
        print("\n===== TRAVEL EXPENSE MANAGER =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            save_expense()

        elif choice == "2":
            show_expenses()

        elif choice == "3":
            print("Thank you for using the Travel Expense Manager!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

