# from vending_machine import CASH_CLASSES
import money
#TODO: have welcome screen and choice of products ready next time

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

class Item:
    def __init__(self, code, name, price):
        # creates an item and assigns the attributes to the instance of the item
        self.code = code
        self.name = name
        self.price = price


class VendingMachine:
    def __init__(self):
    #get this from csv file - have amount of each item e.g. 5 cans of pepsi etc aswell
        self.items = [
            Item("Tea", 0.50),
            Item("Coffee", 1.00),
            Item("Coke", 1.50),
            Item("Orange Juice", 1.00)
        ]

        self.money_inserted = 0.00

    #this should be called at the start and each time they pay
    def display_stock(self):
        for code, item in enumerate(self.items, start=1):
            print(f"[{code}] - {item.name} (${item.price:.2f})")

    def insert_money(self, money):
        if money <= 0.00:
            raise ValueError
        self.money_inserted += money

