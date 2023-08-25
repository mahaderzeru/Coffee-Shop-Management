import sqlite3

conn = sqlite3.connect('coffee_shop.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL
    )''')
conn.commit()

def add_menu_item(name, price):
    cursor.execute('INSERT INTO menu_items (name, price) VALUES (?, ?)', (name, price))
    conn.commit()

def get_menu():
    cursor.execute('SELECT * FROM menu_items')
    return cursor.fetchall()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
''')
conn.commit()

def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    print("Registration successful!")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    
    if user:
        print("Login successful!")
        return True  # Return True to indicate successful login
    else:
        print("Login failed. Please check your username and password.")
        return False  # Return False to indicate failed login

# User-input based menu
while True:
    print("\nHi! Are you logging in or registering a new user?")
    print("1. Logging In")
    print("2. Registering a New User")
    print("3. Exit")
    
    user_auth = input("Enter your choice: ")
    
    if user_auth == '1':
        if login():
            break  # Exit the user authentication loop after successful login
    elif user_auth == '2':
        register_user()
    elif user_auth == '3':
        print("Exiting program.")
        exit()
    else:
        print("Invalid choice. Please choose a valid option.")

# Main menu - Only accessible after successful login
while True:
    print("\nWelcome User!\nWhat would you like to do? (enter 1, 2, or 3)")
    print("1. View my Menu")
    print("2. Add a Menu Item")
    print("3. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        menu = get_menu()
        print("\nMenu:")
        for item in menu:
            print(f"{item[0]}. {item[1]} - ${item[2]}")
    elif choice == '2':
        menu_items = int(input("How many menu items are you adding today? "))
        for i in range(menu_items):
            name = input("Enter menu item name: ")
            price = float(input("Enter price: "))
            add_menu_item(name, price)
            print(f"{name} added to the menu!")
    elif choice == '3':
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please choose a valid option.")

conn.close()