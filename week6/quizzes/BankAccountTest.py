__author__ = 'claube'

import unittest
from BankAccount import BankAccount

class MyTestCase(unittest.TestCase):
    def test_something(self):
        # Test 1
        my_account = BankAccount(10)
        my_account.withdraw(5)
        my_account.deposit(10)
        my_account.withdraw(5)
        my_account.withdraw(15)
        my_account.deposit(20)
        my_account.withdraw(5)
        my_account.deposit(10)
        my_account.deposit(20)
        my_account.withdraw(15)
        my_account.deposit(30)
        my_account.withdraw(10)
        my_account.withdraw(15)
        my_account.deposit(10)
        my_account.withdraw(50)
        my_account.deposit(30)
        my_account.withdraw(15)
        my_account.deposit(10)
        my_account.withdraw(5)
        my_account.deposit(20)
        my_account.withdraw(15)
        my_account.deposit(10)
        my_account.deposit(30)
        my_account.withdraw(25)
        my_account.withdraw(5)
        my_account.deposit(10)
        my_account.withdraw(15)
        my_account.deposit(10)
        my_account.withdraw(10)
        my_account.withdraw(15)
        my_account.deposit(10)
        my_account.deposit(30)
        my_account.withdraw(25)
        my_account.withdraw(10)
        my_account.deposit(20)
        my_account.deposit(10)
        my_account.withdraw(5)
        my_account.withdraw(15)
        my_account.deposit(10)
        my_account.withdraw(5)
        my_account.withdraw(15)
        my_account.deposit(10)
        my_account.withdraw(5)
        print my_account.get_balance(), my_account.get_fees()
        # Test 2
        account1 = BankAccount(10)
        account1.withdraw(15)
        account2 = BankAccount(15)
        account2.deposit(10)
        account1.deposit(20)
        account2.withdraw(20)
        print account1.get_balance(), account1.get_fees(), account2.get_balance(), account2.get_fees()
        # Test 3
        account1 = BankAccount(20)
        account1.deposit(10)
        account2 = BankAccount(10)
        account2.deposit(10)
        account2.withdraw(50)
        account1.withdraw(15)
        account1.withdraw(10)
        account2.deposit(30)
        account2.withdraw(15)
        account1.deposit(5)
        account1.withdraw(10)
        account2.withdraw(10)
        account2.deposit(25)
        account2.withdraw(15)
        account1.deposit(10)
        account1.withdraw(50)
        account2.deposit(25)
        account2.deposit(25)
        account1.deposit(30)
        account2.deposit(10)
        account1.withdraw(15)
        account2.withdraw(10)
        account1.withdraw(10)
        account2.deposit(15)
        account2.deposit(10)
        account2.withdraw(15)
        account1.deposit(15)
        account1.withdraw(20)
        account2.withdraw(10)
        account2.deposit(5)
        account2.withdraw(10)
        account1.deposit(10)
        account1.deposit(20)
        account2.withdraw(10)
        account2.deposit(5)
        account1.withdraw(15)
        account1.withdraw(20)
        account1.deposit(5)
        account2.deposit(10)
        account2.deposit(15)
        account2.deposit(20)
        account1.withdraw(15)
        account2.deposit(10)
        account1.deposit(25)
        account1.deposit(15)
        account1.deposit(10)
        account1.withdraw(10)
        account1.deposit(10)
        account2.deposit(20)
        account2.withdraw(15)
        account1.withdraw(20)
        account1.deposit(5)
        account1.deposit(10)
        account2.withdraw(20)
        print account1.get_balance(), account1.get_fees(), account2.get_balance(), account2.get_fees()


if __name__ == '__main__':
    unittest.main()