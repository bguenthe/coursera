class BankAccount:
    def __init__(self, initial_balance):
        """Creates an account with the given balance."""
        self.balance = initial_balance
        self.fees = 0

    def deposit(self, amount):
        """Deposits (einzahlen) the amount into the account."""
        self.balance += amount

    def withdraw(self, amount):
        """
        Withdraws (abheben) the amount from the account.  Each withdrawal resulting in a
        negative balance also deducts a penalty fee of 5 dollars from the balance.
        """
        local_fee = 0
        if self.get_balance() - amount < 0:
            self.fees += 5
            local_fee = 5

        self.balance -= amount + local_fee

    def get_balance(self):
        """Returns the current balance in the account."""
        return self.balance


    def get_fees(self):
        """Returns the total fees ever deducted from the account."""
        return self.fees