"""The registration  module.

It provides the functions necessary to register students to a Pistus edition and manage all the information 
related to the registrations.

This module is already implemented!
"""

import sqlite3

# Code for an unexpected error in the database.
UNEXPECTED_ERROR = -1

# Code for a duplicate registration error.
DUPLICATE_REGISTRATION_ERROR = 0

def get_pistus_edition(edition_year, cursor):
    """Returns the Pistus edition on the specified year.

    Parameters
    ----------
    edition_year : string
        The edition year.
    cursor : 
        The object used to query the database. 

    Return
    ------
    A (possibly empty) tuple T.
        T[0] is the edition year.
        T[1] is the registration fee.
    If an error occurs while reading the database, the function returns None.
    """
    pistus_edition = ()
    try:
        cursor.execute("SELECT * FROM PistusEdition WHERE year=?", (edition_year,))
        row = cursor.fetchone()
        if row is not None:
            pistus_edition = (row[0], row[1])
    except sqlite3.Error as error:
        print(error)
        return None
    return pistus_edition

def get_student_registrations(stud_number, cursor):
    """Returns all the registrations of a student

    Parameters
    ----------
    stud_number : int
        The number of the student to register.
    cursor : 
        The object used to query the database. 
    
    Returns
    -------
    A list.
        Each item of the list is a tuple (year, registration_date, payment_date).
        If a database error occurs, the function returns None.

    """
    student_registrations = []
    try:
        cursor.execute("SELECT year, registration_date, payment_date FROM Registration \
            WHERE stud_number=? ORDER BY year ASC", (stud_number,))
        result = cursor.fetchall()
        for row in result:
            student_registrations.append((row[0], row[1], row[2]))
    except sqlite3.Error as error:
        print(error)
        return None
    return student_registrations

def add_pistus_edition(edition_year, registration_fee, cursor):
    """Adds a new Pistus edition

    Parameters
    ----------
    edition_year : string
        The Pistus edition year.
    registration_fee : float
        The registration fee.
    cursor :
        The object used to query the database. 

    Returns:
        A tuple. 
            (True, None, None) if no error occurs.
            (False, UNEXPECTED_ERROR, error) when a database error occurs. The detail of the error is in the 
            variable error.
    """
    try:
        cursor.execute("INSERT INTO PistusEdition VALUES(?, ?)", (edition_year, registration_fee))
    except sqlite3.Error as error:
        print("An error occurred while adding the Pistus edition: {}".format(error))
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)

def add_registration(stud_number, edition_year, registration_date, cursor, payment_date=None):
    """Adds a new student registration to a specified Pistus edition.

    Parameters
    ----------
    stud_number : int
        The number of the student to register.
    edition_year : string
        The Pistus edition year.
    registration_date : string
        The registration date.
    cursor : 
        The object used to query the database. 
    payment_date : string, optional
        The payment date (default: None).

    Returns
    -------
    (True, None, None) if everything goes well.

    (False, DUPLICATE_REGISTRATION_ERROR, edition_year) if we try to register a student twice to the same edition.
    The offending edition year is contained in the variable edition_year.

    (False, UNEXPECTED_ERROR, None) if another database error occurs.
    
    """
    try:
        cursor.execute("INSERT INTO Registration  VALUES(?, ?, ?, ?)", (stud_number, edition_year, registration_date, payment_date))
    except sqlite3.IntegrityError as error:
        print(error)
        return (False, DUPLICATE_REGISTRATION_ERROR, edition_year)
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, None) 
    return (True, None, None)

def delete_registration(stud_number, edition_year, cursor):
    """Deletes a registration.

    Parameters
    ----------
    stud_number : int
        The number of the student to register.
    edition_year : string
        The Pistus edition year.
    cursor : 
        The object used to query the database. 
    
    Returns
    -------
    A tuple. 
        (True, None, None) if no error occurs.
        (False, UNEXPECTED_ERROR, error) if an unexpected database error occurs. The detail of the error is in the 
        variable error.

    """
    try:
        cursor.execute("DELETE FROM Registration WHERE stud_number=? AND year = ?", (stud_number, edition_year))
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)


def update_registration_date(stud_number, edition_year, registration_date, cursor):
    """Edits the registration date of a specific student registration.

    Parameters
    ----------
    stud_number : int
        The number of the student to register.
    edition_year : string
        The Pistus edition year.
    registration_date : string
        The registration date.
    cursor : 
        The object used to query the database. 
    
    Returns
    -------
    A tuple.
        (True, None, None) if no error occurs.
        (False, UNEXPECTED_ERROR, error) if an unexpected database error occurs. The detail of the error is in the 
        variable error.
    """
    try:
        cursor.execute("UPDATE registration SET registration_date=? \
            WHERE stud_number=? AND year=?", (registration_date, stud_number, edition_year))
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)

def update_payment_date(stud_number, edition_year, payment_date, cursor):
    """Edits the payment date of a specific student registration.

    Parameters
    ----------
    stud_number : int
        The number of the student to register.
    edition_year : string
        The Pistus edition year.
    payment_date : string
        The payment date.
    cursor : 
        The object used to query the database. 
    
    Returns
    -------
    A tuple.
        (True, None, None) if no error occurs.
        (False, UNEXPECTED_ERROR, error) if an unexpected database error occurs. The detail of the error is in the 
        variable error.
    
    """
    try:
        cursor.execute("UPDATE registration SET payment_date=? \
            WHERE stud_number=? AND year=?", (payment_date, stud_number, edition_year))
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)