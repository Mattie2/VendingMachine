from coin import Cash
from item import Item

class VendingMachine:
    def __init__(self, stock_file="items.csv"):
        """
        Create an instance of the vending machine class. Initialises attributes and calls relevant methods.
        """
        self.items_dictionary = {}
        self.chosen_items_dictionary = {}
        self.money_inserted = 0.00
        self.total_price = 0.00
        self.stock_file = stock_file
        self.welcome_message()
        self.get_stock()
        self.display_stock()
        self.choose_items()
        self.update_stock()

    def welcome_message(self):
        """
        Displays a welcome message to the user.
        """
        print("Hello and welcome to the vending machine.")
        print("This machine accepts the following cash amounts: ")
        print(Cash.get_valid_cash_instances())  
        print("\n\nWe hope you'll find the snack you're looking for!")

    def get_stock(self):
        """
        Gets the stock from the csv file and adds it to item dictionary attribute. 
        A similiar attribute called chosen item dictionary, which stores the quantity of each item purchased by the user.
        """
        number = 0
        letter = "A"
        f = open(self.stock_file, "r")
        # loop through every line in the text file
        for line in f:
            # removes any line breaks
            line = line.replace("\n", "")            
            # change letter every 10 lines and reset number to 0
            if(number > 9):
                letter = chr(ord(letter)+1)
                number = 0
            code = letter+str(number)
            # csv file format: item_name,item_price, item_quantity
            line_array = line.split(",")
            name = line_array[0]
            price = line_array[1]
            quantity = line_array[2]
            # #converts to float        
            self.items_dictionary[code] = Item(name,price,quantity)
            self.chosen_items_dictionary[code] = Item(name,price,0)
            number += 1

    def display_stock(self):
        """
        Loops through every product by its product code and outputs it to the terminal
        """
        for product_code,product_item in self.items_dictionary.items():
            #prints out the product code, name, price and quantity
            # print(product_code+":"+product_info['name']+" - "+product_info['display_price']+" x "+str(product_info['quantity']))
            print(product_code+":"+product_item.get_summary())
        print('\n')

    def choose_items(self):        
        """
        Validates the user's selection, printing a message if there selection isn't valid or is out of stock
        """
        while True:
            #keep asking the user until they dont want anything else
            code = input("Please enter the product code for the item you would like to enter. (Enter 'STOP' to pay for your items)\n")
            if code == 'stop' or code == 'STOP' or code =='Stop':
                break
            if code in self.items_dictionary:
                #check stock to see whether its available
                if self.chosen_items_dictionary[code]>=self.items_dictionary[code]:
                    print("We're sorry, but there isn't anymore "+str(self.chosen_items_dictionary[code]))
                    #restarts the loop from the top 
                    continue
                self.chosen_items_dictionary[code].update_quantity(1)
                item = self.items_dictionary[code]
                #total price is appended to after every selection
                self.total_price += item.get_stored_price()
            else:
                print("That isn't a valid selection")
        print("That will be £{:.2f}".format(self.total_price))
        self.take_payment()

    def take_payment(self):
        """
        Takes the payment from the user. It ensures the user enters a valid coin/note amount and displays any change they have.
        """
        while self.money_inserted < self.total_price:
            print(f"You've inserted £{self.money_inserted:.2f} into the machine so far.")
            #this loop ensures the user can enter a new cash amount in if their previous cash amount wasnt valid
            while True:
                try:
                    money_to_insert = float(input("Please enter the amount of money you'd like to insert: "))
                    self.insert_money(money_to_insert)
                except ValueError:
                    #value error occurs when the cash amount entered is invalid
                    if money_to_insert < 5:
                        print("This machine doesnt accept £{:.2f} coins".format(money_to_insert))
                    else:
                        print("This machine doesnt accept £{:.2f} notes".format(money_to_insert))        
                    print("This machine accepts the following cash amounts: ")
                    print(Cash.get_valid_cash_instances())                           
                #break out of the inner loop if the cash inserted was valid     
                else:
                    break        
        itemsString = ""
        for code in self.chosen_items_dictionary:
            if self.chosen_items_dictionary[code].get_quantity()>0:
                itemsString += str(self.chosen_items_dictionary[code])+" x "+str(self.chosen_items_dictionary[code].get_quantity())+ " "
        print(f"Thank you! Please take your items:")
        print(itemsString)
        coins,notes = self.get_change()        
        if notes:
            print("Here's your notes")    
            print(notes)
        if coins:
            print("Here's your coins")
            print(coins)            

    def update_stock(self):
        """
        This is called after the user has payed for their items. It updates the csv file with the new amounts.
        """
        #here take quantity of selected stock away from self.items_dictionary. Then write the dictionary back into the csv file
        csvfile = ""
        for code in self.items_dictionary:
            #takes the quantity of each item chosen away from the total quantity of that item
            self.items_dictionary[code] -= self.chosen_items_dictionary[code]
            csvfile+=repr(self.items_dictionary[code])+'\n'
        f = open(self.stock_file, "w")
        f.write(csvfile)
        f.close()
        print("The vending machine stock has been updated")

    def insert_money(self, cash):
        """
        Checks if the cash is a valid amount and updates the money inserted if so.
        """
        #a value error will be returned if the cash parameter is invalid
        Cash(cash)
        self.money_inserted +=cash   

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
        #checking if change >=0 caused a bug when 1p coins were used
        while change > 0.01:
            for cash_amount in reversed(Cash.get_valid_cash()):
                # print("change - "+str(change)+" cash amount - "+str(cash_amount))
                if change >= cash_amount:
                    # Create a cash instance to display user's change
                    cash_object = Cash(cash_amount)
                    if cash_amount<5:
                        coins.append(cash_object)
                    else:
                        notes.append(cash_object)                 
                    change -= cash_amount
                    break
        return coins,notes      

#creates an instance of the vending nachine class
machine = VendingMachine()