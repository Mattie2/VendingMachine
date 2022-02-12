"""
Contains all models relating to money, coins, etc.
"""
from decimal import Decimal

class CashAmount(Decimal):
    """
    Represents a cash amount.
    Extends the decimal.Decimal class.
    """
    def __repr__(self):
        return f"CashAmount('{self}')"

    def __str__(self):
        return f'${self:,.2f}'


class Coin:
    """Base class representing coins."""
    value = CashAmount('0')

    def __radd__(self, other):
        return self.value + other

    def __eq__(self, other):
        return self.value == other.value

class OnePence(Coin):
    """1p coin."""
    value = CashAmount('0.01')

class TwoPence(Coin):
    """2p coin."""
    value = CashAmount('0.02')

class FivePence(Coin):
    """5p coin."""
    value = CashAmount('0.05')

class TenPence(Coin):
    """10p coin."""
    value = CashAmount('0.10')

class TwentyPence(Coin):
    """20p coin."""
    value = CashAmount('0.20')

class FiftyPence(Coin):
    """50p coin"""
    value = CashAmount('0.50')
class OnePound(Coin):
    """£1 coin."""
    value = CashAmount('1.00')

class TwoPounds(Coin):
    """£2 coin."""
    value = CashAmount('2.00')

class FivePounds(Coin):
    """£5 note"""
    value = CashAmount('5.00')

class TenPounds(Coin):
    """£10 note"""
    value = CashAmount('10.00')

class TwentyPounds(Coin):
    """£20 note"""
    value = CashAmount('20.00')

class FiftyPounds(Coin):
    """£50 note"""
    value = CashAmount('50.00')