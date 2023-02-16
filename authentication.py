"""The authentication module.

"""

from passlib.context import CryptContext
import sqlite3
import utils

# Error code used when a specified username
# doesn't exist in the database.
USERNAME_NOT_FOUND = 1

# Error code used when a specified password is incorrect.
INCORRECT_PASSWORD = 2

# Error code used when trying to create an account that uses an already existing
# username.
DUPLICATE_USERNAME = 3

# Specifying the encryption algorithm used to encrypt the password.
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


def encrypt_password(password):
    """Encrypts the given password.

    Parameters
    ----------
    password : string
        Plain text password.

    Returns
    -------
    string
        The encrypted password.
    """
    return pwd_context.hash(password)


def create_account(username, plain_password, cursor, conn):
    """Creates an account with the given credentials that are stored in the database.

    Parameters
    ----------
    username : string
        The username
    plain_password : string
        The plain text password
    cursor : 
        The object used to query the database
    conn : 
        The object used to connect to the database.

    Returns
    -------
    A tuple.
        (True, None, None) when the account can be successfully created.
        (False, DUPLICATE_USERNAME, username) when trying to create an account with an existing username

    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    # Here are what this function must do:
    #
    # * Encrypt the password.
    # * Try to add the given username and the encrypted password to the database table Login.
    # * Detect the fact that we're trying to add a username that is already in table Login; in this
    # case we rollback the transaction and we return (False, DUPLICATE_USERNAME, username)
    # * If the credentials can be added to the database, commit the transaction and return
    # (True, None, None)
    encrypted_password = encrypt_password(plain_password)
    try:
        cursor.execute("INSERT INTO Login VALUES (?, ?)",
                       (username, encrypted_password))
    except sqlite3.IntegrityError as error:
        print(error)
        conn.rollback()
        return (False, DUPLICATE_USERNAME, username)
    conn.commit()
    return (True, None, None)

    # REMOVE THE FOLLOWING INSTRUCTION WHEN YOU WRITE YOUR CODE
    # return (True, None, None)

    ####################################################################################


def login_correct(username, password, cursor):
    """Checks whether the given credentials are correct.

    Parameters
    ----------
    username : string
        The username
    password : string
        The plain text password.
    cursor: 
        The object used to query the database (unused in this first implementation).

    Returns
    -------
    A tuple
        (True, None, None) if the given username and password are correct.
        (False, USERNAME_NOT_FOUND, username) if the given username does not exist.
        (False, INCORRECT_PASSWORD, password) if the given password is incorrect.

    """

    # CURRENT IMPLEMENTATION THAT ONLY GRANTS ACCESS TO USER admin WITH PASSWORD "Adm1n!"
    # REMOVE THIS CODE WHEN YOU WRITE YOUR IMPLEMENTATION
    # if username != "admin":
    #    return (False, USERNAME_NOT_FOUND, username)
    # elif password != "Adm1n!":
    #    return (False, INCORRECT_PASSWORD, password)
    # else:
    #    return (True, None, None)

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    encrypted_password = None
    cursor.execute("SELECT password FROM Login WHERE username=?", (username,))
    res = cursor.fetchone()
    if res is None:
        return (False, USERNAME_NOT_FOUND, username)
    else:
        encrypted_password = res[0]
    if pwd_context.verify(password, encrypted_password):
        return (True, None, None)
    else:
        return(False, INCORRECT_PASSWORD, None)

    # The function must check whether an account with the given username and password
    # exists in table Login. Remember that the password passed as an argument is not encrypted!
    # REMOVE THE CODE ABOVE WHEN YOU WRITE YOUR IMPLEMENTATION

    ####################################################################################


# Entry point of this module.
# When we execute this file, the following instructions are executed that trigger a procedure to
# create an account.
# The user is prompted to enter the username and the password in the Visual Studio Code terminal;
# the password is encrypted and the credentials are added to the database.
if __name__ == "__main__":

    from utils import load_config
    from utils import load_messages_bundle

    # Loads the configuration of the application.
    config = load_config()

    # Loads the messages bundle in the appropriate language.
    messages_bundle = load_messages_bundle(config["bundle"] + config["lang"])

    # Connects to the database.
    conn = sqlite3.connect(config["db"])

    # Get the cursor for the connection. This object is used to execute queries
    # in the database.
    cursor = conn.cursor()

    # The user is prompted to enter the username until the username
    # meets the validity criteria.
    username = ""
    while not utils.username_ok(username):
        print(messages_bundle["enter_username"])
        username = input()

    # The user is prompted to enter the password until the password
    # meets the validity criteria.
    plain_pwd = ""
    while not utils.password_ok(plain_pwd):
        print(messages_bundle["enter_password"])
        plain_pwd = input()

    # Creation of the account
    res = create_account(username, plain_pwd, cursor, conn)

    # Check if any error occurs.
    if res[0]:
        print(messages_bundle["account_created"])
    elif res[1] == DUPLICATE_USERNAME:
        print(messages_bundle["duplicate_username"])

    # Closes the connection to the database
    cursor.close()
    conn.close()
