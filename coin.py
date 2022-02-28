class Cash():
    VALID_CASH = [
       0.01,0.02,0.05,0.10,0.20,0.50,1.00,2.00,5.00,10.00,20.00,50.00
    ]
    def __init__(self, value):
        #ensures only valid cash amounts can be made
        if value in self.VALID_CASH:
            self.value = value
        else:
            #return value error if not valid
            raise ValueError
        
    def __repr__(self):
        #defines how an instance of a class is represented
        if (self.value<1):
            return f'{(self.value*100):,.0f}p'
        else:
            return f'£{self.value:,.2f}'        

    def __str__(self):
        #defines how the cash amount is shown when printed to the terminal
        if (self.value<1):
            return f'{(self.value*100):,.0f}p'
        else:
            return f'£{self.value:,.2f}'

    def __add__(self, other):
        #defines behaviour when two instances of the coin class are added together
        return self.value + other

    def __eq__(self, other):
        #defines behaviour when two instances of the class are compared against each other
        return self.value == other.value
    
    @classmethod
    #class methods are called on the class itself rather than an instance of the class
    def get_valid_cash(self):
        #returns the float values of the accepted cash
        return self.VALID_CASH

    @classmethod
    def get_valid_cash_instances(self):
        #returns valid instances of the cash class
        valid_cash = []
        for cash in self.VALID_CASH:
            valid_cash.append(Cash(cash))
        return valid_cash