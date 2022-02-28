import string


class Item:
    def __init__(self, name, price, quantity):
        self.name = name
        price_float = float(price)          
        #stores as string to 2 decimal places
        price_string = "{:.2f}".format(price_float)
        if price_float < 1:
            self.display_price = f'{(price_float*100):,.0f}p'
        else:
            self.display_price = "£"+str(price_string)        
        self.stored_price = float(price)    
        self.quantity = int(quantity)

    def __repr__(self):
        string = self.name+','+str(self.stored_price)+','+str(self.quantity)
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
        string =  self.name+" - "+self.display_price+" x "+str(self.quantity)
        return string        

    def get_display_price(self):
        return self.display_price
    
    def get_stored_price(self):
        return self.stored_price

    def get_quantity(self):
        return self.quantity

    def update_quantity(self, change):
        if self.quantity+change <0:
            raise ValueError("Quantity cannot be negative")
        else:
            self.quantity += change