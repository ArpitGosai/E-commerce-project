import os
#USER HANDLING FUNCTIONS
def load_users():
    users = {}
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                email, password = line.strip().split(",")
                users[email] = password
    return users


def save_users(users):
    with open("users.txt", "w") as f:
        for email, password in users.items():
            f.write(email + "," + password + "\n")


#CART HANDLING FUNCTIONS
def load_cart(email):
    filename = "cart_" + email.replace("@", "_at_") + ".txt"
    cart = {}

    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                name, price, qty = line.strip().split(",")
                cart[name] = {"price": int(price), "qty": int(qty)}
    return cart


def save_cart(email, cart):
    filename = "cart_" + email.replace("@", "_at_") + ".txt"
    with open(filename, "w") as f:
        for name, item in cart.items():
            f.write(name + "," + str(item["price"]) + "," + str(item["qty"]) + "\n")


#REGISTER USER
def register_user():
    users = load_users()
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    if email in users:
        print("User already exists!\n")
    else:
        users[email] = password
        save_users(users)
        print("Registration successful!\n")


#LOGIN USER
def login_user():
    users = load_users()
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    if email in users and users[email] == password:
        print("Login successful!\n")
        cart = load_cart(email)
        if cart:
            print("You have items left in your previous cart:")
            for name, item in cart.items():
                print("- " + str(item["qty"]) + " x " + name + " (₹" + str(item["price"]) + ")")
        shop_menu(email, cart)
    else:
        print("Invalid email or password! Please register first.\n")


#SHOP MENU
def shop_menu(email, cart):
    items = {
        1: ("Jeans", 1200),
        2: ("Shirt", 800),
        3: ("Pants", 900),
        4: ("T-Shirt", 500),
        5: ("Shorts", 400)
    }

    while True:
        print("\n===== SHOP MENU =====")
        for i, j in items.items():
            print(str(i) + ". " + j[0] + " - ₹" + str(j[1]))
        print("6. Checkout")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if not choice.isdigit():
            print("Please enter a number!")
            continue

        choice = int(choice)

        if choice in range(1, 6):
            qty = input("Enter quantity for " + items[choice][0] + ": ")
            if not qty.isdigit():
                print("Invalid quantity!")
                continue
            qty = int(qty)
            name, price = items[choice]
            if name in cart:
                cart[name]["qty"] += qty
            else:
                cart[name] = {"price": price, "qty": qty}
            save_cart(email, cart)
            print("Added " + str(qty) + " x " + name + " to cart.")

        elif choice == 6:
            checkout(email, cart)
            break

        elif choice == 7:
            print("Saving your cart and exiting shop...")
            save_cart(email, cart)
            break
        else:
            print("Invalid option! Try again.")


#CHECKOUT
def checkout(email, cart):
    if not cart:
        print("Your cart is empty!")
        return

    total = 0
    print("\n===== CHECKOUT =====")
    print("Item\tQty\tPrice\tSubtotal")
    print("-----------------------------")

    for name, item in cart.items():
        subtotal = item["qty"] * item["price"]
        total += subtotal
        print(name + "\t" + str(item["qty"]) + "\t₹" + str(item["price"]) + "\t₹" + str(subtotal))

    print("-----------------------------")
    print("Total Payable Amount: ₹" + str(total))

    pay = input("Do you want to pay now? (yes/no): ").lower()
    if pay == "yes":
        print("Payment successful! Thank you for shopping 🙌\n")
        cart.clear()
        save_cart(email, cart)
    else:
        print("Payment cancelled. Your cart is saved for later.\n")
        save_cart(email, cart)


#MAIN MENU
while True:
    print("\n==== WELCOME TO THE STORE ====")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        login_user()
    elif choice == "2":
        register_user()
    elif choice == "3":
        print("Exiting... Goodbye!")
        break
    else:
        print("Invalid choice! Try again.\n")
