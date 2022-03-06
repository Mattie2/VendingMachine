import sys
from VendingMachine import VendingMachine

parameter=None

try:
    parameter = sys.argv[1]
    #creates an instance of the vending nachine class
    # VendingMachine(parameter)
except IndexError:
    print()

VendingMachine(parameter)
    # VendingMachine()