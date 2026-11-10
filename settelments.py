from storage import read_expenses


def compute_net_balances(members):
    """
    Net balance per member (positive = should receive, negative = should pay).
    Payer names are matched case-insensitively.
    """
    expenses = read_expenses()
    lookup = {m.lower(): m for m in members}
    balances = {m: 0.0 for m in members}
    unknown_payers = set()

    for record in expenses:
        amount = record["Amount"]
        share = amount / len(members)
        payer = lookup.get(record["Payer"].strip().lower())

        if payer:
            balances[payer] += amount
        else:
            unknown_payers.add(record["Payer"])

        for m in members:
            balances[m] -= share

    return balances, unknown_payers


def suggest_payments(balances):
    """Turn net balances into a short list of 'A pays B' transfers."""
    debtors = sorted([[m, -b] for m, b in balances.items() if b < -0.01], key=lambda x: -x[1])
    creditors = sorted([[m, b] for m, b in balances.items() if b > 0.01], key=lambda x: -x[1])
    payments = []

    i = j = 0
    while i < len(debtors) and j < len(creditors):
        pay = min(debtors[i][1], creditors[j][1])
        payments.append((debtors[i][0], creditors[j][0], pay))
        debtors[i][1] -= pay
        creditors[j][1] -= pay
        if debtors[i][1] < 0.01:
            i += 1
        if creditors[j][1] < 0.01:
            j += 1

    return payments


def get_members():
    """Ask for group members; pressing Enter uses the payer names found in the CSV."""
    known = list(dict.fromkeys(r["Payer"].strip() for r in read_expenses() if r["Payer"].strip()))

    while True:
        if known:
            print(f"\nPayers found in file: {', '.join(known)}")
            prompt = "Enter group member names separated by commas (or press Enter to use the above): "
        else:
            prompt = "\nEnter group member names separated by commas: "

        names = input(prompt).strip()

        if not names and known:
            members = known
        else:
            members = list(dict.fromkeys(n.strip() for n in names.split(",") if n.strip()))

        if len(members) >= 2:
            return members

        print("Please enter at least two valid member names.")


def calculate_settlement():
    print("\n---------- EXPENSE SETTLEMENT ----------")

    if not read_expenses():
        print("No expenses recorded yet. Please add expenses first.")
        return

    members = get_members()

    try:
        balances, unknown = compute_net_balances(members)
    except Exception as error:
        print("Unable to calculate settlement:", error)
        return

    print("\n---------- NET BALANCES ----------")
    for member, balance in balances.items():
        if balance > 0.01:
            print(f"{member} should receive: Rs. {balance:.2f}")
        elif balance < -0.01:
            print(f"{member} should pay: Rs. {abs(balance):.2f}")
        else:
            print(f"{member} is settled.")

    payments = suggest_payments(balances)
    if payments:
        print("\n---------- SUGGESTED PAYMENTS ----------")
        for debtor, creditor, amount in payments:
            print(f"{debtor} pays {creditor}: Rs. {amount:.2f}")

    if unknown:
        print(f"\nNote: these payers are not in your member list, so their payments "
              f"were not credited: {', '.join(sorted(unknown))}")

    print("----------------------------------")
