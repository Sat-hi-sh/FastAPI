import pytest
from app.calculation import add, BankAccount, InsufficientFund

@pytest.fixture
def zero_bank_account():
    account_balance = BankAccount()
    return account_balance

@pytest.fixture
def bank_account():
    account_balance = BankAccount(50)
    return account_balance

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 4, 7),
    (12, 5, 17),
    (45, 3, 48)
])
def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2) == expected

def test_bank_zero_account(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_initial_account(bank_account):
    assert bank_account.balance == 50

def test_bank_balance_withdraw(bank_account):
    bank_account.withdraw(30)
    assert bank_account.balance == 20

def test_bank_balance_deposit(bank_account):
    bank_account.deposit(40)
    assert bank_account.balance == 90


@pytest.mark.parametrize("deposit, withdraw, expected",[
    (100,50,50),
    (300,150,150),
    (55,25,30)
])
def test_bank_transaction(zero_bank_account,deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_insufficient(bank_account):
    with pytest.raises(InsufficientFund):
        bank_account.withdraw(70)