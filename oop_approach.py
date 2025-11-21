import os

# BASE CLASS : COMMON FILE HANDLING
class FileHandler:
    def file_exists(self, filename):
        return os.path.exists(filename)

    def read_lines(self, filename):
        if not self.file_exists(filename):
            return []
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines()]

    def write_lines(self, filename, lines):
        with open(filename, "w") as f:
            for line in lines:
                f.write(line + "\n")

# USER CLASS (INHERITS FILEHANDLER)
class User(FileHandler):
    USERS_FILE = "users.txt"

    def load_users(self):
        users = {}
        #Reads users.txt line-by-line using parent class function.
        for line in self.read_lines(self.USERS_FILE):
            #Splits each line by comma.
            email, password = line.split(",")
            users[email] = password
        return users

    def save_users(self, users):
        #Converts dictionary back into list format.
        data = [f"{email},{password}" for email, password in users.items()]
        #Saves all lines into users.txt,Uses parent class write_lines().
        self.write_lines(self.USERS_FILE, data)

    def register(self):
        users = self.load_users()
        email = input("Enter Email: ")
        password = input("Enter Password: ")

        if email in users:
            print("User already exists!\n")
            return None

        users[email] = password
        self.save_users(users)
        print("Registration successful!\n")

    def login(self):
        users = self.load_users()
        email = input("Enter Email: ")
        password = input("Enter Password: ")

        if email in users and users[email] == password:
            print("Login successful!\n")
            return email
        else:
            print("Invalid email or password!\n")
            return None

# CART CLASS (INHERITS FILEHANDLER)
class Cart(FileHandler):

    def get_filename(self, email):
        return "cart_" + email.replace("@", "_at_") + ".txt"

    def load_cart(self, email):
        cart = {}
        for line in self.read_lines(self.get_filename(email)):
            name, price, qty = line.split(",")
            cart[name] = {"price": int(price), "qty": int(qty)}
        return cart

    def save_cart(self, email, cart):
        data = [
            f"{name},{item['price']},{item['qty']}"
            for name, item in cart.items()
        ]
        self.write_lines(self.get_filename(email), data)

# SHOP CLASS
class Shop:
    ITEMS = {
        1: ("Jeans", 1200),
        2: ("Shirt", 800),
        3: ("Pants", 900),
        4: ("T-Shirt", 500),
        5: ("Shorts", 400),
    }

    def __init__(self, email):
        self.email = email
        self.cart_obj = Cart() #Create a Cart object to manage cart storage.
        self.cart = self.cart_obj.load_cart(email) #loads user's saved cart from file.

    def show_menu(self):
        while True:
            print("\n===== SHOP MENU =====")
            for i, j in self.ITEMS.items():
                print(f"{i}. {j[0]} - ₹{j[1]}")
            print("6. Checkout")
            print("7. Exit")

            choice = input("Enter choice: ")

            if not choice.isdigit():
                print("Please enter a valid number!")
                continue

            choice = int(choice)

            if choice in self.ITEMS:
                self.add_item(choice)

            elif choice == 6:
                self.checkout()
                break

            elif choice == 7:
                print("Saving cart and exiting...\n")
                self.cart_obj.save_cart(self.email, self.cart)
                break

            else:
                print("Invalid option!")

    def add_item(self, choice): #→ If choice = 2
        name, price = self.ITEMS[choice] #→ name = "Shirt", price = 800
        qty = input(f"Enter quantity for {name}: ")

        if not qty.isdigit():
            print("Invalid quantity!")
            return

        qty = int(qty)

        if name in self.cart:
            self.cart[name]["qty"] += qty
        else:
            self.cart[name] = {"price": price, "qty": qty}

        self.cart_obj.save_cart(self.email, self.cart)
        print(f"Added {qty} x {name} to cart.")

    def checkout(self):
        if not self.cart:
            print("Your cart is empty!")
            return

        print("\n===== CHECKOUT =====")
        total = 0

        for name, item in self.cart.items():
            subtotal = item["price"] * item["qty"]
            total += subtotal
            print(f"{name} - {item['qty']} x ₹{item['price']} = ₹{subtotal}")

        print("-------------------------------")
        print(f"Total Amount: ₹{total}")

        pay = input("Pay now? (yes/no): ").lower()

        if pay == "yes":
            print("Payment successful!\n")
            self.cart.clear() #Clears cart.
            self.cart_obj.save_cart(self.email, self.cart) #Saves empty cart to file. 
        else:
            print("Payment saved for later.\n")
            self.cart_obj.save_cart(self.email, self.cart) #Keeps cart saved for later.

# MAIN APPLICATION
class StoreApp:
    def __init__(self):
        self.user_obj = User()

    def start(self):
        while True:
            print("\n==== WELCOME TO THE STORE ====")
            print("1. Login")
            print("2. Register")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                email = self.user_obj.login()
                if email:
                    shop = Shop(email)
                    shop.show_menu()

            elif choice == "2":
                self.user_obj.register()

            elif choice == "3":
                print("Goodbye!")
                break

            else:
                print("Invalid choice!")


# RUN APPLICATION
StoreApp().start() #Create StoreApp object,Call the start() method,Begin the program
#This is exactly like:
#app = StoreApp()
#app.start()