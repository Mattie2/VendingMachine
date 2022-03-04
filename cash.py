from abc import ABC, abstractmethod


class Cash(ABC):
    #create a classp property
    VALID_CASH = []

    #this makes the class abstract
    @abstractmethod
    def __init__(self, value=None):
        if value in self.VALID_CASH:
            self.pence = int(value*100)
            self.pounds = value
        # for cash in self.VALID_CASH:
        #     cash = cash/100
        #     if cash == value:
        #         self.pence = int(value)            
        #         self.pounds = float(value/100)
        else:
            raise ValueError(str(value)+" isn't a valid value")

    def __str__(self):        
        return f'£{self.pounds:,.2f}'        

    def __repr__(self):
        #defines how an instance of a class is represented
        return f'{self.pounds:,.2f}'        

    def __add__(self, other):
        #defines behaviour when two instances of the coin class are added together
        return self.pence + other

    def __eq__(self, other):
        #defines behaviour when two instances of the class are compared against each other
        # return self.value == other.value
        return self.pence == other
   
    @classmethod
    #class methods are called on the class itself rather than an instance of the class
    def get_valid_cash_pounds(self):
        #returns the float values of the accepted cash
        return self.VALID_CASH

    @classmethod
    #class methods are called on the class itself rather than an instance of the class
    def get_valid_cash_pennies(self):
        #returns the float values of the accepted cash
        pounds = []
        for cash in self.VALID_CASH:
            pounds.append(int(cash*100))
        return pounds


    @classmethod
    def get_valid_cash_instances(self):
        #returns valid instances of the cash class
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

print(Notes.get_valid_cash_pounds())
print(Notes.get_valid_cash_pennies())
print(Notes.get_valid_cash_instances())