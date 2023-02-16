"""The deadline module.
"""

import datetime
import sqlite3
import mregistration as mreg
import mstudent as mstud
import utils

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# The main window of the PistusResa application.
pistus_window = None

# The object used to query the database.
cursor = None

# The object used to connect to the database.
conn = None

# Code indicating an unexpected database error.
UNEXPECTED_ERROR = 0


def deadline(registration_date):
    """Returns the payment deadline given the registration date.

    Parameters
    ----------
        registration_date : datetime
            The registration date.

    Returns
    -------
        datetime
            The deadline computed on the given registration date.
    """
    return (registration_date + datetime.timedelta(days=5)).date()


def deadline_expired(_registration_date):
    """Returns whether the payment deadline has expired for a given registration.

    Parameters
    ----------
    _registration_date : string
        The registration date (dd/mm/yyyy).

    Returns
    -------
    bool
        True if the deadline has expired, False otherwise.
    """
    registration_date = utils.get_date(_registration_date)
    if registration_date is not None:
        return (datetime.date.today() - deadline(registration_date)).days > 0

    return False


def deadline_aproaching(_registration_date):
    """Returns whether the deadline for the given registration is approaching (2 days before the deadline).

    Parameters:
    ----------
        _registration_date : string
            The registration date.

    Returns:
    --------
        bool
            True if today is 2 days before the deadline.

    """
    registration_date = utils.get_date(_registration_date)
    if registration_date is not None:
        return (deadline(registration_date) - datetime.date.today()).days == 2

    return False


def deadline_management_init(_pistus_window, _cursor, _conn):
    """Initializes the deadline management module.

    Parameters
    ----------
        _pistus_window : tk.Tk
            The main window of the application.
        _cursor : 
            The object used to query the database.
        _conn : 
            The object used to connect to the database.
    """
    global pistus_window
    global cursor
    global conn

    pistus_window = _pistus_window
    cursor = _cursor
    conn = _conn


def _unpaid_registrations():
    """Returns all the unpaid registrations.

    Returns
    -------
    list.
        The list of unpaid registrations. 
        Each item of the list is a tuple (stud_number, year, registration_date).
    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    unpaid_registrations = []
    try:
        cursor.execute(
            "SELECT stud_number, year, registration_date FROM Registration WHERE payment_date is NULL")
        res = cursor.fetchall()
        for row in res:
            unpaid_registrations.append((row[0], row[1], row[2]))
    except sqlite3.Error as error:
        print(error)
    return unpaid_registrations

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def _expired_registrations(unpaid_registrations):
    """Returns all the registrations that haven't met the payment deadline.

    Parameters
    ----------
    unpaid_registrations : list
        List of all the unpaid registrations. 
        This list is the one returned by the function _unpaid_registrations().

    Returns
    -------
    list
        The list of all the registrations that haven't met the payment deadline.
        Each item of the list is a tuple (stud_number, year, registration_date).
    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    expired_registrations = []
    for reg in unpaid_registrations:
        if deadline_expired(reg[2]):
            expired_registrations.append(reg)

    return expired_registrations

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def _late_payment_registrations(unpaid_registrations):
    """Returns the registrations for which the payment deadline is two days from the current date.

    Parameters
    ----------
    unpaid_registrations : list
        List of all the unpaid registrations. 
        This list is the one returned the function _unpaid_registrations().

    Returns
    -------
    list
        The list of all the registrations for which the payment deadline is two days from the current date.
        Each item of the list is  tuple (first_name, email_address, registration_date)
    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ################
    late_payment_registrations = []
    for reg in unpaid_registrations:
        if deadline_aproaching(reg[2]):
            student = mstud.get_student(reg[0], cursor)
            late_payment_registrations.append(
                (student[1], student[4][0], reg[2]))
    return late_payment_registrations

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def _remove_expired_registrations(expired_registrations):
    """Removes all the expired registrations from the database.

    IMPORTANT:

    * You can use the function delete_registration() defined in the registration module (file mregistration.py)

    * There is likely to be more than one expired registration. 
    You should remove all the expired registrations within a transaction.
    If any registration could not be deleted for any reason (look at the delete_registration return value), 
    you should rollback the transaction. Only if all the registrations could be successfully removed, 
    you can commit the transaction.

    Parameters
    ----------
    expired_registrations : list
        List of all the expired registrations. 
        This list is the one returned by the function _expired_registrations().

    Returns
    -------
    A tuple.
        The return value of the function mreg.delete_registration.
    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ################

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    pass

    ####################################################################################


def _send_late_payment_reminder(late_payment_registrations):
    """Sends an automatic email to all students having late registrations.

    Parameters
    ----------
    _late_payment_registrations : list
        List of all the late registrations. 
        This list is the one returned by the function _late_payment_registrations().
    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ###############
    mail_server = smtplib.SMTP('localhost', 1025)
    mail_text = '''Dear {}, 
this is just a reminder that the payment deadline for your Pistus registration 
is {}.
Sincerely, 
The Pistus Organizers'''

    for reg in late_payment_registrations:
        msg = MIMEMultipart()
        msg['from'] = 'organization@pistus.fr'
        msg['Subject'] = 'Payment deadline reminder'
        msg['to'] = reg[1]
        msg.attach(MIMEText(mail_text.format(
            reg[0], deadline(utils.get_date(reg[2]))), 'plain'))
        mail_server.send_message(msg)

    mail_server.quit()

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def deadline_management():
    """Function invoked periodically to manage the unpaid registrations.

    * Retrieves the unpaid registrations
    * Identifies in the unpaid registrations those that are expired.
    * Identifies in the unpaid registrations those that are late.
    * Removes the expired registrations.
    * Sends a reminder to the students who have late registrations.

    This function is first invoked in the function  open_main_window in file 
    ./gui/mainwindow.py.
    The function is then  invoked once a day. 

    """
    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ################
    unpaid_registrations = _unpaid_registrations()
    expired_registrations = _expired_registrations(unpaid_registrations)
    late_payment_registrations = _late_payment_registrations(
        unpaid_registrations)
    _remove_expired_registrations(expired_registrations)
    _send_late_payment_reminder(late_payment_registrations)
    pistus_window.after(60*60*24*1000, deadline_management)

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################
