class Item:
    #all prices are in pence as storing floats causes issues
    def __init__(self, name, price, quantity):
        """
        Create an instance of the item class. Initialises attributes and calls relevant methods.
        """
        #double underscore ensures that the attributes are private, meaning they cannot be accessed or modified from outside the class
        self.__name = name
        self.__stored_price = int(float(price)*100)          
        self.__display_price = "£{:.2f}".format(float(price))
        self.__quantity = int(quantity)

    def __repr__(self):
        """
        Defines how an item is represented
        """
        string =  self.__name+" - "+self.__display_price+" x "+str(self.__quantity)
        return string     

    def __str__(self):
        """
        Defines how an item is represented when converted to a string
        """
        return self.__name

    def __eq__(self, other):
        """
        Defines behaviour when two instances of the class are compared against each other
        """
        return self.__name == other   

    def __sub__(self,other) :
        """
        Defines behaviour when two instances of the class are subtracted from each other
        """
        self.__quantity -= other.get_quantity()
        return self

    def __add__(self,other) :
        """
        Defines behaviour when two instances of the class are added together
        """
        self.__quantity += other.get_quantity()
        return self        

    def __lt__(self, other):
        """
        Compares whether one instance of the item class is less than the other
        """
        return self.__quantity < other.get_quantity()

    def __gt__(self, other):
        """
        Compares whether one instance of the item class is greater than the other
        """
        print(repr(self))
        print(other)
        return self.__quantity > other.get_quantity()

    def __le__(self, other):
        """
        Compares whether one instance of the item class is less than or equal to the other
        """
        return self.__quantity <= other.get_quantity()

    def __ge__(self, other):
        """
        Compares whether one instance of the item class is greater than or equal to the other
        """
        return self.__quantity >= other.get_quantity()    

    def get_summary(self):
        """
        Used to update csv file
        """
        string =  self.__name+","+str(float(self.__stored_price)/100)+","+str(self.__quantity)
        return string     

    def get_price_pennies(self):
        return self.__stored_price

    def get_price_pounds(self):
        return self.__display_price

    def get_quantity(self):
        return self.__quantity

    def update_quantity(self, change):
        if self.__quantity+change <0:
            raise ValueError("Quantity cannot be negative")
        else:
            self.__quantity += change