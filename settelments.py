import csv
# To read the csv file
def read_expenses():
    expenses = []

    with open("expenses.csv", "r", newline = "") as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append(row)

    return expenses
# To find the share
def compute_net_balances(members):
    expenses = read_expenses()
    balances = {}

    for i in members:
        balances[i] = 0

    for n in expenses:
        payer = i["Payer"]
        amount = i["Amount"]

        share = amount/len(members)
        if payer in balances:
            balances[payer] += amount

        for i in members:
            balances[i] -= share

    return balances
