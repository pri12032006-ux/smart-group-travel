from storage import create_file
from expenses import save_expense, show_expenses
from settlement import calculate_settlement
from analytics import run_analytics


def display_menu():
    print("\n==========================================")
    print("       GROUP TRAVEL EXPENSE MANAGER")
    print("==========================================")
    print("1. Add New Expense")
    print("2. View All Expenses")
    print("3. Calculate Expense Settlement")
    print("4. View Expense Analytics")
    print("5. Exit")
    print("==========================================")


def main():
    create_file()

    print("\nWelcome to Group Travel Expense Management System!")

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            print("\n---------- ADD NEW EXPENSE ----------")
            save_expense()
        elif choice == "2":
            print("\n---------- ALL EXPENSES ----------")
            show_expenses()
        elif choice == "3":
            calculate_settlement()
        elif choice == "4":
            print("\n---------- EXPENSE ANALYTICS ----------")
            run_analytics()
        elif choice == "5":
            print("\nThank you for using Group Travel Expense Manager!")
            print("Have a safe and happy trip!")
            break
        else:
            print("\nInvalid choice! Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
