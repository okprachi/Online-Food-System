import sqlite3
from sqlite3 import Error
from datetime import datetime

def get_db_connection():
    try:
        return sqlite3.connect('food_ordering.db')
    except Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None

def create_database_and_tables():
    conn = get_db_connection()
    if conn is None:
        return
    
    with conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL CHECK(price > 0)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                food_item_id INTEGER,
                quantity INTEGER CHECK(quantity > 0),
                total_price REAL,
                order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                payment_method TEXT CHECK(payment_method IN ('cash', 'card', 'upi')),
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (food_item_id) REFERENCES food_items(id)
            )
        ''')
    
    print("Database and tables created successfully.")

def recreate_customers_table():
    conn = get_db_connection()
    if conn is None:
        return
    
    with conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS customers')  # Drop the old table
        cursor.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number TEXT,
                email TEXT
            )
        ''')
    
    print("Customers table recreated successfully.")

def execute_query(query, params=()):
    """Executes a query with parameters and returns the cursor."""
    conn = get_db_connection()
    if conn is None:
        return None
    
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor, conn

def add_customer(name, phone_number, email):
    """Adds a new customer to the database."""
    query = 'INSERT INTO customers (name, phone_number, email) VALUES (?, ?, ?)'
    cursor, conn = execute_query(query, (name, phone_number, email))
    
    if cursor:
        conn.commit()
        print(f'Added customer: {name}')
        cursor.close()
        conn.close()

def view_customers():
    """Displays all customers in the database."""
    cursor, conn = execute_query('SELECT * FROM customers')
    
    if cursor:
        print("\nCustomer List:")
        for customer in cursor.fetchall():
            print(f'ID: {customer[0]}, Name: {customer[1]}, Phone: {customer[2]}, Email: {customer[3]}')
        
        cursor.close()
        conn.close()

def add_food_item(name, price):
    """Adds a new food item to the database."""
    query = 'INSERT INTO food_items (name, price) VALUES (?, ?)'
    cursor, conn = execute_query(query, (name, price))
    
    if cursor:
        conn.commit()
        print(f'Added food item: {name} at ${price:.2f}')
        cursor.close()
        conn.close()

def view_food_items():
    """Displays all food items in the database."""
    cursor, conn = execute_query('SELECT * FROM food_items')
    
    if cursor:
        print("\nFood Menu:")
        for item in cursor.fetchall():
            print(f'ID: {item[0]}, Name: {item[1]}, Price: ${item[2]:.2f}')
        
        cursor.close()
        conn.close()

def place_order(customer_id, food_item_id, quantity):
    """Places an order for a food item."""
    
    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return
    
    payment_method = input("Choose payment method (cash/card/UPI): ").strip().lower()
    
    if payment_method not in ['cash', 'card', 'upi']:
         print("Invalid payment method. Please choose cash, card, or UPI.")
         return
    
    query = 'SELECT price FROM food_items WHERE id = ?'
    cursor, conn = execute_query(query, (food_item_id,))
    
    if cursor:
         result = cursor.fetchone()
         
         if result:
             price = result[0]
             total_price = price * quantity
             
             insert_order_query = '''
                 INSERT INTO orders (customer_id, food_item_id, quantity, total_price, payment_method)
                 VALUES (?, ?, ?, ?, ?)
             '''
             execute_query(insert_order_query, (customer_id, food_item_id, quantity, total_price, payment_method))
             conn.commit()
             
             order_id = cursor.lastrowid  
             print(f'Order placed! Total price: ${total_price:.2f}')
             
             print_receipt(order_id)
             
             view_orders()
         else:
             print("Invalid food item ID.")
             
         cursor.close()
         conn.close()

def print_receipt(order_id):
     """Prints a receipt for the order."""
     
     query = '''
         SELECT o.id AS order_id, c.name AS customer_name, f.name AS food_item_name,
                o.quantity, o.total_price, o.order_time 
         FROM orders o 
         JOIN customers c ON o.customer_id = c.id 
         JOIN food_items f ON o.food_item_id = f.id 
         WHERE o.id = ?
     '''
     cursor, conn = execute_query(query, (order_id,))
     
     if cursor:
          order_details = cursor.fetchone()

          if order_details:
              print("\n--- Receipt ---")
              print(f"Order ID: {order_details[0]}")
              print(f"Customer Name: {order_details[1]}")
              print(f"Food Item: {order_details[2]}")
              print(f"Quantity: {order_details[3]}")
              print(f"Total Price: ${order_details[4]:.2f}")
              print(f"Order Time: {order_details[5]}")
              print("----------------")
              
          cursor.close()
          conn.close()

def view_orders():
     
     query = '''
         SELECT o.id AS order_id, c.name AS customer_name, f.name AS food_item_name,
                o.quantity, o.total_price, o.order_time 
         FROM orders o 
         JOIN customers c ON o.customer_id = c.id 
         JOIN food_items f ON o.food_item_id = f.id
     '''
     cursor, conn = execute_query(query)
     
     if cursor:
          orders = cursor.fetchall()

          print("\nOrder History:")
          for order in orders:
              print(f'Order ID: {order[0]}, Customer: {order[1]}, Food Item: {order[2]}, '
                    f'Quantity: {order[3]}, Total Price: ${order[4]:.2f}, Order Time: {order[5]}')
              
          cursor.close()
          conn.close()

def main():
    create_database_and_tables()   
    recreate_customers_table()  # Ensure the customers table is updated
    
    while True:
        print("\nOnline Food Ordering System")
        options = {
            '1': "Add Customer",
            '2': "View Customers",
            '3': "Add Food Item",
            '4': "View Food Items",
            '5': "Place Order",
            '6': "View Orders",
            '7': "Exit"
        }
        
        for key in options:
            print(f"{key}. {options[key]}")

        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter name: ")
            phone_number = input("Enter phone number: ")
            email = input("Enter email address: ")
            add_customer(name.strip(), phone_number.strip(), email.strip())

        elif choice == '2':
            view_customers()

        elif choice == '3':
            name = input("Enter food item name: ")
            try:
                price = float(input("Enter food item price: "))
                add_food_item(name.strip(), price)
            except ValueError:
                print("Invalid price entered. Please enter a numeric value.")

        elif choice == '4':
            view_food_items()

        elif choice == '5':
            view_customers()  
            try:
                customer_id = int(input("Enter customer ID to place an order for: "))
                view_food_items()  
                food_item_id = int(input("Enter food item ID to order: "))
                quantity = int(input("Enter quantity: "))
                place_order(customer_id, food_item_id, quantity)
            except ValueError:
                print("Invalid input. Please enter numeric values for ID and quantity.")

        elif choice == '6':
            view_orders()

        elif choice == '7':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
