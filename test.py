#!/usr/bin/env python3

"""Python script that can connect to a MySQL database and run through multiple connections passing in different character sets and collations."""

# Import the necessary modules
import mysql.connector
from mysql.connector import errorcode
from termcolor import colored

# Create a function that will connect to the database and pass in the character set and collation
def connect_to_database(charset, collation):
    try:
        # Connect to the database add a port to connect to a remote server port=6033
        cnx = mysql.connector.connect(user='klarsen', password='ou812', host='192.168.50.75', port=6033, database='chaos', charset=charset, collation=collation) # Add the host name

        color = 'green' if charset == 'utf8' else 'red'
        print(colored(f"Connected to server {cnx.server_host} on port {cnx.server_port}", color))
        print(colored(f"Current character set: {charset} and collation: {collation}", color))

        # Create a cursor
        cursor = cnx.cursor()

        # Create a query
        query = ("SELECT 1")

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()

        # Print the results
        print(results)

        # Close the cursor
        cursor.close()

        # Close the connection
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)
# Function to add an employee
def add_employee(name, salary, charset, collation):
    try:
        print(f"Attempting to connect to the database with character set {charset} and collation {collation}")
        # Connect to the database
        cnx = mysql.connector.connect(user='klarsen', password='ou812', host='192.168.50.75', port=6033, database='chaos', charset=charset, collation=collation)

        color = 'green' if charset == 'utf8' else 'red'
        print(colored(f"Attempting to connect to the database with character set {charset} and collation {collation}", color))

        if charset == 'latin1':
            print("Latin1 character set is accepted when adding an employee.")

        print(f"Connected to the database. Adding employee {name} with salary {salary}")
        # Create a cursor
        cursor = cnx.cursor()

        # Create an insert query
        query = "INSERT INTO employees (name, salary) VALUES (%s, %s)"

        # Execute the query with the provided name and salary
        cursor.execute(query, (name, salary))

        # Create an insert query for the second table
        query2 = "INSERT INTO test_table (name, additional_info) VALUES (%s, %s)"

        # Define the additional_info variable
        additional_info = "Some additional info with German umlauts: ä, ö, ü, ß. Here are some words: schön, fräulein, grüßen"

        # Execute the query with the provided name and additional info
        cursor.execute(query2, (name, additional_info))

        print(f"Employee {name} added successfully. Committing the transaction.")
        # Commit the transaction
        cnx.commit()

        # Close the cursor
        cursor.close()

        # Close the connection
        cnx.close()

    except mysql.connector.Error as err:
        print(colored(f"An error occurred: {err}", 'red'))

# Call the function with different character sets and collations
charsets_and_collations = [
    ('latin1', 'latin1_swedish_ci'),
    #('utf8', 'utf8_general_ci'),
    # Add more as needed...
]

for charset, collation in charsets_and_collations:
    connect_to_database(charset, collation)
    # Add an employee for each character set and collation
    add_employee('Chaos2', 5000, charset, collation)
    #add_employee('John Doe', 6000, charset, collation)