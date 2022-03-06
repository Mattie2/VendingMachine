from cash import Coins,Notes
from item import Item
from colour import Colour
from sys import exit
from getpass import getpass

class VendingMachine:
    def __init__(self, parameter=None, stock_file="items.csv",coins_file="coins.csv",notes_file="notes.csv"):
        """
        Create an instance of the vending machine class. Initialises attributes and calls relevant methods.
        """
        #double underscore ensures all of the attributes are private
        self.__stock_file = stock_file
        self.__notes_file = notes_file
        self.__coins_file = coins_file
        self.__items_dictionary,self.__chosen_items_dictionary = self.get_stock()
        self.__notes_dictionary,self.__inserted_notes_dictionary = self.get_notes()
        self.__coins_dictionary,self.__inserted_coins_dictionary = self.get_coins()
        if parameter=="ADMIN":
            self.__admin_password = "adminpassword123"
            self.admin_login()
            self.admin_menu()
        else:            
            self.__chosen = False
            #these are integers - cash values stored as integers
            self.__money_inserted = 0
            self.__total_price = 0
            self.welcome_message()
            self.display_stock()
            self.choose_items()
            if self.__chosen == True:
                self.update_stock("customer")

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
        items_dictionary={}
        chosen_items={}
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
            items_dictionary[code] = Item(name,price,quantity)
            chosen_items[code] = Item(name,price,0)
            number += 1
        return items_dictionary,chosen_items

    def get_notes(self):
        """
        Gets the notes from the csv file and adds it to notes dictionary attribute. 
        A similiar attribute called chosen item dictionary, which stores the quantity of each item purchased by the user.
        """
        notes_dictionary={}
        inserted_notes_dictionary={}
        f = open(self.__notes_file, "r")
        # loop through every line in the text file
        for line in f:
            # removes any line breaks
            line = line.replace("\n", "")            
            # csv file format: value,quantity
            line_array = line.split(",")
            value = line_array[0]
            quantity = int(line_array[1])     
            notes_dictionary[Notes(value)] = quantity
            inserted_notes_dictionary[Notes(value)] = 0
        return notes_dictionary,inserted_notes_dictionary

    def get_coins(self):
        """
        Gets the coins from the csv file and adds it to coins dictionary attribute. 
        A similiar attribute called chosen item dictionary, which stores the quantity of each item purchased by the user.
        """
        coins_dictionary={}
        inserted_coins_dictionary={}
        f = open(self.__coins_file, "r")
        # loop through every line in the text file
        for line in f:
            # removes any line breaks
            line = line.replace("\n", "")            
            # csv file format: value,quantity
            line_array = line.split(",")
            value = line_array[0]
            quantity = int(line_array[1])     
            coins_dictionary[Coins(value)] = quantity
            inserted_coins_dictionary[Coins(value)] = 0
        return coins_dictionary,inserted_coins_dictionary

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
            code = input("Please enter the product code for the item you would like to enter. (Enter '"+Colour.BOLD+"STOP"+Colour.END+"' to pay for your items)\n")
            code = code.upper()
            if code == 'STOP':
                break
            if code in self.__items_dictionary:
                #check stock to see whether its available
                if self.__chosen_items_dictionary[code]>=self.__items_dictionary[code]:
                    print(Colour.BOLD+"We're sorry, but there isn't anymore "+str(self.__chosen_items_dictionary[code])+""+Colour.END)
                    #restarts the loop from the top 
                    continue
                self.__chosen_items_dictionary[code].update_quantity(1)
                item = self.__items_dictionary[code]
                self.__chosen=True
                #total price is appended to after every selection
                self.__total_price += item.get_price_pennies()
            else:
                print("\n"+Colour.RED+"That isn't a valid selection"+Colour.END+"\n")
        if self.__chosen:
            print("\n{}That will be £{:.2f}{}".format(Colour.BOLD,float(self.__total_price/100),Colour.END))
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
                print(f"\nYou have {Colour.RED}£{(self.__total_price-self.__money_inserted)/100:.2f} {Colour.END}left to pay.You've inserted {Colour.GREEN}£{self.__money_inserted/100:.2f}{Colour.END} into the machine so far.")
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
                        print("\n"+Colour.RED+"That isn't a valid note!"+Colour.END)    
                        print("This machine accepts the following notes: ")
                        print(Notes.get_valid_cash_instances())
                        print("\n")                           
                    #break out of the inner loop if the note inserted was valid     
                    else:
                        break      
                if coins == True:
                    break
        except StopIteration:
            print("\n")

        #loops until user has paid the full amount
        while self.__money_inserted < self.__total_price:
            print(f"\nYou have {Colour.RED}£{(self.__total_price-self.__money_inserted)/100:.2f}{Colour.END} left to pay. You've inserted {Colour.GREEN}£{self.__money_inserted/100:.2f}{Colour.END} into the machine so far.")
            while True:
                try:
                    money_to_insert = float(input("Please insert your coins now: "))
                    self.insert_money(coins=money_to_insert)
                except ValueError as error:
                    #value error occurs when the coin entered is invalid
                    print("\n"+Colour.RED+"That isn't a valid coin!"+Colour.END)    
                    print("This machine accepts the following coins: ")
                    print(Coins.get_valid_cash_instances())
                    print("\n")                           
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

    def insert_money(self, notes=None, coins=None):
        """
        Checks if the cash is a valid amount and updates the money inserted if so.
        """
        
        if notes:
            #a value error will be returned if the cash parameter is invalid
            note = Notes(notes)
            self.__notes_dictionary[note]+=1
            self.__money_inserted +=int(notes*100)

        if coins:
            #a value error will be returned if the cash parameter is invalid
            #check if this works
            coin=Coins(coins)
            self.__coins_dictionary[coin]+=1
            self.__money_inserted +=int(coins*100)

    def get_change(self):
        """
        Returns change representing positive balance. The largest
        denominations are always used first.
        """
        money_inserted = self.__money_inserted
        price = self.__total_price
        change = money_inserted-price

        notes = []
        stop =False
        while change >= min(Notes.get_valid_cash_pennies())and stop ==False:
            # for cash_amount in reversed(Notes.get_valid_cash_pennies()):
            for cash_object,quantity in reversed(self.__notes_dictionary.items()):
                # if change >= cash_amount:
                if cash_object<=change and quantity>0:
                    # Create a cash instance to display user's change
                    # cash_object = Notes(cash_amount/100)
                    notes.append(cash_object)                 
                    # change -= cash_amount
                    self.__notes_dictionary[cash_object]-=1
                    change -=cash_object.get_penny_value()
                    break
                elif quantity==0:
                    if cash_object==Notes.get_valid_cash_pennies()[0]:
                        stop=True
                        break

        #update the coin csv here
        csvfile = ""
        for note,quantity in self.__notes_dictionary.items():
            csvfile+="{},{}\n".format(note.get_pound_value(),quantity)
        f = open(self.__notes_file,"w")
        f.write(csvfile)
        f.close()  

        coins = []
        stop=False
        while change >= min(Coins.get_valid_cash_pennies()) and stop == False:
            for cash_object,quantity in reversed(self.__coins_dictionary.items()):           
                if cash_object<=change and quantity>0:
                    coins.append(cash_object)
                    self.__coins_dictionary[cash_object]-=1
                    change -=cash_object.get_penny_value()
                    break
                elif quantity==0:
                    #if there's no more change, and it's down to 1p
                    if cash_object==Coins.get_valid_cash_pennies()[0]:
                        if not coins:
                            print("\n"+Colour.YELLOW+"We are very sorry, but we have no change to give you."+Colour.END+"\n")
                        else:
                            print("\n"+Colour.YELLOW+"We're sorry but we don't have enough coins to give you the full change"+Colour.END+"\n")
                        stop=True
                        break
            
        #update the coin csv here
        csvfile = ""
        for coin,quantity in self.__coins_dictionary.items():
            csvfile+="{},{}\n".format(coin.get_pound_value(),quantity)
        f = open(self.__coins_file,"w")
        f.write(csvfile)
        f.close()                

        return coins,notes      

    def update_stock(self,user):
        """
        This is called after the user has payed for their items. It updates the csv file with the new amounts.
        """
        #here take quantity of selected stock away from self.__items_dictionary. Then write the dictionary back into the csv file
        csvfile = ""
        if user=="customer":
            for code in self.__items_dictionary:
                #takes the quantity of each item chosen away from the total quantity of that item
                self.__items_dictionary[code] -= self.__chosen_items_dictionary[code]
                csvfile+=self.__items_dictionary[code].get_summary()+'\n'
        elif user=="admin":
            for code in self.__items_dictionary:
                #adds each item to total
                self.__items_dictionary[code] += self.__chosen_items_dictionary[code]
                csvfile+=self.__items_dictionary[code].get_summary()+'\n'      
            #resets chosen dictionary back to 0
            for code in self.__chosen_items_dictionary:
                quantity=self.__chosen_items_dictionary[code].get_quantity()
                self.__chosen_items_dictionary[code].update_quantity(-quantity)
                      
        f = open(self.__stock_file, "w")
        f.write(csvfile)
        f.close()
        print("The vending machine stock has been updated")        

    def admin_login(self):
        """
        Displays a welcome message to the administrator, asking them to enter a password before they can continue.
        """
        print("Hello, and welcome to the administrator page!")
        valid_password = False
        password = getpass("Please enter the administrator password to continue:")
        retryCount=0      
        if password==self.__admin_password:
            valid_password=True
        while valid_password==False:
            retryCount+=1
            password=getpass(Colour.RED+"Invalid password entered.\n"+Colour.END+"Please retry or enter 'EXIT' to quit:")
            if password.upper()=="EXIT":
                print(Colour.BOLD+"Exiting program"+Colour.END)
                exit(1)
            elif retryCount==3:
                print(Colour.BOLD+"Too many failed password attempts, terminating session!"+Colour.END)
                exit(0)
            elif password==self.__admin_password:
                valid_password=True
    
    def admin_menu(self):
        while True:
            choice = input("Enter 1 to refill stock.\nEnter 2 to refill notes.\nEnter 3 to refill coins.\n")
            if choice == '1':
                self.refill_stock()
            elif choice == '2':
                self.refill_notes()
            elif choice == '3':
                self.refill_coins()
            else:
                print(Colour.RED+""+str(choice)+" isn't a valid choice, please retry."+Colour.END)

    def refill_stock(self):
        print("The stock is as follows:")
        self.display_stock()
        #loop round, asking admin to enter the amount of each they have added to the vending machine
        while True:
            #keep asking the user until they dont want anything else
            refill = input("Please enter the product code for the item you would like to refill, followed by the amount you have added. For example, A0,5\n(Enter "+Colour.BOLD+"STOP"+Colour.END+" when you have finished restocking the machine.)\n")            
            if refill == 'STOP' or refill=='Stop' or refill=='stop':
                break
            try:
                int(refill.split(",")[1])
            except:
                #makes text bold
                print(Colour.RED+"\nInvalid format. Please retry.\n"+Colour.END)
                continue
            code=refill.split(",")[0].upper()
            amount=int(refill.split(",")[1])
            if code in self.__items_dictionary:
                #check stock to see whether its available
                self.__chosen_items_dictionary[code].update_quantity(amount)
                self.update_stock("admin")
                print("\nThe new stock levels are:")
                self.display_stock()
            else:
                print("\n"+Colour.RED+"That isn't a valid selection"+Colour.END+"\n")

        menu = input("Please enter "+Colour.BOLD+"RETURN"+Colour.END+" to go back to the menu. If not you will exit the program. ")
        if menu.upper()!="RETURN":
            print("Thank you for refilling this vending machine's stock.")
            exit(0)

    def display_notes_quantities(self):
        for product_code,product_item in self.__notes_dictionary.items():
            print("{} x {}".format(product_code,product_item))
        print('\n')

    def display_coins_quantities(self):
        for product_code,product_item in self.__coins_dictionary.items():
            print("{} x {}".format(product_code,product_item))
        print('\n')

    def refill_notes(self):
        csvfile=""
        print("\nHere is the current amount of notes:")
        self.display_notes_quantities()

        while True:
            #keep asking the user until they dont want anything else
            refill = input("Please enter the value of the coin you would like to refill, followed by the amount you have added. For example, 5,5\n(Enter '"+Colour.BOLD+"STOP"+Colour.END+"' when you have finished restocking the machine.)\n")            
            if refill == 'STOP' or refill=='Stop' or refill=='stop':
                break
            try:
                int(refill.split(",")[1])
            except:
                print(Colour.RED+"\nInvalid format. Please retry.\n"+Colour.END)
                continue
            try:
                note=Notes(refill.split(",")[0])
            except:
                print("\n"+Colour.RED+"Invalid note, try again."+Colour.END+"\n")
                continue
            amount=int(refill.split(",")[1])
            self.__inserted_notes_dictionary[note]+=amount

            for note, quantity in self.__notes_dictionary.items():
                #updates inserted dictionary
                self.__notes_dictionary[note] += self.__inserted_notes_dictionary[note]
                csvfile+=("{},{}\n".format(note.get_pound_value(),self.__notes_dictionary[note]))
                #resets inserted dictionary back to 0
                self.__inserted_notes_dictionary[note]=0     
                

            f = open(self.__notes_file, "w")
            f.write(csvfile)
            f.close()

            #resetting the csv file
            csvfile=""

            print("\nThe new stock levels are:")
            self.display_notes_quantities()

        menu = input("Please enter "+Colour.BOLD+"RETURN"+Colour.END+" to go back to the menu. If not you will exit the program. ")
        if menu.upper()!="RETURN":
            print("Thank you for refilling this vending machine's cash")
            exit(0)

    def refill_coins(self):
        csvfile=""
        print("\nHere is the current amount of coins:")
        self.display_coins_quantities()

        while True:
            #keep asking the user until they dont want anything else
            refill = input("Please enter the value of the coin you would like to refill, followed by the amount you have added. For example, 0.01,5\n(Enter '"+Colour.BOLD+"STOP"+Colour.END+"' when you have finished restocking the machine.)\n")            
            if refill == 'STOP' or refill=='Stop' or refill=='stop':
                break
            try:
                int(refill.split(",")[1])
            except:
                print(Colour.RED+"\nInvalid format. Please retry.\n"+Colour.END)
                continue
            try:
                coin=Coins(refill.split(",")[0])
            except:
                print("\n"+Colour.RED+"Invalid coin, try again."+Colour.END+"\n")
                continue
            amount=int(refill.split(",")[1])
            #DOES THIS UPDATE THE KEY OR VALUE?
            self.__inserted_coins_dictionary[coin]+=amount

            for coin, quantity in self.__coins_dictionary.items():
                #updates inserted dictionary
                self.__coins_dictionary[coin] += self.__inserted_coins_dictionary[coin]
                csvfile+=("{},{}\n".format(coin.get_pound_value(),self.__coins_dictionary[coin]))
                #resets inserted dictionary back to 0
                self.__inserted_coins_dictionary[coin]=0     

            f = open(self.__coins_file, "w")
            
            f.write(csvfile)
            f.close()

            csvfile=""

            print("\nThe new stock levels are:")
            self.display_coins_quantities()

        menu = input("Please enter "+Colour.BOLD+"RETURN"+Colour.END+" to go back to the menu. If not you will exit the program. ")
        if menu.upper()!="RETURN":
            print("Thank you for refilling this vending machine's cash")
            exit(0)