class Item:
    def __init__(self, code, name, price):
        # creates an item and assigns the attributes to the instance of the item
        self.code = code
        self.name = name
        self.price = price

items = []

number = 0
letter = "A"
f = open("items.txt", "r")
#loop through every line in the text file
for line in f:
    #change letter every 10 lines and reset number to 0
    if(number>9):
        letter = chr(ord(letter+1))
        number = 0
    code = letter+str(number)
    #text file format: item_name,item_price
    lineArray = line.split(",")
    name = lineArray[0]
    price = lineArray[1]
    items.append(Item(code,name,price))
    

    number +=1
    # print(item)
    # print(price)

print(items)

# Item("A1","Tea", 0.50),
# Item("Coffee", 1.00),
# Item("Coke", 1.50),
# Item("Orange Juice", 1.00)
