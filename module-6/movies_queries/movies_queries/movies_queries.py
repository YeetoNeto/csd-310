""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode
 
import dotenv # to use .env file
from dotenv import dotenv_values

#using our .env file
secrets = dotenv_values(r"C:\Users\Noah\Documents\GitHub\csd-310\module-6\Secret.env")
 
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
    query1 = "SELECT * FROM studio;" # display studio records
    query2 = "SELECT * FROM genre;"# display genre records
    query3 = "SELECT film_name, film_runtime FROM film WHERE film_runtime < 120;" #get short film
    query4 = "SELECT film_name, film_director FROM film ORDER BY film_director;" #get director records
    cursor.execute(query1)
    results = cursor.fetchall()
    print("-- Displaying Studio RECORDS --")
    for studio_id, studio_name in results:
     print(f"Studio ID: {studio_id} \n Studio Name: {studio_name}")

    cursor.execute(query2)
    results = cursor.fetchall()
    print("\n-- Displaying Genre RECORDS --")
    for genre_id, genre_name in results:
     print(f"Genre ID: {genre_id} \n Genre Name: {genre_name}")

    cursor.execute(query3)
    results = cursor.fetchall()
    print("\n-- Displaying Short Film RECORDS --")
    for film_name, film_runtime in results:
     print(f"Film Name: {film_name} \n Film Runtime: {film_runtime}")

    cursor.execute(query4)
    results = cursor.fetchall()
    print("\n-- Displaying Directors RECORDS in Order--")
    for film_name, director_name in results:
     print(f"Film Name: {film_name} \n Director Name: {director_name}")
 
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
