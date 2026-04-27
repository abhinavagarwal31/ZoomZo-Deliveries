import mysql.connector
import csv

conn = mysql.connector.connect(host='localhost',user='root',password=<your password>,database=<db name>)
cursor = conn.cursor()
print('''
||||||||||||||||||||||||||||||||||||| 
| **WELCOME TO ZOOMZO DELIVERIES!** |
|||||||||||||||||||||||||||||||||||||
''')

def admin_login():
    print("Admin Login:")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    query = "SELECT * FROM ADMINS WHERE Name = %s AND Pwd = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        print("Welcome, " + username + "!")
        admin_operations()
    else:
        print("Invalid credentials. Try again!")

def admin_operations():
    while True:
        print("\nAdmin Operations:")
        print("1. Manage Customers")
        print("2. Manage Companies")
        print("3. Manage Delivery Personnel")
        print("4. Add a New Admin")
        print("5. View Reviews for Orders")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            manage_customers()
        elif choice == "2":
            manage_companies()
        elif choice == "3":
            manage_delivery_personnel()
        elif choice == "4":
            add_admin()
        elif choice == "5":
            view_reviews()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again!")

def manage_customers():
    print("\nManage Customers:")
    print("1. View Customer Details")
    print("2. Add a Customer")
    choice = input("Enter your choice: ")

    if choice == "1":
        cust_id = input("Enter Customer ID: ")
        cursor.execute("SELECT * FROM CUSTOMERS WHERE Cust_ID = %s", (cust_id,))
        row = cursor.fetchone()
        if row:
            print("Customer ID: " + str(row[0]))
            print("Name: " + row[1])
            print("Contact Number: " + str(row[2]))
            print("Email: " + row[3])
            print("Address: " + row[4])
        else:
            print("Customer not found.")
    elif choice == "2":
        name = input("Enter Customer Name: ")
        contact_no = input("Enter Contact Number: ")
        email = input("Enter Email: ")
        address = input("Enter Address: ")
        cursor.execute("INSERT INTO CUSTOMERS (Name, Contact_No, Email, Address) VALUES (%s, %s, %s, %s)", 
                       (name, contact_no, email, address))
        conn.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        cust_id = cursor.fetchone()[0]
        print("Customer added successfully! Customer ID: " + str(cust_id))
    else:
        print("Invalid choice.")

def manage_companies():
    print("\nManage Companies:")
    print("1. View Company Details")
    print("2. Add a Company")
    choice = input("Enter your choice: ")

    if choice == "1":
        company_id = input("Enter Company ID: ")
        cursor.execute("SELECT * FROM COMPANIES WHERE Company_ID = %s", (company_id,))
        row = cursor.fetchone()
        if row:
            print("Company ID: " + str(row[0]))
            print("Name: " + row[1])
            print("Address: " + row[2])
            print("Contact Number: " + row[3])
            print("Email: " + row[4])
        else:
            print("Company not found.")
    elif choice == "2":
        name = input("Enter Company Name: ")
        address = input("Enter Address: ")
        contact_no = input("Enter Contact Number: ")
        email = input("Enter Email: ")
        cursor.execute("INSERT INTO COMPANIES (Name, Address, Contact_No, Email) VALUES (%s, %s, %s, %s)", 
                       (name, address, contact_no, email))
        conn.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        company_id = cursor.fetchone()[0]
        print("Company added successfully! Company ID: " + str(company_id))
    else:
        print("Invalid choice.")

def manage_delivery_personnel():
    print("\nManage Delivery Personnel:")
    print("1. View Delivery Personnel Details")
    print("2. Add Delivery Personnel")
    choice = input("Enter your choice: ")

    if choice == "1":
        personnel_id = input("Enter Personnel ID: ")
        cursor.execute("SELECT * FROM DELIVERY_PERSONNEL WHERE Personnel_ID = %s", (personnel_id,))
        row = cursor.fetchone()
        if row:
            print("Personnel ID: " + str(row[0]))
            print("Name: " + row[1])
            print("Contact Number: " + row[2])
            print("Vehicle Number: " + row[3])
        else:
            print("Delivery Personnel not found.")
    elif choice == "2":
        name = input("Enter Name: ")
        contact_no = input("Enter Contact Number: ")
        vehicle_no = input("Enter Vehicle Number: ")
        cursor.execute("INSERT INTO DELIVERY_PERSONNEL (Name, Contact_No, Vehicle_No) VALUES (%s, %s, %s)", 
                       (name, contact_no, vehicle_no))
        conn.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        personnel_id = cursor.fetchone()[0]
        print("Delivery personnel added successfully! Personnel ID: " + str(personnel_id))
    else:
        print("Invalid choice.")

def add_admin():
    print("\nAdd a New Admin:")
    name = input("Enter Admin Name: ")
    pwd = input("Enter Password: ")
    cursor.execute("INSERT INTO ADMINS (Name, Pwd) VALUES (%s, %s)", (name, pwd))
    conn.commit()
    print("Admin added successfully!")

def view_reviews():
    print("\nReviews for Orders:")
    try:
        with open("reviews.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                print("Order ID: " + row[0] + " | Review: " + row[1])
    except FileNotFoundError:
        print("No reviews found.")

def delivery_login():
    print("Delivery Personnel Login:")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    query = "SELECT * FROM DELIVERY_PERSONNEL WHERE Name = %s AND Personnel_ID = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        print("Welcome, " + username + "!")
        delivery_operations(result[0])
    else:
        print("Invalid credentials. Try again!")

def delivery_operations(personnel_id):
    while True:
        print("\nDelivery Personnel Operations:")
        print("1. View Assigned Orders")
        print("2. Update Order Status")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            cursor.execute("SELECT * FROM ORDERS WHERE Personnel_ID = %s", (personnel_id,))
            for row in cursor.fetchall():
                print("Order ID: " + str(row[0]))
                print("Customer ID: " + str(row[1]))
                print("Order Date: " + str(row[3]))
                print("Total Amount: " + str(row[4]))
                print("Delivery Status: " + row[5] + "\n")
        elif choice == "2":
            order_id = input("Enter Order ID: ")
            status = input("Enter new status (Pending, Shipped, Delivered): ")
            cursor.execute("UPDATE ORDERS SET Delivery_Status = %s WHERE Order_ID = %s", (status, order_id))
            conn.commit()
            print("Order status updated successfully!")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

def customer_login():
    print("Customer Login:")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    query = "SELECT * FROM CUSTOMERS WHERE Name = %s AND CONCAT(Cust_ID, '@', Contact_No) = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        print("Welcome, " + username + "!")
        customer_operations(result[0])
    else:
        print("Invalid credentials. Try again!")

def customer_operations(customer_id):
    while True:
        print("\nCustomer Operations:")
        print("1. Track Orders")
        print("2. Give a Review")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            cursor.execute("SELECT * FROM ORDERS WHERE Cust_ID = %s", (customer_id,))
            for row in cursor.fetchall():
                print("Order ID: " + str(row[0]))
                print("Order Date: " + str(row[3]))
                print("Total Amount: " + str(row[4]))
                print("Delivery Status: " + row[5] + "\n")
        elif choice == "2":
            order_id = input("Enter Order ID: ")
            review = input("Enter your review: ")
            with open("reviews.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([order_id, review])
            print("Thank you for your review!")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Admin Login")
        print("2. Delivery Personnel Login")
        print("3. Customer Login")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            admin_login()
        elif choice == "2":
            delivery_login()
        elif choice == "3":
            customer_login()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again!")

main_menu()
cursor.close()
conn.close()
