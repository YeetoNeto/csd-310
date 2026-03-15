""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode
 
import dotenv # to use .env file
from dotenv import dotenv_values

#using our .env file
secrets = dotenv_values(r"C:\Users\Noah\Documents\GitHub\csd-310\module-10\Secret.env")
 
""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}
try:
    """ try/catch block for handling potential MySQL database errors """
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    # output the connection status 
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))
 
    input("\n\n  Press any key to continue...\n")
    query1 = """
    SELECT w.WineName, COALESCE(SUM(oi.OrderQuantity),0) AS TotalOrderedLastMonth
        FROM Wine w
    LEFT JOIN OrderItems oi 
        ON w.WineID = oi.WineID
    LEFT JOIN Distributor_Orders o
        ON oi.OrderID = o.OrderID
        AND o.OrderDate >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
    GROUP BY w.WineID, w.WineName;
    """ # display Wines sold records; COALESCE replaces NULLS with a 0

    query2 = "SELECT * FROM Wine;" # display Wines in stock records

    query3 = """
    SELECT d.DistributorName, w.WineName
        FROM Distributor d
    JOIN DistributorWine dw 
        ON d.DistributorID = dw.DistributorID
    JOIN Wine w 
        ON dw.WineID = w.WineID
    ORDER BY d.DistributorName, w.WineName;
    """ #Display the Wines our Distributors Carry


    cursor.execute(query1)
    results = cursor.fetchall()
    print("-- Displaying Wine Bought in the Last Month --")
    for WineName, TotalOrderedLastMonth in results:
     print(f"Wine: {WineName} \n Amount Ordered: {TotalOrderedLastMonth}")


    cursor.execute(query2)
    results = cursor.fetchall()
    print("-- Displaying Wine Stock --")
    for WineId, WineName, QuantityStocked in results:
     print(f"Wine: {WineName} \n Quantity in Stock: {QuantityStocked}")


    cursor.execute(query3)
    results = cursor.fetchall()
    print("-- Displaying What Wine each Distributor Sells --")
    for DistributorName, WineName in results:
     print(f"Distributor: {DistributorName} \n Wine: {WineName}")

except mysql.connector.Error as err:
    """ on error code """
 
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
 
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
 
    else:
        print(err)
 
finally:
    """ close the connection to MySQL """
 
    db.close()
