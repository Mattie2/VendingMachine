from abc import abstractmethod, abstractproperty
# from typing_extensions import Self
from unicodedata import name
import weakref
from abc import ABC, abstractmethod


class Cash(ABC):
    #create a classp property
    static valid_cash = []

    #this makes the class abstract
    @abstractmethod
    def __init__(self, value=None):
        # self.__class__.valid_cash.append(weakref.proxy(self))
        # self.__class__.valid_cash.append(self)
        self.value = value

    def __repr__(self):
        #defines how an instance of a class is represented
        return f'{self.value:,.2f}'        

    def __add__(self, other):
        #defines behaviour when two instances of the coin class are added together
        return self.value + other

    def __eq__(self, other):
        #defines behaviour when two instances of the class are compared against each other
        # return self.value == other.value
        return self.value == other
   
    @classmethod
    #class methods are called on the class itself rather than an instance of the class
    def get_valid_cash(self):
        #returns the float values of the accepted cash
        return self.valid_cash

    @classmethod
    def get_valid_cash_instances(self):
        #returns valid instances of the cash class
        valid_cash = []
        for cash in self.valid_cash:
            valid_cash.append(Cash(cash))
        return valid_cash

class Notes(Cash):
    VALID_NOTES = [
       5.00,10.00,20.00,50.00
    ]
    def __init__(self, width,height,value=None):
        super().__init__(value)
        self.width = width
        self.height = height

    def __str__(self):        
        return f'£{self.value:,.2f}'
        
class Coins(Cash):
    VALID_COINS = []
    def __str__(self):
        if (self.value<1):
            return f'{(self.value*100):,.0f}p'
        else:
            return f'£{self.value:,.2f}' 
