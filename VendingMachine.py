# from vending_machine import CASH_CLASSES
import money
# TODO: have welcome screen and choice of products ready next time

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
    def __init__(self, stock_file="items.csv"):
        # get this from csv file - have amount of each item e.g. 5 cans of pepsi etc aswell
        self.items_dictionary = {}
        self.money_inserted = 0.00
        self.welcome_message()
        self.get_stock()
        self.display_stock()

    def welcome_message(self):
        print("Hello and welcome to the vending machine.")
        print("We hope you'll find the snack you're looking for.")

    def get_stock(self):
        number = 0
        letter = "A"
        f = open("items.csv", "r")
        # loop through every line in the text file
        for line in f:
            # change letter every 10 lines and reset number to 0
            # remove the line break
            line = line.replace("\n", "")
            if(number > 9):
                letter = chr(ord(letter+1))
                number = 0
            code = letter+str(number)
            # text file format: item_name,item_price
            lineArray = line.split(",")
            name = lineArray[0]
            price = lineArray[1]
            amount = lineArray[2]
            
            self.items_dictionary[code] = {
                'name': name,
                'price': price, 
                'amount': amount
            }
            number += 1

    # this should be called at the start and each time they pay
    def display_stock(self):
        for product_code,product_info in self.items_dictionary.items():
            print(product_code)
            for key in product_info:
                if product_info[key]
                print(key + ':' + product_info[key])


    def update_stock(self, code, amount):
        return

    def insert_money(self, money):
        if money <= 0.00:
            raise ValueError
        self.money_inserted += money


VendingMachine()