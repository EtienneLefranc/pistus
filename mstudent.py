"""The student module

It contains all the functions to add and edit a student in the database.

Each function is associated to an already implemented test function.
All tests functions are called in the main section of this module (see the bottom of this file). 

WHAT YOU HAVE TO DO.
--------------------
Implement the functions that are flagged with the phrase "TODO: you'll have to implement this function".
When you're done implementing a function, you can run this file as a Python script to trigger a test. 

"""

import sqlite3
import utils

# Code for an unexpected error in the database.
UNEXPECTED_ERROR = -1
# Code of the error raised when trying to use the same number for two different students.
DUPLICATE_STUD_NUMBER = 0
# Code of the error raised when trying to use the same email address for two different students.
DUPLICATE_EMAIL_ADDRESS = 1
# Code of the error raised when trying to add twice a student to the same association.
DUPLICATE_MEMBERSHIP = 2


def test_get_student(cursor):
    """Tests the function get_student

    Parameters
    ----------
    cursor :
        The object used to query the database.
    """
    try:
        # Non-existing student
        stud = get_student(1234, cursor)
        assert len(
            stud) == 0, "when a student doesn't exist, the return tuple must be empty"

        # Existing student
        stud = get_student(7719175, cursor)
        assert len(
            stud) != 0, "when a student exists, the return tuple must not be empty"
        assert stud[0] == 7719175, "the first item of the returned tuple must be the student number"
        assert stud[1] == "Eliane", "the second item of the returned tuple must be the student first name"
        assert stud[2] == "CHOISNE", "the third item of the returned tuple must be the student last name"
        assert stud[3] == "M", "the fourth item of the returned tuple must be the student gender"
        print("The function get_student is CORRECT! Great job!\n\n")
    except NotImplementedError:
        pass


def get_student(stud_number, cursor):
    """Loads the student with the given number from the database.

    Parameters
    ----------
    stud_number : int
        The student number.
    cursor : 
        The object used to query the database.

    Returns
    -------
    A tuple
        T[0] is the student number.
        T[1] is the student first name.
        T[2] is the student last name.
        T[3] is the student gender.
        T[4] is a (possibly, empty) list containing the email addresses of the student.

    If no student can be found, the tuple T is empty.

    If an error occurs while querying the database, the function returns None.
    """
    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    stud_data = None
    # Gets the data from the table Student
    try:
        cursor.execute('SELECT * FROM Student WHERE stud_number=?',
                       (stud_number,))
        stud_data = cursor.fetchone()
    except sqlite3.Error as error:
        print(error)
        return None
    # If no student can be found, return an empty tuple
    if stud_data is None:
        return ()

    email_addresses = []
    try:
        # Gets the email addresses of the student.
        cursor.execute(
            "SELECT email FROM EmailAddress WHERE stud_number=?", (stud_number,))
        result = cursor.fetchall()
        for row in result:
            email_addresses.append(row[0])
    except sqlite3.Error as error:
        print(error)
        return None
    return (stud_data[0], stud_data[1], stud_data[2], stud_data[3], email_addresses)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_get_student().

    ##############################################################################


def test_get_associations(cursor):
    """Tests the function get_associations

    Parameters
    ----------
    cursor :
        The object used to query the database.
    """
    try:
        associations = get_associations(cursor)
        assert len(associations) == 11, "You must have 11 associations in your database.\
            Verify that you correctly loaded the data into the database and try again"

        associations.sort(key=lambda x: x[0])
        assert associations[0][
            0] == "BDA", "The function returns a list where each item is a tuple (asso_name, asso_desc)"
        print("The function get_associations is CORRECT! Great job!\n\n")
    except NotImplementedError:
        pass


def get_associations(cursor):
    """Returns all the associations from the database.

    Parameters
    ----------
    cursor : 
        The object used to query the database.

    Returns
    -------
    A (possibly, empty) list of all the associations in the database. 
    Each item of the list is a tuple (asso_name, asso_desc).

    If an error occurs while querying the database, the function returns None.
    """
    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    associations = []
    try:
        # Gets the data from the table Association.
        cursor.execute('SELECT * FROM Association')
        result = cursor.fetchall()
        for row in result:
            associations.append((row[0], row[1]))
    except sqlite3.Error as error:
        print(error)
        return None
    return associations

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_get_associations().

    ##############################################################################


def test_get_roles(cursor):
    """Tests the function get_roles

    Parameters
    ----------
    cursor :
        The object used to query the database.
    """
    try:
        roles = get_roles(cursor)
        assert len(roles) == 5, "You must have  5 roles in your database.\
            Verify that you correctly loaded the data into the database and try again"

        roles.sort()
        actual_roles = ['member', 'president',
                        'secretary', 'treasurer', 'vice-president']

        for i in range(len(roles)):
            assert roles[i] == actual_roles[i], "The five roles must be 'member', 'president', 'secretary', 'treasurer', 'vice-president'"
        print("The function get_roles is CORRECT! Great job!\n\n")
    except NotImplementedError:
        pass


def get_roles(cursor):
    """Get the student roles in the associations WITHOUT REPETITIONS.

    Parameters
    ----------
    cursor: 
        The object used to query the database.

    Returns
    -------
    A (possibly, empty) list of all the student roles.

    If an error occurs while querying the database, the function returns None.
    """
    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    roles = []
    try:
        # Get the student roles in the associations.
        cursor.execute('SELECT DISTINCT stud_role FROM Membership')
        result = cursor.fetchall()
        for row in result:
            roles.append(row[0])
    except sqlite3.Error as error:
        print(error)
        return None
    return roles

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_get_roles().

    ##############################################################################


def test_get_memberships(cursor):
    """Tests the function get_memberships

    Parameters
    ----------
    cursor :
        The object used to query the database.
    """

    try:
        # Memberships of an non-existing student.
        memberships = get_memberships(1234, cursor)
        assert len(
            memberships) == 0, "The memberships of a non-existing student must be an empty list"

        memberships = get_memberships(7719175, cursor)
        assert len(
            memberships) == 3, "Student 7719175 must be member of 3 associations"

        memberships.sort(key=lambda x: x[0])
        assert memberships[0][0] == "BDE" and memberships[0][
            1] == "member", "The function returns a list, where each item must be a tuple (asso_name, stud_role)"

        print("The function get_memberships is CORRECT! Great job!\n\n")
    except NotImplementedError:
        pass


def get_memberships(stud_number, cursor):
    """Get all the associations of which a student is a member.

    Parameters
    ----------
    stud_number : int
        The student number
    cursor: 
        The object used to query the database.

    Returns
    -------
    A (possibly, empty) list of the student memberships.
    Each item of the list is a tuple (asso_name, student_role).

    If an error occurs while querying the database, the function returns None.

    """
    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    memberships = []
    try:
        cursor.execute('SELECT asso_name, stud_role FROM Membership WHERE stud_number=?',
                       (stud_number,))
        result = cursor.fetchall()
        for row in result:
            memberships.append((row[0], row[1]))
    except sqlite3.Error as error:
        print(error)
        return None
    return memberships

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_get_memberships().

    ##############################################################################


def test_add_email_address(cursor, conn):
    """Tests the function add_email_address

    Parameters
    ----------
    cursor :
        The object used to query the database.
    conn : 
        The object used to connect to the database.
    """

    try:
        # Trying to insert an existing email address.
        cursor.execute("BEGIN")
        res = add_email_address(
            7719175, "eliane.choisne@centralesupelec.fr", cursor)
        assert res == (False, DUPLICATE_EMAIL_ADDRESS, "eliane.choisne@centralesupelec.fr"), "The email address eliane.choisne@centralesupelec.fr is already in use. \
            The function should return (False, DUPLICATE_EMAIL_ADDRESS, eliane.choisne@centralesupelec.fr)"
        conn.rollback()

        # Trying to add an email address with no errors.
        cursor.execute("BEGIN")
        res = add_email_address(7719175, "eliane.choisne@gmail.com", cursor)
        assert res == (
            True, None, None), "Adding this email address should raise no error and the function should return (True, None, None)"
        conn.rollback()
        print("The function add_email_address is CORRECT! Great job!\n\n")
    except NotImplementedError:
        conn.rollback()


def add_email_address(stud_number, email_address, cursor):
    """Adds an email address of a student.

    Parameters
    ----------
    stud_number : int
        The student number.
    email_address : string
        The student email address.
    cursor : 
        The object used to query the database.

    Returns
    -------
    A tuple T
        (True, None, None) if no error occurs.

        (False, DUPLICATE_EMAIL_ADDRESS, email) if we try to use the same email address for two different 
        students. The variable email indicates the offending email address

        (False, UNEXPECTED_ERROR, error) if an unexpected error arises. The variable error contains the raw 
        sqlite3.Error message.
    """

    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    try:
        cursor.execute('INSERT INTO EmailAddress VALUES (?, ?)',
                       (email_address, stud_number))
    except sqlite3.IntegrityError as error:
        print(error)
        return (False, DUPLICATE_EMAIL_ADDRESS, email_address)
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_add_email_address().
    #
    # NOTE THAT THE MESSAGE "UNIQUE constraint failed: EmailAddress.email" WILL BE
    # DISPLAYED DURING THE EXECUTION OF THIS TEST, THIS IS EXPECTED

    ##############################################################################


def test_add_student(cursor, conn):
    """Tests the function add_student

    Parameters
    ----------
    cursor :
        The object used to query the database.
    conn : 
        The object used to connect to the database.
    """

    try:
        # Trying to re-use an existing student number.
        cursor.execute("BEGIN")
        res = add_student(7719175, "Test", "Student", "F", [
                          "test.student@centralesupelec.fr"], cursor)
        assert res == (False, DUPLICATE_STUD_NUMBER, None), "The student number 7719175 is already in use. \
            The function should return (False, DUPLICATE_STUD_NUMBER, None)"
        conn.rollback()

        # Trying to use an existing email address
        cursor.execute("BEGIN")
        res = add_student(1234, "Test", "Student", "F", [
                          "eliane.choisne@centralesupelec.fr"], cursor)
        assert res == (False, DUPLICATE_EMAIL_ADDRESS, "eliane.choisne@centralesupelec.fr"), "The email address eliane.choisne@centralesupelec.fr is already in use. \
            The function should return (False, DUPLICATE_EMAIL_ADDRESS, eliane.choisne@centralesupelec.fr)"
        conn.rollback()

        # Trying to add a student with no errors.
        cursor.execute("BEGIN")
        res = add_student(1234, "Test", "Student", "F", [
                          "test.student@centralesupelec.fr", "test.student@gmail.com"], cursor)
        assert res == (
            True, None, None), "Adding this student should raise no error and the function should return (True, None, None)"
        conn.rollback()
        print("The function add_student is CORRECT! Great job!\n\n")
    except NotImplementedError:
        conn.rollback()


def add_student(stud_number, first_name, last_name, gender, email_addresses, cursor):
    """Adds a student to the database.
    The function adds the following information: student number, first name, last name, gender and 
    all the email addresses specified in the list email_addresses. 

    Parameters
    ----------
    stud_number : int
        The student number.
    first_name : string
        The student first name.
    last_name : string
        The student last name.
    gender : string
        The student gender.
    email_addresses : list
        The student email addresses.
    cursor : 
        The object used to query the database.

    Returns
    -------
    A tuple T
        (True, None, None) if no error occurs.

        (False, DUPLICATE_STUD_NUMBER, None) if we try to use the same number for two different students.

        (False, DUPLICATE_EMAIL_ADDRESS, email) if we try to use the same email address for two different 
        students. The variable email indicates the offending email address

        (False, UNEXPECTED_ERROR, error) if an unexpected error arises. The variable error is the raw 
        sqlite3.Error message.
    """
    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    try:
        # Insert the values in the table Student
        cursor.execute('INSERT INTO Student VALUES (?, ?, ?, ?)',
                       (stud_number, first_name, last_name, gender))
    except sqlite3.IntegrityError as error:
        print(error)
        return (False, DUPLICATE_STUD_NUMBER, None)
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)

    # Add the email addresses of the student
    for email in email_addresses:
        res = add_email_address(stud_number, email, cursor)
        if res[0] == False:
            return res
    return (True, None, None)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_add_student().
    #
    # NOTE THAT THE MESSAGE "UNIQUE constraint failed: Student.stud_number" WILL BE
    # DISPLAYED DURING THE EXECUTION OF THIS TEST, THIS IS EXPECTED
    #

    ##############################################################################


def test_add_membership(cursor, conn):
    """Tests the function add_membership

    Parameters
    ----------
    cursor :
        The object used to query the database.
    conn : 
        The object used to connect to the database.
    """

    try:
        # Trying to add a duplicate membership
        cursor.execute("BEGIN")
        res = add_membership(7719175, ("BDE", "member"), cursor)
        assert res == (False, DUPLICATE_MEMBERSHIP, "BDE"), "The student number 7719175 is already in association BDE. \
            The function should return (False, DUPLICATE_MEMBERSHIP, \"BDE\")"
        conn.rollback()

        # Trying to add a membership with no errors.
        cursor.execute("BEGIN")
        res = add_membership(3528, ("BDE", "president"), cursor)
        assert res == (
            True, None, None), "Adding the membership (3528, BDE, president) should raise no error and the function should return (True, None, None)"
        conn.rollback()
        print("The function add_membership is CORRECT! Great job!\n\n")
    except NotImplementedError:
        conn.rollback()


def add_membership(stud_number, membership, cursor):
    """Adds a membership to the database. 

    Parameters
    ----------
    stud_number : int
        The student number.
    membership : tuple T
        T[0] is the association name, T[1] is the student role in the association.
    cursor : 
        The object used to query the database.

    Returns
    -------
    A tuple T
        (True, None, None) if no error occurs.

        (False, DUPLICATE_MEMBERSHIP, asso_name) if we try to add a student twice to the same association.
        The variable asso_name contains the name of the offending association.

        (False, UNEXPECTED_ERROR, error) if an unexpected error arises. The variable error is the raw 
        sqlite3.Error message.
    """

    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    try:
        cursor.execute('INSERT INTO Membership VALUES (?, ?, ?)',
                       (stud_number, membership[0], membership[1]))
    except sqlite3.IntegrityError as error:
        print(error)
        return (False, DUPLICATE_MEMBERSHIP, membership[0])
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_add_membership().
    #
    # NOTE THAT THE MESSAGE "UNIQUE constraint failed: Membership.stud_number, Membership.asso_name" WILL BE
    # DISPLAYED DURING THE EXECUTION OF THIS TEST, THIS IS EXPECTED
    #

    ##############################################################################


def test_delete_email_address(cursor, conn):
    """Tests the function delete_email_address

    Parameters
    ----------
    cursor :
        The object used to query the database.
    conn : 
        The object used to connect to the database.
    """
    try:
        cursor.execute("BEGIN")
        res = delete_email_address(
            6655783, "zineb.algourdin@centralesupelec.fr", cursor)
        assert res == (
            True, None, None), "Deleting this email address should not raise any error and the function should return (True, None, None)"
        conn.commit()
        print("The function delete_email_address is CORRECT! Great job!\n\n")
    except NotImplementedError:
        conn.rollback()


def delete_email_address(stud_number, email_address, cursor):
    """Deletes an email address of a student.

    Parameters
    ----------
    stud_number : int
        The student number.
    email_address : string
        The student email address
    cursor : 
        The object used to query the database.

    Returns
    -------
    A tuple T
        (True, None, None) if no error occurs.

        (False, UNEXPECTED_ERROR, error) if an unexpected error arises. The variable error contains the raw 
        sqlite3.Error message.
    """
   ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    try:
        cursor.execute('DELETE FROM EmailAddress WHERE stud_number=? AND email=?',
                       (stud_number, email_address))
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_delete_email_address(). IF THE TEST
    # SUCCEEDS, VERIFY (BY USING DB BROWSER FOR SQLITE) THAT IN THE DATABASE:
    #
    # * The student 6655783 isn't associated to the address zineb.algourdin@centralesupelec.fr anymore.
    #

    ##############################################################################


def test_delete_membership(cursor, conn):
    """Tests the function delete_membership

    Parameters
    ----------
    cursor :
        The object used to query the database.
    conn : 
        The object used to connect to the database.
    """
    try:
        cursor.execute("BEGIN")
        res = delete_membership(36833, "BDE", cursor)
        assert res == (
            True, None, None), "Deleting this membership should not raise any error and the function should return (True, None, None)"
        conn.commit()
        print("The function delete_membership is CORRECT! Great job!\n\n")
    except NotImplementedError:
        conn.rollback()


def delete_membership(stud_number, asso_name, cursor):
    """Deletes a membership of a student.

    Parameters
    ----------
    stud_number : int
        The student number.
    asso_name : string
        The association of the student
    cursor : 
        The object used to query the database.

    Returns
    -------
    A tuple T
        (True, None, None) if no error occurs.

        (False, UNEXPECTED_ERROR, error) if an unexpected error arises. The variable error is the raw 
        sqlite3.Error message.
    """
    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    try:
        cursor.execute('DELETE FROM Membership WHERE stud_number=? and asso_name=?',
                       (stud_number, asso_name))
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_delete_membership(). IF THE TEST
    # SUCCEEDS, VERIFY (BY USING DB BROWSER FOR SQLITE) THAT IN THE DATABASE:
    #
    # * The student 36833 isn't in the association BDE anymore.
    #

    ##############################################################################


def test_update_first_name(cursor, conn):
    """Tests the function update_first_name

    Parameters
    ----------
    cursor :
        The object used to query the database.
    conn : 
        The object used to connect to the database.
    """
    try:
        cursor.execute("BEGIN")
        res = update_first_name(36833, "Camille", cursor)
        assert res == (
            True, None, None), "Updating this first name should not raise any error and the function should return (True, None, None)"
        conn.commit()
        print("The function update_first_name is CORRECT! Great job!\n\n")
    except NotImplementedError:
        conn.rollback()


def update_first_name(stud_number, first_name, cursor):
    """Updates the first name of a student.

    Parameters
    ----------
    stud_number : int
        The student number.
    first_name : string
        The student new first name.
    cursor : 
        The object used to query the database.

    Returns
    -------
    A tuple T
        (True, None, None) if no error occurs.

        (False, UNEXPECTED_ERROR, error) if an unexpected error arises. The variable error contains the raw sqlite3.Error message.
    """
    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    try:
        cursor.execute('UPDATE student SET first_name=? WHERE stud_number=?',
                       (first_name, stud_number))
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_update_first_name(). IF THE TEST
    # SUCCEEDS, VERIFY (BY USING DB BROWSER FOR SQLITE) THAT IN THE DATABASE:
    #
    # * The first name of student 36833 is Camille.
    #

    ##############################################################################


def test_update_last_name(cursor, conn):
    """Tests the function update_last_name

    Parameters
    ----------
    cursor :
        The object used to query the database.
    conn : 
        The object used to connect to the database.
    """
    try:
        cursor.execute("BEGIN")
        res = update_last_name(36833, "BLANC", cursor)
        assert res == (
            True, None, None), "Updating this last name should not raise any error and the function should return (True, None, None)"
        conn.commit()
        print("The function update_last_name is CORRECT! Great job!\n\n")
    except NotImplementedError:
        conn.rollback()


def update_last_name(stud_number, last_name, cursor):
    """Updates the last name of a student.

    Parameters
    ----------
    stud_number : int
        The student number.
    last_name : string
        The student new last name.
    cursor : 
        The object used to query the database.

    Returns
    -------
    A tuple T
        (True, None, None) if no error occurs.

        (False, UNEXPECTED_ERROR, error) if an unexpected error arises. The variable error contains the raw 
        sqlite3.Error message.
    """
    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    try:
        cursor.execute('UPDATE student SET last_name=? WHERE stud_number=?',
                       (last_name, stud_number))
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_update_last_name(). IF THE TEST
    # SUCCEEDS, VERIFY (BY USING DB BROWSER FOR SQLITE) THAT IN THE DATABASE:
    #
    # * The last name of student 36833 is BLANC.
    #

    ##############################################################################


def test_update_gender(cursor, conn):
    """Tests the function update_gender

    Parameters
    ----------
    cursor :
        The object used to query the database.
    conn : 
        The object used to connect to the database.
    """
    try:
        cursor.execute("BEGIN")
        res = update_gender(36833, "F", cursor)
        assert res == (
            True, None, None), "Updating this gender should not raise any error and the function should return (True, None, None)"
        conn.commit()
        print("The function update_gender is CORRECT! Great job!\n\n")
    except NotImplementedError:
        conn.rollback()


def update_gender(stud_number, gender, cursor):
    """Updates the gender of a student.

    Parameters
    ----------
    stud_number : int
        The student number.
    gender : string
        The student new gender.
    cursor : 
        The object used to query the database.

    Returns
    -------
    A tuple T
        (True, None, None) if no error occurs.

        (False, UNEXPECTED_ERROR, error) if an unexpected error arises. The variable error contains the raw 
        sqlite3.Error message.
    """
    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    try:
        cursor.execute('UPDATE student SET gender=? WHERE stud_number=?',
                       (gender, stud_number))
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_update_gender(). IF THE TEST
    # SUCCEEDS, VERIFY (BY USING DB BROWSER FOR SQLITE) THAT IN THE DATABASE:
    #
    # * The gender of student 36833 is F.
    #

    ##############################################################################


def test_update_email_address(cursor, conn):
    """Tests the function update_email_address

    Parameters
    ----------
    cursor :
        The object used to query the database.
    conn : 
        The object used to connect to the database.
    """
    try:
        # Trying to update to an existing email address
        cursor.execute("BEGIN")
        res = update_email_address(
            3528, "ericka.guyomard@centralesupelec.fr", "eliane.choisne@centralesupelec.fr", cursor)
        assert res == (False, DUPLICATE_EMAIL_ADDRESS, "eliane.choisne@centralesupelec.fr"), "The email address is already in use and the function\
            should return (False, DUPLICATE_EMAIL_ADDRESS, \"eliane.choisne@centralesupelec.fr\")"
        conn.rollback()

        # Trying to add a legitimate email address.
        cursor.execute("BEGIN")
        res = update_email_address(
            3528, "ericka.guyomard@centralesupelec.fr", "ericka.guyomard@gmail.com", cursor)
        assert res == (
            True, None, None), "Updating this email address should not raise any error and the function should return (True, None, None)"
        conn.rollback()
        print("The function update_email_address is CORRECT! Great job!\n\n")
    except NotImplementedError:
        conn.rollback()


def update_email_address(stud_number, old_email_address, new_email_address, cursor):
    """Updates an email address of a student.

    Parameters
    ----------
    stud_number : int
        The student number.
    old_email_address : string
        The student old email address
    new_email_address : string
        The student new email address
    cursor : 
        The object used to query the database.

    Returns
    -------
    A tuple T
        (True, None, None) if no error occurs.

        (False, DUPLICATE_EMAIL_ADDRESS, email) if we try to use the same email address for two different 
        students. The variable email indicates the offending email address

        (False, UNEXPECTED_ERROR, error) if an unexpected error arises. The variable error contains the raw 
        sqlite3.Error message.
    """
    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    try:
        cursor.execute('UPDATE EmailAddress SET email=? WHERE stud_number=? AND email=?',
                       (new_email_address, stud_number, old_email_address))
    except sqlite3.IntegrityError as error:
        print(error)
        return (False, DUPLICATE_EMAIL_ADDRESS, new_email_address)
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_update_email_address().
    #
    # NOTE THAT THE MESSAGE "UNIQUE constraint failed: EmailAddress.email" WILL BE
    # DISPLAYED DURING THE EXECUTION OF THIS TEST, THIS IS EXPECTED
    #

    ##############################################################################


def test_update_membership(cursor, conn):
    """Tests the function update_membership

    Parameters
    ----------
    cursor :
        The object used to query the database.
    conn : 
        The object used to connect to the database.
    """

    try:
        # Trying to update to an existing membership
        cursor.execute("BEGIN")
        res = update_membership(7719175, "Barco", "BDE", "member", cursor)
        assert res == (False, DUPLICATE_MEMBERSHIP, "BDE"), "The student is already in BDE the function\
            should return (False, DUPLICATE_MEMBERSHIP, \"BDE\")"
        conn.rollback()

        # Trying to add a legitimate membership.
        cursor.execute("BEGIN")
        res = update_membership(7719175, "Barco", "BDA", "member", cursor)
        assert res == (
            True, None, None), "Updating this membership should not raise any error and the function should return (True, None, None)"
        conn.rollback()
        print("The function test_update_membership is CORRECT! Great job!\n\n")
    except NotImplementedError:
        conn.rollback()


def update_membership(stud_number, old_association, new_association, role, cursor):
    """Updates a membership of a student

    Parameters
    ----------
    stud_number : int
        The student number.
    old_association : string
        Name of the old association of the student.
    new_association : string
        Name of the new association of the student.
    role : string
        The role of the student in the new association.
    cursor : 
        The object used to query the database.

    Returns
    -------
    A tuple T
        (True, None, None) if no error occurs.

        (False, DUPLICATE_MEMBERSHIP, asso_name) if we try to add a student twice to the same association.
        The variable asso_name contains the name of the offending association.

        (False, UNEXPECTED_ERROR, error) if an unexpected error arises. The variable error is the raw 
        sqlite3.Error message.
    """
    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    try:
        cursor.execute('UPDATE Membership SET asso_name=?, stud_role=? WHERE stud_number=?\
            AND asso_name=?', (new_association, role, stud_number, old_association))
    except sqlite3.IntegrityError as error:
        print(error)
        return (False, DUPLICATE_MEMBERSHIP, new_association)
    except sqlite3.Error as error:
        print(error)
        return (False, UNEXPECTED_ERROR, error)
    return (True, None, None)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    # AFTER YOU FINISH THE IMPLEMENTATION OF THIS FUNCTION, RUN THIS FILE AS A PYTHON
    # SCRIPT. THIS WILL TRIGGER THE TEST test_update_membership().
    #
    # NOTE THAT THE MESSAGE "Membership.stud_number, Membership.asso_name" WILL BE
    # DISPLAYED DURING THE EXECUTION OF THIS TEST, THIS IS EXPECTED
    #

    ##############################################################################


# Entry point of this module.
if __name__ == '__main__':

    # Loads the application configuration
    config = utils.load_config()

    # Connects to the database.
    conn = sqlite3.connect(config["db"])

    # Enables the foreign key contraints support in SQLite.
    conn.execute("PRAGMA foreign_keys = 1")

    # Get the cursor for the connection. This object is used to execute queries
    # in the database.
    cursor = conn.cursor()

    ###################### CALLING HERE THE TEST FUNCTIONS ##########################

    test_get_student(cursor)
    test_get_associations(cursor)
    test_get_roles(cursor)
    test_get_memberships(cursor)
    test_add_email_address(cursor, conn)
    test_add_student(cursor, conn)
    test_add_membership(cursor, conn)
    test_delete_email_address(cursor, conn)
    test_delete_membership(cursor, conn)
    test_update_first_name(cursor, conn)
    test_update_last_name(cursor, conn)
    test_update_gender(cursor, conn)
    test_update_email_address(cursor, conn)
    test_update_membership(cursor, conn)

    #################################################################################

    # Close the connection to the database.
    cursor.close()
    conn.close()
