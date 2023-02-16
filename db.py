"""The DB module.

This module defines the functions to create the PistusResa database and its tables.

When you run this file as a Python script, the Python interpreter 
executes the instructions after the 
statement if __name__ == "__main__": that you find at the bottom of the file.
"""

import sqlite3
import utils


def create_database(conn, cursor):
    """Creates the PistusResa database

    Parameters
    ----------
    conn : 
        The object used to manage the database connection.
    cursor : 
        The object used to query the database.

    Returns
    -------
    bool
        True if the database could be created, False otherwise.

    """

    # We open a transaction.
    # A transaction is a sequence of read/write statements that
    # have a permanent result in the database only if they all succeed.
    #
    # More concretely, in this function we create many tables in the database.
    # The transaction is therefore a sequence of CREATE TABLE statements such as :
    #
    # BEGIN
    # CREATE TABLE XXX
    # CREATE TABLE YYY
    # CREATE TABLE ZZZ
    # ....
    #
    # If no error occurs, all the tables are permanently created in the database.
    # If an error occurs while creating a table (for instance YYY), no table will be created, even those for which
    # the statement CREATE TABLE has already been executed (in this example, XXX).
    #
    # When we start a transaction with the statement BEGIN, we must end it with either COMMIT
    # or ROLLBACK.
    #
    # * COMMIT is called when no error occurs. After calling COMMIT, the result of all the statements in
    # the transaction is permanetly written to the database. In our example, COMMIT results in actually creating all the tables
    # (XXX, YYY, ZZZ, ....)
    #
    # * ROLLBACK is called when any error occurs in the transaction. Calling ROLLBACK means that
    # the database is not modified (in our example, no table is created).
    #
    #
    cursor.execute("BEGIN")

    # Create the tables.
    try:
        # We create the table Login.
        # To do so, we call the function cursor.execute() and we pass it the
        # CREATE TABLE statement as a parameter.
        # The function cursor.execute() can raise an exception sqlite3.Error.
        # That's why we write the code for creating the tables in a try...except block.
        print("Creating the table Login....")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Login(
                username TEXT PRIMARY KEY,
                password BINARY(256)
            )
        ''')

       #####TODO: COMPLETE THE CODE HERE TO CREATE THE OTHER TABLES ####
        print("Creating table Student...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Student(
            stud_number INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            gender TEXT
            ) 
        ''')

        print("Creating table EmailAddress...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS EmailAddress(
            email TEXT  PRIMARY KEY,
            stud_number INTEGER,
            FOREIGN KEY(stud_number) REFERENCES Student(stud_number)
            ) 
        ''')

        print("Creating table Association...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Association(
            asso_name TEXT PRIMARY KEY,
            asso_desc TEXT
            ) 
        ''')

        print("Creating table Membership...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Membership(
            stud_number INTEGER,
            asso_name TEXT,
        stud_role TEXT,
        PRIMARY KEY(stud_number, asso_name),
        FOREIGN KEY(stud_number) REFERENCES Student(stud_number),
        FOREIGN KEY(asso_name) REFERENCES Association(asso_name)
    ) 
''')

        print("Creating table PistusEdition...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PistusEdition(
            year TEXT PRIMARY KEY,
            registration_fee REAL
        ) 
    ''')

        print("Creating table Registration...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Registration(
            stud_number INTEGER,
            year TEXT,
            registration_date TEXT,
            payment_date TEXT,
            PRIMARY KEY(stud_number, year),
            FOREIGN KEY(stud_number) REFERENCES Student(stud_number),
            FOREIGN KEY(year) REFERENCES PistusEdition(year)
        ) 
    ''')

       ###################################################################

    # Exception raised when something goes wrong while creating the tables.
    except sqlite3.Error as error:
        print("An error occurred while creating the tables: {}".format(error))
        # IMPORTANT : we rollback the transaction! No table is created in the database.
        conn.rollback()
        # Return False to indicate that something went wrong.
        return False

    # If we arrive here, that means that no error occurred.
    # IMPORTANT : we must COMMIT the transaction, so that all tables are actually created in the database.
    conn.commit()
    print("Database created successfully")
    # Returns True to indicate that everything went well!
    return True


# The entry point of this module.
if __name__ == "__main__":

    # Loads the app config into the dictionary app_config.
    app_config = utils.load_config()

    # From the configuration, gets the path to the database file.
    db_file = app_config["db"]

    # Open a connection to the database.
    conn = sqlite3.connect(db_file)

    # The cursor is used to execute queries to the database.
    cursor = conn.cursor()

    # Creates the database. THIS IS THE FUNCTION THAT YOU'LL NEED TO MODIFY
    create_database(conn, cursor)

    # Closes the connection to the database
    cursor.close()
    conn.close()
