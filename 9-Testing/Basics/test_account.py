import pytest

class Account:
    def __init__(self, balance = 0) -> None:
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception("Insufficient funds in the account!!")
        self.balance -= amount

@pytest.fixture
def account():
    return Account(50)

def test_balance_amount(account):
    assert account.balance == 50

def test_deposit(account):
    account.deposit(20)
    assert account.balance == 70

def test_withdraw(account):
    account.withdraw(30)
    assert account.balance == 20

def test_insufficient_funds(account):
    with pytest.raises(Exception):
        account.withdraw(70)