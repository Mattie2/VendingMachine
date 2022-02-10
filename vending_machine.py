"""
Contains vending machine model.
"""
import money


# Coin types used by machine
CASH_CLASSES = [
    money.FiftyPounds,
    money.TwentyPounds,
    money.TenPounds,
    money.FivePounds,
    money.TwoPounds,
    money.OnePound,
    money.FiftyPence,
    money.TwentyPence,
    money.TenPence,
    money.FivePence,
    money.TwoPence,
    money.OnePence

]


class VendingMachine:
    """
    A virtual vending machine.
    """
    def __init__(self):
        self.inserted_coins = []

    

    def insert_coin(self, coin):
        """
        Accepts a Coin instance and inserts it into the vending machine.
        """
        if not isinstance(coin, money.Coin):
            raise ValueError()

        self.inserted_coins.append(coin)

    def get_balance(self):
        """
        Returns the balance remaining.
        """
        return sum(self.inserted_coins)

    def get_change(self):
        """
        Returns change representing positive balance. The largest
        denominations are always used first.
        """
        coins = []
        balance = self.get_balance()
        balance -= balance * 100 % 5

        while balance > 0:
            for coin_class in reversed(COIN_CLASSES):
                if balance - coin_class.value >= 0:
                    coin = coin_class()  # Create a coin instance
                    coins.append(coin)
                    balance -= coin_class.value
                    break

        return coins