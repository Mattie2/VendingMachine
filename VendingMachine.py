from pickle import FALSE
from cash import Coins,Notes,Cash
from item import Item

class VendingMachine:
    def __init__(self, stock_file="items.csv"):
        """
        Create an instance of the vending machine class. Initialises attributes and calls relevant methods.
        """
        #double underscore ensures all of the attributes are private
        self.__chosen = False
        self.__items_dictionary = {}
        self.__chosen_items_dictionary = {}
        #these are integers - cash values stored as integers
        self.__money_inserted = 0
        self.__total_price = 0
        self.__stock_file = stock_file
        self.welcome_message()
        self.get_stock()
        self.display_stock()
        self.choose_items()
        if self.__chosen == True:
            self.update_stock()

    def welcome_message(self):
        """
        Displays a welcome message to the user.
        """
        print("Hello and welcome to the vending machine.")
        print("\nThis machine accepts the following Notes: ")
        print(Notes.get_valid_cash_instances())  
        print("This machine accepts the following Coins: ")
        print(Coins.get_valid_cash_instances())          
        print("\n\nWe hope you'll find the snack you're looking for!")

    def get_stock(self):
        """
        Gets the stock from the csv file and adds it to item dictionary attribute. 
        A similiar attribute called chosen item dictionary, which stores the quantity of each item purchased by the user.
        """
        number = 0
        letter = "A"
        f = open(self.__stock_file, "r")
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
            self.__items_dictionary[code] = Item(name,price,quantity)
            self.__chosen_items_dictionary[code] = Item(name,price,0)
            number += 1

    def display_stock(self):
        """
        Loops through every product by its product code and outputs it to the terminal
        """
        for product_code,product_item in self.__items_dictionary.items():
            print(product_code+":"+repr(product_item))
        print('\n')

    def choose_items(self):        
        """
        Validates the user's selection, printing a message if there selection isn't valid or is out of stock
        """
        while True:
            #keep asking the user until they dont want anything else
            code = input("Please enter the product code for the item you would like to enter. (Enter 'STOP' to pay for your items)\n")
            code = code.upper()
            if code == 'STOP':
                break
            if code in self.__items_dictionary:
                #check stock to see whether its available
                if self.__chosen_items_dictionary[code]>=self.__items_dictionary[code]:
                    print("We're sorry, but there isn't anymore "+str(self.__chosen_items_dictionary[code]))
                    #restarts the loop from the top 
                    continue
                self.__chosen_items_dictionary[code].update_quantity(1)
                item = self.__items_dictionary[code]
                self.__chosen=True
                #total price is appended to after every selection
                self.__total_price += item.get_price_pennies()
            else:
                print("That isn't a valid selection")
        if self.__chosen:
            print("\nThat will be £{:.2f}".format(float(self.__total_price/100)))
            self.take_payment()

    def take_payment(self):
        """
        Takes the payment from the user. It ensures the user enters a valid coin/note amount and displays any change they have.
        """
        #loops until user can no longer pay by notes
        coins = False
        try:
            while self.__money_inserted < self.__total_price and (self.__total_price-self.__money_inserted)>=min(Notes.get_valid_cash_pennies()):
                # /100 as they're both stored in pennies so they can be integers as floats cause issues
                print(f"\nYou have £{(self.__total_price-self.__money_inserted)/100:.2f} left to pay.You've inserted £{self.__money_inserted/100:.2f} into the machine so far.")
                #this loop ensures the user can enter a new cash amount in if their previous cash amount wasnt valid
                while True:
                    try:
                        money_to_insert = input("Please insert your notes now. (Enter Coins if you would like to start inserting coins).\n")
                        if str(money_to_insert).upper()  == 'COINS':
                            #  or str(money_to_insert) == 'Coins' or str(money_to_insert) == 'coins':
                            coins = True
                            raise StopIteration
                        self.insert_money(notes=float(money_to_insert))
                    except ValueError as error:
                        #value error occurs when the note entered is invalid
                        print("That isn't a valid note!")    
                        print("This machine accepts the following notes: ")
                        print(Notes.get_valid_cash_instances())                           
                    #break out of the inner loop if the note inserted was valid     
                    else:
                        break      
                if coins == True:
                    break
        except StopIteration:
            print("\n")


        #loops until user has paid the full amount
        while self.__money_inserted < self.__total_price:
            print(f"\nYou have £{(self.__total_price-self.__money_inserted)/100:.2f} left to pay. You've inserted £{self.__money_inserted/100:.2f} into the machine so far.")
            while True:
                try:
                    money_to_insert = float(input("Please insert your coins now: "))
                    self.insert_money(coins=money_to_insert)
                except ValueError as error:
                    #value error occurs when the coin entered is invalid
                    print("That isn't a valid coin!")
                    print("This machine accepts the following coins: ")
                    print(Coins.get_valid_cash_instances())                           
                #break out of the inner loop if the coin inserted was valid     
                else:
                    break                  
        itemsString = ""
        for code in self.__chosen_items_dictionary:
            if self.__chosen_items_dictionary[code].get_quantity()>0:
                itemsString += str(self.__chosen_items_dictionary[code])+" x "+str(self.__chosen_items_dictionary[code].get_quantity())+ " "        
        
        print(f"Thank you! Please take your items:")
        print(itemsString)
        coins,notes = self.get_change()        
        if notes:
            print("Here's your notes:")    
            print(notes)
        if coins:
            print("Here's your coins:")
            print(coins)            


    def update_stock(self):
        """
        This is called after the user has payed for their items. It updates the csv file with the new amounts.
        """
        #here take quantity of selected stock away from self.__items_dictionary. Then write the dictionary back into the csv file
        csvfile = ""
        for code in self.__items_dictionary:
            #takes the quantity of each item chosen away from the total quantity of that item
            self.__items_dictionary[code] -= self.__chosen_items_dictionary[code]
            csvfile+=self.__items_dictionary[code].get_summary()+'\n'
        f = open(self.__stock_file, "w")
        f.write(csvfile)
        f.close()
        print("The vending machine stock has been updated")

    def insert_money(self, notes=None, coins=None):
        """
        Checks if the cash is a valid amount and updates the money inserted if so.
        """
        
        if notes:
            #a value error will be returned if the cash parameter is invalid
            Notes(notes)
            self.__money_inserted +=int(notes*100)

        if coins:
            #a value error will be returned if the cash parameter is invalid
            Coins(coins)
            self.__money_inserted +=int(coins*100)

    def get_change(self):
        """
        Returns change representing positive balance. The largest
        denominations are always used first.
        """
        money_inserted = self.__money_inserted
        price = self.__total_price
        change = money_inserted-price
        #checking if change >=0 caused a bug when 1p coins were used

        notes = []
        while change >= min(Notes.get_valid_cash_pennies()):
            for cash_amount in reversed(Notes.get_valid_cash_pennies()):
                # print("change - "+str(change)+" cash amount - "+str(cash_amount))
                if change >= cash_amount:
                    # Create a cash instance to display user's change
                    cash_object = Notes(cash_amount/100)
                    notes.append(cash_object)                 
                    change -= cash_amount
                    break

        coins = []
        while change >= min(Coins.get_valid_cash_pennies()):
            for cash_amount in reversed(Coins.get_valid_cash_pennies()):
                # print("change - "+str(change)+" cash amount - "+str(cash_amount))
                if change >= cash_amount:
                    # Create a cash instance to display user's change
                    cash_object = Coins(cash_amount/100)
                    coins.append(cash_object)                 
                    change -= cash_amount
                    break
        return coins,notes      

#creates an instance of the vending nachine class
machine = VendingMachine()