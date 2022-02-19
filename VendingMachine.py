# from vending_machine import CASH_CLASSES
from coin import Cash
# TODO: have welcome screen and choice of products ready next time

VALID_CASH = [
    0.01,0.02,0.05,0.10,0.20,0.50,1.00,2.00,5.00,10.00,20.00,50.00
]

VALID_CASH_INSTANCES = []    
for value in VALID_CASH:
    cash = Cash(value)
    VALID_CASH_INSTANCES.append(cash) 

class VendingMachine:
    def __init__(self, stock_file="items.csv"):
        # get this from csv file - have amount of each item e.g. 5 cans of pepsi etc aswell
        self.items_dictionary = {}
        self.chosen_items_dictionary = {}
        self.money_inserted = 0.00
        self.total_price = 0.00
        self.welcome_message()
        self.get_stock()
        self.display_stock()
        self.choose_items()
        self.update_stock()

    def welcome_message(self):
        print("Hello and welcome to the vending machine.")
        print("We hope you'll find the snack you're looking for.")
        print("This machine accepts the following cash amounts: ")
        print(VALID_CASH_INSTANCES)
        # print [cash.value for cash in VALID_CASH_INSTANCES]

        # print(', '.join(str(VALID_CASH_INSTANCES)))

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
            quantity = line_array[2]
            
            self.items_dictionary[code] = {
                'name': name,
                'stored_price': price_float, 
                'display_price': price_string, 
                'quantity': quantity
            }
            self.chosen_items_dictionary[code] = {
                'name' : name,
                'stored_price' : price_float,
                'display_price' : price_string,
                #quantity chosen is initalised to 0 for every item
                'quantity' : 0
            }
            number += 1

    # this should be called at the start and each time they pay
    def display_stock(self):
        # see_stock=input("Please press enter to see the stock")
        #loops through every product - by its product code
        for product_code,product_info in self.items_dictionary.items():
            #prints out the product code, name, price and quantity
            print(product_code+":"+product_info['name']+" - "+product_info['display_price']+" x "+str(product_info['quantity']))

    def choose_items(self):        
        while True:
            code = input("Please enter the product code for the item you would like to enter\n")
            if code in self.items_dictionary:
                #check stock to see whether its available
                self.chosen_items_dictionary[code]['quantity']+=1
                item = self.items_dictionary[code]
                self.total_price += item['stored_price']
                more = input("Would you like anything else? Enter yes or no\n")
                if more == "No" or more == "No" or more == "no":
                    break
            else:
                print("That isn't a valid selection")

        print("That will be £{:.2f}".format(self.total_price))
        self.take_payment()

    def take_payment(self):
        # self.money_inserted = 0
        # item = self.items_dictionary[product_code]
        # while self.money_inserted < item['stored_price']:
        while self.money_inserted < self.total_price:
            print(f"You've inserted £{self.money_inserted:.2f} into the machine so far.")
            #this loop ensures the user can enter a new cash amount in if their previous cash amount wasnt valid
            while True:
                try:
                    money_to_insert = float(input("Please enter the amount of money you'd like to insert: "))
                    # self.insert_cash(money_to_insert)
                    self.insert_money(money_to_insert)
                except ValueError:
                    if money_to_insert < 5:
                        print("This machine doesnt accept £{:.2f} coins".format(money_to_insert))
                    else:
                        print("This machine doesnt accept £{:.2f} notes".format(money_to_insert))        
                    print("This machine accepts the following cash amounts: ")
                    print(VALID_CASH_INSTANCES)                           
                #break out of the loop if the cash inserted was valid     
                else:
                    break
        #update to show multiple items
        # print(f"Thank you! Please take your \"{item['name']}\".")
        
        itemsString = ""
        for code in self.chosen_items_dictionary:
            if self.chosen_items_dictionary[code]['quantity']>0:
                itemsString += self.chosen_items_dictionary[code]['name']+" x "+str(self.chosen_items_dictionary[code]['quantity'])+ " "
        print(f"Thank you! Please take your "+itemsString)
        coins,notes = self.get_change()        
        # print(f"The remaining change in the machine is £{self.money_inserted - item['stored_price']:.2f}.")
        if notes:
            print("Here's your notes")    
            print(notes)
        if coins:
            print("Here's your coins")
            print(coins)            

    def update_stock(self):
        #here take quantity of selected stock away from self.items_dictionary. Then write the dictionary back into the csv file
        return
        #add a message to say the stock has been updated - message saying if things are sold out

    def insert_money(self, cash):
        """
        Checks if the cash is a valid amount and updates the money inserted if so.
        """
        if not cash in VALID_CASH:
            raise ValueError()

        self.money_inserted +=cash

    # def get_balance(self):
    #     """
    #     Returns the balance remaining.
    #     """
    #     return sum(self.inserted_coins)        

    def get_change(self):
        """
        Returns change representing positive balance. The largest
        denominations are always used first.
        """
        coins = []
        notes = []
        money_inserted = self.money_inserted
        price = self.total_price
        change = money_inserted-price
        # balance -= balance * 100 % 5

        while change > 0:
            for cash_amount in reversed(VALID_CASH):
                if change >= cash_amount:
                    # coin = coin_class()  # Create a coin instance
                    cash_object = Cash(cash_amount)
                    if cash_amount<5:
                        coins.append(cash_object)
                    else:
                        notes.append(cash_object)
                    change -= cash_amount
                    break

        return coins,notes      

machine = VendingMachine()