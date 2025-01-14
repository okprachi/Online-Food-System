import mysql.connector
from mysql.connector import Error
from datetime import datetime

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',  # replace with your MySQL username
            password='YES',  # replace with your MySQL password
            database='food_ordering'
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database_and_tables():
    """Creates the database and necessary tables if they do not exist."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # replace with your MySQL username
            password='YES'  # replace with your MySQL password
        )
        
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS food_ordering")
        
        # Use the newly created database
        cursor.execute("USE food_ordering")
        
        # Create customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                phone_number VARCHAR(20),
                email VARCHAR(255)
            )
        ''')
        
        # Create food_items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL
            )
        ''')
        
        # Create orders table with payment_method column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                food_item_id INT,
                quantity INT,
                total_price DECIMAL(10, 2),
                order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                payment_method VARCHAR(20),
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (food_item_id) REFERENCES food_items(id)
            )
        ''')
        
        print("Database and tables created successfully.")
        
    except Error as e:
        print(f"Error creating database or tables: {e}")
    finally:
        cursor.close()
        conn.close()

def add_customer(username, phone_number, email):
    """Adds a new customer to the database."""
    conn = get_db_connection()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO customers (username, phone_number, email) VALUES (%s, %s, %s)', 
                       (username, phone_number, email))
        conn.commit()
        print(f'Added customer: {username}')
    except Error as e:
        print(f"Error adding customer: {e}")
    finally:
        cursor.close()
        conn.close()

def view_customers():
    """Displays all customers in the database."""
    conn = get_db_connection()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM customers')
        customers = cursor.fetchall()

        print("\nCustomer List:")
        for customer in customers:
            print(f'ID: {customer[0]}, Username: {customer[1]}, Phone: {customer[2]}, Email: {customer[3]}')
    except Error as e:
        print(f"Error retrieving customers: {e}")
    finally:
        cursor.close()
        conn.close()

def add_food_item(name, price):
    """Adds a new food item to the database."""
    conn = get_db_connection()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO food_items (name, price) VALUES (%s, %s)', (name, price))
        conn.commit()
        print(f'Added food item: {name} at ${price:.2f}')
    except Error as e:
        print(f"Error adding food item: {e}")
    finally:
        cursor.close()
        conn.close()

def view_food_items():
    """Displays all food items in the database."""
    conn = get_db_connection()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM food_items')
        items = cursor.fetchall()

        print("\nFood Menu:")
        for item in items:
            print(f'ID: {item[0]}, Name: {item[1]}, Price: ${item[2]:.2f}')
    except Error as e:
        print(f"Error retrieving food items: {e}")
    finally:
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
    
    conn = get_db_connection()
    
    if conn is None:
         return
    
    cursor = conn.cursor()
     
    try:
         # Get the price of the food item
         cursor.execute('SELECT price FROM food_items WHERE id = %s', (food_item_id,))
         
         result = cursor.fetchone()
         
         if result:
             price = result[0]
             total_price = price * quantity
             
             # Insert the order into the orders table
             cursor.execute('INSERT INTO orders (customer_id, food_item_id, quantity, total_price, payment_method) VALUES (%s, %s, %s, %s, %s)',
                            (customer_id, food_item_id, quantity, total_price, payment_method))
             
             order_id = cursor.lastrowid  # Get the last inserted order ID
             
             conn.commit()
             print(f'Order placed! Total price: ${total_price:.2f}')
             
             # Print receipt
             print_receipt(order_id)
             
             # Optionally view orders after placing one
             view_orders()  
             
         else:
             print("Invalid food item ID.")
             
    except Error as e:
         print(f"Error placing order: {e}")
         
    finally:
         cursor.close()
         conn.close()

def print_receipt(order_id):
     """Prints a receipt for the order."""
     
     conn = get_db_connection()
     
     if conn is None:
          return
     
     cursor = conn.cursor()

     try:
          # Retrieve order details for receipt
          cursor.execute('''
              SELECT o.id AS order_id, c.username AS customer_name, f.name AS food_item_name,
                     o.quantity, o.total_price, o.order_time 
              FROM orders o 
              JOIN customers c ON o.customer_id = c.id 
              JOIN food_items f ON o.food_item_id = f.id 
              WHERE o.id = %s
          ''', (order_id,))
          
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
              
     except Error as e:
          print(f"Error retrieving order details for receipt: {e}")

     finally:
          cursor.close()
          conn.close()

def view_orders():
     """Displays all orders placed by users."""
     
     conn = get_db_connection()
     
     if conn is None:
          return
     
     cursor = conn.cursor()
     
     try:
          # Join orders with customers and food items
          cursor.execute('''
              SELECT o.id AS order_id, c.username AS customer_name, f.name AS food_item_name,
                     o.quantity, o.total_price, o.order_time 
              FROM orders o 
              JOIN customers c ON o.customer_id = c.id 
              JOIN food_items f ON o.food_item_id = f.id
          ''')
          
          orders = cursor.fetchall()

          print("\nOrder History:")
          for order in orders:
              print(f'Order ID: {order[0]}, Customer: {order[1]}, Food Item: {order[2]}, '
                    f'Quantity: {order[3]}, Total Price: ${order[4]:.2f}, Order Time: {order[5]}')
              
     except Error as e:
          print(f"Error retrieving orders: {e}")
          
     finally:
          cursor.close()
          conn.close()

def main():
    
     create_database_and_tables()  # Ensure database and tables are created before proceeding
    
     while True:
         print("\nOnline Food Ordering System")
         print("1. Add Customer")
         print("2. View Customers")
         print("3. Add Food Item")
         print("4. View Food Items")
         print("5. Place Order")
         print("6. View Orders")
         print("7. Exit")

         choice = input("Choose an option: ")

         if choice == '1':
             username = input("Enter username: ")
             phone_number = input("Enter phone number: ")
             email = input("Enter email address: ")
             add_customer(username, phone_number, email)

         elif choice == '2':
             view_customers()

         elif choice == '3':
             name = input("Enter food item name: ")
             try:
                 price = float(input("Enter food item price: "))
                 add_food_item(name, price)
             except ValueError:
                 print("Invalid price entered. Please enter a numeric value.")

         elif choice == '4':
             view_food_items()

         elif choice == '5':
             view_customers()  # Show customers before placing an order
             try:
                 customer_id = int(input("Enter customer ID to place an order for: "))
                 view_food_items()  # Show menu before placing an order
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
