"""This modules defines some useful functions that are 
called in different points of the application.

"""

from datetime import datetime, date
from PIL import Image, ImageTk
import re
import csv


def load_config():
    """Loads the application configuration from the file into a dictionary.

    Returns
    -------
    A dictionary.
        The application configuration.
    """
    # The dictionary to return.
    config = {}

    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    with open("./config/config", "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            config[row[0]] = row[1]

    return config

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    ##############################################################################


def load_messages_bundle(messages_bundle_file):
    """Loads the messages bundle from the given file into a dictionary.

    The messages bundle contains all the text (labels, button labels..) 
    that is shown in the application GUI.
    In the bundle, each message is identified by a key.
    In the program code, each message is referred to by using its key; the message is not hard-coded in the program.
    This way, if we want to change the language, we can simply load a different bundle, without changing the code.

    Parameters
    ----------
    messages_bundle_file : string
        The path to the file containing the messages bundle.

    Returns
    -------
    dictionary
        Contains the key-value pairs that compose the bundle.
    """
    # The dictionary to return
    messages_bundle = {}

    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    with open(messages_bundle_file, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            messages_bundle[row[0]] = row[1]

    return messages_bundle

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    ##############################################################################


def load_check_image():
    """Loads the image used to indicate that a field contains a correct value.

    """
    check_image = Image.open("./gui/icons/check-128.png")
    check_image = check_image.resize((20, 20), Image.ANTIALIAS)
    check_image = ImageTk.PhotoImage(check_image)
    return check_image


def get_date(date):
    """Returns a datetime object from the given date.

    Parameters
    ----------
    date : string
        A date (format dd/mm/yyyy)

    Returns
    -------
    datetime
        The given date as a datetime object.
        The function returns None if the given date is not in the right format.

    """
    date_obj = None
    try:
        date_obj = datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        pass
    return date_obj


def is_valid_date(date, empty=True):
    """Returns whether the given date is valid or not.

    Parameters:
    -----------
    date : string
        A date (format dd/mm/yyyy)
    empty :
        If set to True, an empty string is considered as a valid date.

    Returns
    -------
    bool
        True if the given date is valid, False otherwise.
    """

    if empty and len(date) == 0:
        return True
    return get_date(date) is not None


def check_registration_year(_registration_date, year=None):
    """Checks that the registration year (if specified) is (given year - 1)

    Parameters
    ----------
    _registration_date : string
        The registration date.
    year : string
        The given year.

    Returns
    -------
    bool
        True if the registration year (if specified) is (year-1).
    """

    registration_date = get_date(_registration_date)
    return year is None or registration_date is None or registration_date.year == year - 1


def payment_date_after_registration(_payment_date, _registration_date):
    """Checks whether the payment date is after the registration date.

    Parameters
    ----------
    _payment_date : string
        The payment date
    _registration_date : string
        The registration date

    Returns
    -------
    bool
        True if the payment date is after the registration date, False otherwise.
    """
    payment_date = get_date(_payment_date)
    registration_date = get_date(_registration_date)

    return payment_date is None or registration_date is None or (payment_date - registration_date).days >= 0


def is_valid_fee(fee):
    """Checks whether the givne registration fee is a real number.

    Parameters
    ----------
    fee : string
        The registration fee.

    Returns
    -------
    bool
        True if the given fee is a real number, False otherwise.
    """
    try:
        float(fee)
    except ValueError:
        return False
    return True


def is_valid_year(year):
    """Checks if the given year is valid.

    Parameters
    ----------
    year : string
        A year.

    Returns
    --------
    bool
        True is the given year is an integer and is current year or higher.

    """

    current_year = date.today().year
    try:
        year = int(year)
    except ValueError:
        year = 0

    return year != 0 and year >= current_year


def is_valid_email_address(email_address):
    """Returns whether the given email address is valid or not.

    Parameters
    ----------
    email_address : string
        An email address.

    Returns
    -------
    bool
        True if the given email address is valid, False otherwise.
    """
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex, email_address)


def username_ok(username):
    """Returns whether the username meets the validity criteria.

    Validity criteria:
    * Username must have 5 characters or more.

    Parameters
    ----------
    username : string
        The username.

    Returns
    -------
    bool
        True if the username meets the validity criteria, False otherwise.
    """

    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    return len(username) >= 5
    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    ##############################################################################


def password_ok(password):
    """Returns whether the password meets the validity criteria.

    Validity criteria:
    * Password must have 5 characters or more.
    * Password must contain at least one capital letter.
    * Password must contain at least one digit.
    * Password must contain at least one symbol character (@,!,#,$)

    Parameters
    ----------
    password : string
        The password.

    Returns
    -------
    bool
        True if the password meets the validity criteria, False otherwise.
    """

    ################ TODO: WRITE HERE THE CODE OF THE FUNCTION ##################
    return len(password) >= 5 and \
        not password.islower() and \
        any(char.isdigit() for char in password) and \
        any(char in ['@', '!', '#', '$'] for char in password)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE.
    #raise NotImplementedError

    ##############################################################################


# When we execute this script, tests are run on the function implemented in this
# module.
if __name__ == "__main__":

    try:
        config = load_config()
        assert config["app"] == "PistusResa" \
            and (config["lang"] == "en" or config["lang"] == "fr") \
            and config["db"] == "./data/pistus.db" \
            and config["bundle"] == "./config/messages_bundle_" \
            and (config["auth"] == "yes" or config["auth"] == "no")

        messages_bundle = load_messages_bundle(
            config["bundle"] + config["lang"])
        assert len(messages_bundle) == 63 \
            and (messages_bundle["add_registration"] == "Add registration" or
                 messages_bundle["add_registration"] == "Ajouter une inscription")
        print("YOUR IMPLEMENTATION OF load_config() AND load_messages_bundle() IS CORRECT!")
    except NotImplementedError:
        pass

    try:
        # Test username_ok
        assert not username_ok(
            "nick"), "when len(username)<5, username_ok() must return False"
        assert username_ok(
            "nickname"), "when len(username)>=5, username_ok() must return True"

        # Test password_ok
        assert not password_ok("mdp"), "password(\"mdp\") must return False"
        assert not password_ok(
            "mdpasse"), "password(\"mdpasse\") must return False"
        assert not password_ok(
            "mDpasse"), "password(\"mdpasse\") must return False"
        assert not password_ok(
            "mDpass3"), "password(\"mdpasse\") must return False"
        assert password_ok("mDp@ss3"), "password(\"mdpasse\") must return True"

        print("YOUR IMPLEMENTATION OF username_ok() AND password_ok() IS CORRECT!")
    except NotImplementedError:
        pass
