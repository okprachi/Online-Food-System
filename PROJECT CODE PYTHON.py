import os
import platform
import mysql.connector
import pandas as pd
mydb=mysql.connector.connect(host="localhost",\
                             user="root",\
                             passwd ="root",\
                             database="food")
mycursor=mydb.cursor()

def Customer():
    L=[]
    c_id=int(input("Enter the Customer ID number : "))
    L.append(c_id)
    name=input("Enter Customer's name : ")
    L.append(name)
    cphone=int(input("Enter customer's Phone number : "))
    L.append(cphone)
    payment=int(input("Enter payment method ((1)Credit Card/(2)Debit Card:)"))
    L.append(payment)
    pstatus=input("Enter the payment status : ")
    L.append(pstatus)
    email=input("Enter the email ID : ")
    L.append(email)
    orderid=input("Enter the Order ID : ")
    L.append(orderid)
    date=input("Enter the Date : ")
    L.append(date)
    cust=(L)
    sql="INSERT INTO Customer(c_id,name,cphone,payment,pstatus,email,orderid,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql,cust)
    mydb.commit()
   # Customer Table :- c_id (PK  C_name  C_phonenum  Payment_method (Cash/Credit Card)  Payment_status (Paid/Unpaid)  Email  Emp_id (FK)  date


def Employee():
    L=[]
    Emp_id=int(input("Enter the Employee ID : "))
    L.append(Emp_id)
    ename=input("Enter Employee's name : ")
    L.append(ename)
    emp_g=input("Enter Employee's gender : ")
    L.append(emp_g)
    eage=int(input("Enter Employee's age : "))
    L.append(eage)
    emp_phone=int(input("Enter Employee's Phone number : "))
    L.append(emp_phone)
    pwd=input("Enter the password : ")
    L.append(pwd)
    EMP=(L)
    sql="INSERT INTO Employee(Emp_id,ename,emp_g,eage,emp_phone,pwd) values (%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql,EMP)
    mydb.commit()




def Food():
    L=[]
    Food_id=int(input("Enter the Food id : "))
    L.append(Food_id)
    Foodname=input("Enter the Food name : ")
    L.append(Foodname)
    Food_size=input("Enter Food size : ")
    L.append(Food_size)
    prize=int(input("Enter Prize of Food : "))
    L.append(prize)
    Food=(L)
    sql="INSERT INTO Food(Food_id,Foodname,Food_size,prize) values (%s,%s,%s,%s)"
    mycursor.execute(sql,Food)
    mydb.commit()


#Food_id (PK)    Foodname    Food_size    price




def OrderFood():
    L=[]
    OrderF_id=int(input("Enter the Food order ID : "))
    L.append(OrderF_id)
    C_id=input("Enter Customer's ID : ")
    L.append(C_id)
    Emp_id=input("Enter Employee's ID : ")
    L.append(Emp_id)
    Food_id=int(input("Enter Food ID : "))
    L.append(Food_id)
    Food_qty=input("Enter Qty : ")
    L.append(Food_qty)
    Total_price=int(input("Enter Total price : "))
    L.append(Total_price)
    OrderFood=(L)
    sql="INSERT INTO OrderFood(OrderF_id,C_id,Emp_id,Food_id,Food_qty,Total_price ) values (%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql,OrderFood)
    mydb.commit()

#OrderF_id (PK)  C_id (FK)  Employee_if (FK)  Food_id (FK)  Food_qty  Total_price




def View():
    print("Select the search criteria : ")
    print("1. Employee")
    print("2. Cutomer")
    print("3. Food")
    print("4. Order Food")
    ch=int(input("Enter the choice 1 to 4 : "))
    if ch==1:
        s=int(input("Enter Employee ID : "))
        rl=(s,)
        sql="select * from Employee where Emp_id=%s"
        mycursor.execute(sql,rl)
        res=mycursor.fetchall()
        for x in res:
            print(x)



    elif ch==2:
        s=input("Enter Customer's name : ")
        rl=(s,)
        sql="select * from Customer where cname=%s"
        mycursor.execute(sql,rl)
        res=mycursor.fetchall(_)
        for x in res:
            print(x)



    elif ch==3:

        sql="select * from food"
        mycursor.execute(sql)
        res=mycursor.fetchall()
        for x in res:
            print(x)

#print("The Food details are as follows : ")
#print("(Customer ID, Food Name, quantity, Cost)")
#for x in res:
    #print(x)

def feeDeposit():
    L=[]
    roll=int(input("Enter the roll number : "))
    L.append(roll)
    feedeposit=("Enter the Fee to be deposited : ")
    L.append(feedeposit)
    month=input("Enter month of fee : ")
    L.append(month)
    fee=(L)
    sql="insert into fee (roll,feedeposit,month) values (%s,%s,%s)"
    mycursor.execute(sql,fee)
    mydb.coomit()



def MenuSet():
    print("Enter 1 : To Add Employee")
    print("Enter 2 : To Add Customer details")
    print("Enter 3 : To Add Food Details ")
    print("Enter 4 : For Food Order")
    print("Enter 5 : For feedDeposit")
    print("Enter 6 : To view Food booking")

    try:

        userInput = int(input("Please Select an above option : "))
    except ValueError:
        exit("\nhy! That's not a number")
    else:
         print("\n")
    if (userInput==1):
        Employee()
    elif (userInput==2):
        Customer()
    elif (userInput==3):
        Food()
    elif (userInput==4):
        OrderFood()
    elif (userInput==5):
        feeDeposit()
    elif (userInput==6):
        View()

    else:
            print("Enter correct choice. . .")


def runAgain():
    runAgn=input("\nwant to run Again Y/N")
    while runAgn.lower()=='y':
        if(platform.system()=="Windows"):
            print(os.system('cls'))
        else:
            print(os.system('clear'))
        MenuSet()
        runAgn=input("\nwant to run Again y/n")
        print("Good Bye ... HAVE A NICE DAY")
MenuSet()
runAgain()

        
                
