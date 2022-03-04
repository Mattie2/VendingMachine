class Item:
    #all prices are in pence as storing floats causes issues
    def __init__(self, name, price, quantity):
        self.name = name
        self.stored_price = int(float(price)*100)          
        self.display_price = "£{:.2f}".format(float(price))
        # if self.stored_price < 100:
        #     self.display_price = f'{(self.stored_price):,.0f}p'
        # else:
        #     price_float = float(price)
            # self.display_price = "£"+str(price_float)          
        self.quantity = int(quantity)

    def __repr__(self):
        #used to update csv file
        string =  self.name+" - "+self.display_price+" x "+str(self.quantity)
        return string     

    def __str__(self):
        #defines how the item class is formatted when printed to the screen
        return self.name

    def __eq__(self, other):
        #defines behaviour when two instances of the class are compared against each other
        return self.name == other   

    def __sub__(self,other) :
        self.quantity -= other.quantity
        return self

    def __lt__(self, other):
        #compares whether one instance of the item class is less than the other
        return self.quantity < other.quantity

    def __gt__(self, other):
        #compares whether one instance of the item class is greater than the other
        print(repr(self))
        print(other)
        return self.quantity > other.quantity

    def __le__(self, other):
        #compares whether one instance of the item class is less than or equal to the other
        return self.quantity <= other.quantity

    def __ge__(self, other):
        #compares whether one instance of the item class is greater than or equal to the other
        return self.quantity >= other.quantity    

    def get_summary(self):
        #used to update csv file
        string =  self.name+","+str(float(self.stored_price)/100)+","+str(self.quantity)
        return string     

    def get_price_pennies(self):
        return self.stored_price

    def get_price_pounds(self):
        return self.display_price

    def get_quantity(self):
        return self.quantity

    def update_quantity(self, change):
        if self.quantity+change <0:
            raise ValueError("Quantity cannot be negative")
        else:
            self.quantity += change