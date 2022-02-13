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
        self.choose_item()

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
            line_array = line.split(",")
            name = line_array[0]
            #converts to float
            price_float = float(line_array[1])          
            #stores as string to 2 decimal places
            price_string = "{:.2f}".format(price_float)
            if price_float < 1:
                price_string = str(price_string).split(".")[1]+"p"
            else:
                price_string = "£"+str(price_string)
            amount = line_array[2]
            
            self.items_dictionary[code] = {
                'name': name,
                'stored_price': price_float, 
                'display_price': price_string, 
                'amount': amount
            }
            number += 1

    # this should be called at the start and each time they pay
    def display_stock(self):
        # see_stock=input("Please press enter to see the stock")
        #loops through every product - by its product code
        for product_code,product_info in self.items_dictionary.items():
            #prints out the product code, name, price and amount
            print(product_code+":"+product_info['name']+" - "+product_info['display_price']+" x "+str(product_info['amount']))

    def choose_item(self):
        code = input("Please enter the product code for the item you would like to enter\n")
        if code in self.items_dictionary:
            print("That will be "+str(self.items_dictionary[code]['display_price']))
        else:
            print("That isn't a valid selection")

    def update_stock(self, code, amount):
        return

    def insert_money(self, money):
        if money <= 0.00:
            raise ValueError
        self.money_inserted += money


VendingMachine()