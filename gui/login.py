"""The login window.

Follow the instructions in the comments in order to create the login window.

READ THE CODE FROM TOP TO BOTTOM in order to read all the comments and understand the instructions.

"""

# Import the tkinter widgets.
import tkinter as tk
from tkinter import ttk

# Import the configuration of the PistusResa GUI.
import gui.gui_config as config

# Import the function open_main_window. This will be called if the login succeeds.
from gui.mainwindow import open_main_window

# Import the authentication module. This is used to check whether the username and the password
# are correct. For now, login and password are considered as correct if they're both "admin".
# We'll implement a more sophisticated version of the authorization module later.
import authentication as auth

# Import the utility functions.
import utils


"""
INSTRUCTION: The definition of global variables goes here. 
You can add as many as you need for the realization of the window.
"""

# The messages bundle.
messages_bundle = {}

# The language of the interface.
lang = None

# The object used to query the database.
cursor = None

# The object used to connect to the database.
conn = None

# The root window.
window = None

# The entries in the login window.
entries = {}

# The control labels in the login window.
control_labels = {}

# The buttons in the login window.
buttons = {}


def open_login_window(_cursor, _conn, _messages_bundle, _lang):
    """Opens a new login window.

    This is the function that is called from file pistus.py to open the login window.
    THIS FUNCTION IS ALREADY IMPLEMENTED, BUT READ THE CODE AND THE COMMENTS TO UNDERSTAND WHAT IT DOES

    Parameters
    ----------
    _cursor : 
        The object used to query the database.
    _conn : 
        The object used to connect to the database.
    _messages_bundle : dictionary
        The messages bundle.
    _lang : string
        The language of the interface.
    """
    global messages_bundle
    global cursor
    global conn
    global window
    global lang

    # We assign the passed arguments to the global variables.
    messages_bundle = _messages_bundle
    cursor = _cursor
    conn = _conn
    lang = _lang

    # Creates the login window.
    window = tk.Tk()

    # Assigns a title to the window
    # NOTE: we don't hard-code the title, but instead we refer to it by using its key in the messages
    # bundle.
    window.title(messages_bundle["authentication_title"])

    # Load the icon image of the application.
    # This function is already implemented in the file ./gui/gui_config.py
    icon = config.load_icon_image()

    # Assigns the icon to the window.
    # If you're on Windows, the icon will appear next to the title in the title bar.
    # If you're on MacOS, the icon  will appear in the dock (the bar at the bottom of the
    # screen showing the application icons).
    # The same instruction is interpreted in two different ways by the underlying windows managers.
    # This is a good example of how complicated is to provide a cross-platform widget toolkit!
    window.iconphoto(False, icon)

    # Set the window as non-resizable.
    window.resizable(False, False)

    # We configure the style of the window.
    config.configure_style()

    # We create a frame inside the window. This frame will contain all the widgets of the window.
    root_frame = ttk.Frame(window, style="Tab.TFrame")

    # We add a frame, called the credentials frame, that will contain:
    #
    # * The label "Username".
    # * The text field to enter the username.
    # * The label "Password".
    # * The text field to enter the password.
    # The parent of this frame is the root frame.
    credentials_frm = ttk.Frame(root_frame, style="Tab.TFrame")

    # Call the function that creates the widgets in the credentials frame.
    # This function is defined below in this file and you'll have to implement it.
    _credentials_frm_widgets(credentials_frm)

    # Create the message frame that will contain the label displaying messages
    # to the user (in the figure, that's the label with the text "Enter the username (at least 5 characters)").
    message_frm = ttk.Frame(root_frame, style="Tab.TFrame")

    # Call the function that creates the widgets in the message frame.
    # This function is defined below in this file and you'll have to implement it.
    _message_frm_widgets(message_frm)

    # Creates the buttons frame. This frame will contain the buttons at the bottom of the
    # window.
    buttons_frm = ttk.Frame(root_frame, style="Tab.TFrame")

    # Call the function that creates the widgets in the buttons frame.
    # This function is defined below in this file and you'll have to implement it.
    _buttons_frm_widgets(buttons_frm)

    # Adds the credentials, message and buttons frames to the root frame.
    # We add some extra space between them, so as to make the interface prettier.
    credentials_frm.pack(fill="both", expand=True, padx=20, pady=10)
    message_frm.pack(fill="both", expand=True, padx=20, pady=10)
    buttons_frm.pack(fill="both", expand=True, padx=20, pady=10)

    # Adds the root frame to the window.
    root_frame.pack()

    # The login window is initially in the state INIT
    init_state()

    # Starts the event loop.
    window.mainloop()


def _credentials_frm_widgets(credentials_frm):
    """Creates the widgets in the credentials frame.

    The credentials frame will have to contain:

     * The label "Username".
     * The text field to enter the username.
     * The label "Password".
     * The text field to enter the password.

    Parameters
    ----------
    credentials_frm : ttk.Frame
        The credentials frame.
    """

    # The text of the label "Username".
    username_lbl_text = messages_bundle["username"]

    # The text of the label "password".
    password_lbl_text = messages_bundle["password"]

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    # Adds the label "username"
    ttk.Label(credentials_frm, text=username_lbl_text)\
        .grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Adds the text field "username"
    username_ent_var = tk.StringVar("")
    username_ent = ttk.Entry(credentials_frm, textvariable=username_ent_var)
    username_ent.grid(row=0, column=1, sticky='ew')
    entries["username"] = (username_ent, username_ent_var)

    # Adds the label "password".
    ttk.Label(credentials_frm, text=password_lbl_text).grid(
        row=1, padx=10, pady=10, column=0, sticky="W")

    # Adds the text field "password".
    password_ent_var = tk.StringVar("")
    password_ent = ttk.Entry(credentials_frm, show='*',
                             textvariable=password_ent_var)
    password_ent.grid(row=1, column=1, sticky='ew')
    entries["password"] = (password_ent, password_ent_var)

    # The text fields will span the entire column.
    credentials_frm.columnconfigure(1, weight=1)

    username_ent_var.trace("w", username_updated)
    password_ent_var.trace("w", password_updated)

    # TIP: when you create the text field to enter the password, you can use the argument
    # show='*' of ttk.Entry() in order to hide the password while the user types it.

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def _message_frm_widgets(message_frm):
    """Creates the widgets in the message frame.

    This frame will contain the label used to display messages to the user.

    Parameters
    ----------
    message_frm : ttk.Frame
        The message frame.
    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    message_lbl = ttk.Label(message_frm, style="Check.TLabel")
    message_lbl.grid(row=0, column=0, sticky='ew')
    control_labels["message_ctrl"] = message_lbl

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def _buttons_frm_widgets(buttons_frm):
    """Creates the widgets in the buttons frame.

    This frame will contain the buttons at the bottom of the window.

    Parameters
    ----------
    buttons_frm : ttk.Frame
        The buttons frame.
    """

    # Text in the button "Login".
    login_btn_text = messages_bundle["login"]

    # Text in the button clear.
    clear_btn_text = messages_bundle["clear_button"]

    # Text in the button cancel.
    cancel_btn_text = messages_bundle["cancel_button"]

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    buttons_frm.columnconfigure(0, weight=1)

    # Creates and adds the login button.
    login_btn = ttk.Button(buttons_frm, text=login_btn_text)
    login_btn.grid(row=0, column=0, padx=10, sticky='ew')
    buttons["login"] = login_btn

    # Creates and adds the clear button.
    clear_btn = ttk.Button(buttons_frm, text=clear_btn_text)
    clear_btn.grid(row=0, column=1, padx=10, sticky='ew')
    buttons["clear"] = clear_btn

    # Creates and adds the cancel button.
    cancel_btn = ttk.Button(buttons_frm, text=cancel_btn_text)
    cancel_btn.grid(row=0, column=2, padx=10, sticky='ew')
    buttons["cancel"] = cancel_btn

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def init_state():
    """Sets the state of the widgets in the INIT_STATE.

    The password text field and the login button are disabled.
    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    entries["username"][0].configure(state=["!disabled"])
    entries["password"][0].configure(state=["disabled"])
    buttons["login"].configure(state=["disabled"])
    control_labels["message_ctrl"].configure(
        text=messages_bundle["enter_username"])

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def username_entered_state():
    """Sets the state of the widgets in the USERNAME_ENTERED_STATE.

    The login button is disabled.
    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    entries["username"][0].configure(state=["!disabled"])
    entries["password"][0].configure(state=["!disabled"])
    buttons["login"].configure(state=["disabled"])
    control_labels["message_ctrl"].configure(
        text=messages_bundle["enter_password"])

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def credentials_entered_state(message):
    """Sets the state of the widgets in the CREDENTIALS_ENTERED_STATE

    All widgets are enabled and the given message is written in the control label.

    Parameters
    ----------
    message: string
    The message to show in the control label.

    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    entries["username"][0].configure(state=["!disabled"])
    entries["password"][0].configure(state=["!disabled"])
    buttons["login"].configure(state=["!disabled"])
    control_labels["message_ctrl"].configure(text=message)

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def get_username():
    """Returns the current value of the username.

    Returns
    -------
    string
        The current value of the username text field.
    """
    return entries["username"][1].get().strip()


def get_password():
    """Returns the current value of the password.

    Returns
    -------
    string
        The current value of the password text field.
    """
    return entries["password"][1].get().strip()


def username_updated(*args):
    """Invoked when the user is typing the username.

    This function checks whether the current value in the username text field meets the validity
    constraints. Depeding on the result of the validity check and the current state, the window will
    transition to the appropriate state.

    Parameters
    ----------
    args :
        Arguments passed to the function by Tkinter when it is invoked as a callback.
        You can ignore them.

    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    if utils.username_ok(get_username()):
        if not utils.password_ok(get_password()):
            username_entered_state()
        else:
            credentials_entered_state(messages_bundle["login_authorized"])
    else:
        init_state()

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def password_updated(*args):
    """Invoked when the user is typing the password.

    This function checks whether the current value in the password text field meets the validity
    constraints. Depeding on the result of the validity check and the current state, the window will
    transition to the appropriate state.

    Parameters
    ----------
    args :
        Arguments passed to the function by Tkinter when it is invoked as a callback.
        You can ignore them.

    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    if utils.password_ok(get_password()):
        if not utils.username_ok(get_username()):
            init_state()
        else:
            credentials_entered_state(messages_bundle["login_authorized"])
    else:
        if not utils.username_ok(get_username()):
            init_state()
        else:
            username_entered_state()

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def login():
    """Invoked when the user clicks on the button Login.

    The function calls auth.login_correct() to check whether the username and password typed by the user are correct.
    The function auth.login_correct() takes in as arguments:
    * The username
    * The password
    * The cursor (not used in the current implementation of the function, it will be used when we implement 
    the authentication module).

    The function returns a tuple:
    * (True, None, None) if the username and the password are correct (in the current implementation, the only correct
    combinatio is ("admin", "Adm1n!") ).

    * (False, USERNAME_NOT_FOUND, username) if the username doesn't exist.

    * (False, INCORRECT_PASSWORD, password) if the password is not correct.

    Use the return value of this function to take the proper action.
    """
    res = auth.login_correct(get_username(), get_password(), cursor)

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    res = auth.login_correct(get_username(), get_password(), cursor)

    if res[0]:
        window.destroy()
        open_main_window(cursor, conn, messages_bundle, lang)
    elif res[1] == auth.INCORRECT_PASSWORD:
        credentials_entered_state(messages_bundle["incorrect_password"])
    elif res[1] == auth.USERNAME_NOT_FOUND:
        credentials_entered_state(messages_bundle["username_not_found"])

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def clear():
    """Invoked when the user clicks on the button Clear.

    This function needs to clear the text fields and return to the state INIT
    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    entries["username"][1].set("")
    entries["password"][1].set("")

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def cancel():
    """Invoked when the user clicks on the button Cancel.

    """

    ############ TODO: WRITE HERE THE CODE TO IMPLEMENT THIS FUNCTION ##########
    clear()
    window.destroy()

    # REMOVE THIS INSTRUCTION WHEN YOU WRITE YOUR CODE
    # pass

    ####################################################################################


def get_username():
    """Returns the current value of the username.

    Returns
    -------
    string
        The current value of the username text field.
    """
    return entries["username"][1].get().strip()


def get_password():
    """Returns the current value of the password.

    Returns
    -------
    string
        The current value of the password text field.
    """
    return entries["password"][1].get().strip()
