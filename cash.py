from abc import ABC, abstractmethod

class Cash(ABC):
    #Constant in the class that defines the values the instances could be
    VALID_CASH = []

    #this makes the class abstract
    @abstractmethod
    def __init__(self, value=None):
        """
        Create an instance of the cash class. Initialises attributes and calls relevant methods.
        """    
        value = float(value)
        if value in self.VALID_CASH:
            self.pence = int(value*100)
            self.pounds = value
        else:
            raise ValueError(str(value)+" isn't a valid value")

    def __str__(self):      
        """
        Defines behaviour when an instance of the class is converted to a string
        """  
        return f'£{self.pounds:,.2f}'        

    def __repr__(self):
        """
        Defines how an instance of the class is represented
        """
        return f'{self.pounds:,.2f}'        

    def __add__(self, other):
        """
        Defines behaviour when two instances of the coin class are added together
        """
        return self.pence + other

    def __sub__(self,other):
        return self.pence - other

    def __eq__(self, other):
        """
        Defines behaviour when two instances of the class are compared against each other
        """
        return self.pence == other

    def __le__(self,other):
        """
        Defines the behaviour when comparing an instance of the class againt an integer
        """
        return self.pence <= other

    def __hash__(self):
        return self.pence

    def get_pound_value(self):
        return self.pounds
   
    def get_penny_value(self):
        return self.pence

    @classmethod
    #class methods are called on the class itself rather than an instance of the class
    def get_valid_cash_pounds(self):
        """
        Returns the float values of the accepted cash
        """
        return self.VALID_CASH

    @classmethod
    def get_valid_cash_pennies(self):
        """
        Returns integer values of the accepted cash in pennies.
        """
        pounds = []
        for cash in self.VALID_CASH:
            pounds.append(int(cash*100))
        return pounds


    @classmethod
    def get_valid_cash_instances(self):
        """
        Returns valid instances of the cash class
        """
        return

class Notes(Cash):
    VALID_CASH = [
       5,10,20,50
    ]
    def __init__(self,value=None):
        super().__init__(value)

    def __repr__(self):
        #defines how an instance of a class is represented        
        return f'£{self.pounds:,.2f} Note'               
        
    @classmethod
    def get_valid_cash_instances(self):
        instances = []
        for notes in self.VALID_CASH:
            instances.append(Notes(notes))
        return instances

class Coins(Cash):
    VALID_CASH = [0.01,0.02,0.05,0.10,0.20,0.50,1,2]

    def __init__(self,value=None):
        super().__init__(value)

    def __repr__(self):
        #defines how an instance of a class is represented
        return f'£{self.pounds:,.2f} Coin'               

    def __str__(self):
        if (self.pounds<1):
            return f'{(self.pence):,.0f}p'
        else:
            return f'£{self.pounds:,.2f}' 

    @classmethod
    def get_valid_cash_instances(self):
        instances = []
        for coins in self.VALID_CASH:
            instances.append(Coins(coins))
        return instances