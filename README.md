# VendingMachine

# Running
Run the 'application.py' script to run the application. Add the 'ADMIN' as a parameter to run as an administrator. The password is 'adminpassword123'

# Features
Machine has csv files for stock to track stock. Admin can refill.
CSV file for coins and notes - updated with cash inserted and removed as change. Will only give users change with the coins in the machine, meaning if there's no cash left the user will not have any change, or if there's not enough of the correct change it will carr on giving change from lowe demoniation if possible e.g. 5 £1's if no £5 notes and sufficient £1's.

# Validation Features
- Password checking - kills program after 3 incorrect password attempts
- Stock checking - only allows user to buy item if it's in stock, or theres enough - e.g. if theres only 1 left the user wont be able to buy two
- Coin/cash checking - the cash and coins will be updated when the user inserts cash, and when change is given. If there is no change available, the user will be notified. If there is only part of the change available, the user will receive as much as possible, along with a message explaining the machine is low on change.
