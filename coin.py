
class Cash():
    def __init__(self, value):
        #maybe have valid amounts here
        self.value = value
        #return value error if not valid

    def __repr__(self):
        #defines how an instance of a class is represented
        return f'£{self.value:,.2f}'

    def __str__(self):
        #defines how the cash amount is shown when printed to the terminal
        return f'£{self.value:,.2f}'

    def __add__(self, other):
        #defines behaviour when two instances of the coin class are added together
        return self.value + other

    def __eq__(self, other):
        #defines behaviour when two instances of the class are compared against each other
        return self.value == other.value