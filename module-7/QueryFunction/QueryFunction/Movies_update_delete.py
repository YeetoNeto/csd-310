""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode
 
import dotenv # to use .env file
from dotenv import dotenv_values



def showFilm(cursor, title):
    query = """
        SELECT film.film_name AS Name,
               film.film_director AS Director,
               genre.genre_name AS Genre,
               studio.studio_name AS Studio
        FROM film
        INNER JOIN genre
            ON film.genre_id = genre.genre_id
        INNER JOIN studio
            ON film.studio_id = studio.studio_id
    """

    # Execute the query
    cursor.execute(query)

    # Fetch all results
    films = cursor.fetchall()

    # Format output header
    print("\n" + "-" * 60)
    print(title)
    print("-" * 60)

    # Iterate through dataset and display results
    for film in films:
        print(f"Name: {film[0]}")
        print(f"Director: {film[1]}")
        print(f"Genre: {film[2]}")
        print(f"Studio: {film[3]}")
        print('')

    print("-" * 60)
        

def insertFilm(cursor):
   query = """
    INSERT INTO film
    (film_name, film_releaseDate, film_runtime,
    film_director, studio_id, genre_id)
    VALUES('The Martian','2015',144,'Riddley Scott',1,2)
    """
    
   cursor.execute(query)


def updateFilm(cursor):
   query = """
    UPDATE film
    SET genre_id = 1
    WHERE film_name = 'Alien';
    """
    
   cursor.execute(query)


def deleteFilm(cursor):
    query = """
    DELETE FROM film
    WHERE film_name = 'Gladiator';
    """
    cursor.execute(query)

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
db = mysql.connector.connect(**config)
cursor = db.cursor()
title = 'Displaying Films'
showFilm(cursor, title)
insertFilm(cursor)
title = 'Displaying Films After Insert'
showFilm(cursor, title)
updateFilm(cursor)
title = 'Displaying Films After Update'
showFilm(cursor, title)
deleteFilm(cursor)
title = 'Displaying Films After Delete'
showFilm(cursor, title)