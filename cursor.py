import mysql.connector
'''
db:-
A variable that stores the connection object. 
This object is primary interface for all further database operations. 
db is used to create cursors and manage transactions.'''

# db->Database connection Object
db = mysql.connector.connect( #Creates a connection between Python program and MySQL database server.
    host="localhost",
    user="root",  # MySQL username
    password="Shahid@123",  # MySQL password
    database="shahid1"  # database name
)

cursor = db.cursor() # Database Cursor Object ->A cursor is like a pointer inside the database connection.
                     #Executes SQL commands and retrieves data