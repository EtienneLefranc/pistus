"""Functions associated with the new registration tab.

In this file, we define all the functions that are used to 
create the new registration tab and make it react to events.
All the callbacks associated to users' actions on the new registration tab are
defined here.
"""

import mstudent as mstud
import mregistration as mreg
import utils

# Here we store all the different widgets of the student tab.
control_labels = {}
entries = {}
buttons = {}

# Event that occurs when a registration is successfully added to the database.
REGISTRATION_ADDED_EVENT = 0

# Number of mandatory fields in the new registration tab.
# Each mandatory field is associated to a numeric code.
nb_mandatory_fields = 6
STUD_NUMBER = 0
YEAR = 1
REGISTRATION_DATE = 2
FIRST_NAME = 3
LAST_NAME = 4
REGISTRATION_FEE = 5

# Bit vector associated to the mandatory fields in the new registration tab.
# Each mandatory field is assigned a value: 1 if the mandatory field is 
# correctly filled by the user, 0 otherwise. 
# The position in the array of the value assigned to a field is given by 
# the numeric code of the field.
# For instance, filled_mandatory_fields[STUD_NUMBER] = 0 means that the user 
# did not specify the student number as required.
filled_mandatory_fields = [0 for i in range(nb_mandatory_fields)]

# Depending on the user's actions, the new registration tab might 
# be in one of several states; the appearance of the interface changes depending 
# on the state. 
# In the INIT state, the button Add is disabled
# because the user hasn't filled the student data fields yet.
INIT_STATE = 0
# In the ADD state, all mandatory fields are correctly filled in and 
# the add button must be enabled.
ADD_STATE =  1
# In the REGISTRATION_ADDED state, a new registration has been added to the database.
# All fields are disabled and a positive message is displayed in the message area.
REGISTRATION_ADDED_STATE = 2

# Initially, we are in the INIT state.
current_state = INIT_STATE

# This variable is set to True when the payment date format is correct.
# The variable is True even if the payment date is empty (this is not a mandatory field).
payment_date_ok = True

# The dictionary containing all the messages shown in the GUI.
messages_bundle = {}

# The image used to indicate that a field contains a correct value.
check_image = None

# Reference to the new registration tab.
new_reg_tab = None

# The object used to query the database.
cursor = None

# The object used to connect to the database.
conn = None

def init(_messages_bundle, _check_image, _new_reg_tab, _cursor, _conn):
    """Initializes some of the global variables defined in the file.

    Parameters
    ----------
    _messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    _check_image : ImageTk.PhotoImage
        The image used to indicate that a field contains a correct value.
    _new_reg_tab : ttk.Frame
        The new registration tab.
    _cursor : 
        The object used to query the database.
    _conn : 
        The object used to connect to the database.
    """

    global messages_bundle
    global check_image
    global new_reg_tab
    global cursor
    global conn

    messages_bundle = _messages_bundle
    check_image = _check_image
    new_reg_tab = _new_reg_tab
    cursor = _cursor
    conn = _conn

def reset():
    """Resets some of the global variables defined in this file.

    This function is invoked when clearing all the fields in the new registration tab.
    """
    global filled_mandatory_fields
    
    filled_mandatory_fields = [0 for i in range(nb_mandatory_fields)]
    transition()
    reset_control_label()

def reset_control_label(lbl="all"):
    """Resets the values in the control labels.

    Parameters
    ----------
    lbl : string
        The key associated to the control label to reset (Default: "all", to reset all control labels).
    """

    if lbl == "all" or lbl == "stud_number_ctrl":
        control_labels["stud_number_ctrl"].configure(image = "", text=messages_bundle["enter_identifier"])
    
    if lbl == "all" or lbl == "year_ctrl":
        control_labels["year_ctrl"].configure(image = "", text=messages_bundle["enter_year"])

    if lbl == "all" or lbl == "registration_fee_ctrl":
        control_labels["registration_fee_ctrl"].configure(image = "", text=messages_bundle["enter_registration_fee"])
    
    if lbl == "all" or lbl == "registration_date_ctrl":
        control_labels["registration_date_ctrl"].configure(image = "", text=messages_bundle["enter_date"])
    
    if lbl == "payment_date_ctrl":
        control_labels["payment_date_ctrl"].configure(image = "", text="")

    if lbl == "all" or lbl == "message_area_ctrl":
        control_labels["message_ctrl"].configure(text="")

def init_state():
    """Sets the state of the widgets in the state INIT_STATE
    """
    global current_state

    current_state = INIT_STATE
    # Enable all widgets, except the add button (and first and last names, that will be automatically filled in).
    entries["stud_number"][0].state(["!disabled"])
    entries["year"][0].state(["!disabled"])
    entries["registration_fee"][0].state(["!disabled"])
    entries["registration_date"][0].state(["!disabled"])
    entries["payment_date"][0].state(["!disabled"])
    buttons["add_btn"].state(["disabled"])  

def add_state():
    """Sets the state of the widgets in the state ADD_STATE
    """

    global current_state

    current_state = ADD_STATE
    # We enable the add button.
    buttons["add_btn"].state(["!disabled"])

def registration_added_state():
    """Sets the state of the widgets in the state REGISTRATION_ADDED_STATE
    """
    global current_state

    current_state = REGISTRATION_ADDED_STATE
    # We disable all the widgets, except the clear and cancel buttons.
    entries["stud_number"][0].state(["disabled"])
    entries["year"][0].state(["disabled"])
    entries["registration_fee"][0].state(["disabled"])
    entries["registration_date"][0].state(["disabled"])
    entries["payment_date"][0].state(["disabled"])
    buttons["add_btn"].state(["disabled"])  

def transition(event=None):
    """Defines the transitions between the states.

    Parameters
    ----------
    event : string
        The event that triggers the transition (default: None)
    """
    if mandatory_fields_ok() and payment_date_ok:
        if current_state == INIT_STATE:
            add_state()
        elif current_state == ADD_STATE and event == REGISTRATION_ADDED_EVENT:
            registration_added_state()
    else:
        init_state()

def mandatory_fields_ok():
    """Checks whether the mandatory fields have been correctly filled.

    Returns
    -------
    bool
        True if all the mandatory fields have been correctly filled, False otherwise.

    """
    return sum(filled_mandatory_fields) == nb_mandatory_fields

def clear_fields_student_except_stud_number():
    """Clears all the fields relative to the student except the student number.
    """
    set_first_name("")
    set_last_name("")

def clear_fields_student():
    """Clears all the fields relative to the student.
    """
    set_stud_number("")
    clear_fields_student_except_stud_number()

def clear_fields():
    """Clears all the data fields.
    """
    clear_fields_student()
    set_year("")
    set_registration_date("")
    set_registration_fee("")
    set_payment_date("")

def stud_number_updated():
    """Invoked when the student number is updated.
    """
    stud_number = get_stud_number()
    # If the student number has been filled in, we check that it's correct.
    if len(stud_number) > 0:
        # The student number must be composed of digits only.
        if not stud_number.isdigit():
            control_labels["stud_number_ctrl"].configure(text=messages_bundle["invalid_identifier"], image = "")
            filled_mandatory_fields[STUD_NUMBER] = 0
        else:  # everything is OK.
            control_labels["stud_number_ctrl"].configure(text="", image = check_image)
            control_labels["stud_number_ctrl"].image=check_image
            filled_mandatory_fields[STUD_NUMBER] = 1
    else: # No student number has been specified.
        reset_control_label(lbl="stud_number_ctrl")
        filled_mandatory_fields[STUD_NUMBER] = 0
    transition()

def year_updated():
    """Invoked when the year is updated.
    """
    year = get_year()
    # The year has been specified.
    if len(year) > 0:
        # Not a valid year.
        if not utils.is_valid_year(year):
            control_labels["year_ctrl"].configure(text=messages_bundle["invalid_year"], image = "")
            filled_mandatory_fields[YEAR] = 0
        else: # The year is correct.
            # The registration year must be the edition year - 1
            if not utils.check_registration_year(get_registration_date(), int(year)):
                control_labels["registration_date_ctrl"].configure(\
                    text=messages_bundle["invalid_registration_date"] + str(int(year)-1), image = "")
                filled_mandatory_fields[REGISTRATION_DATE] = 0
            else: # if the registation year is correct, then we must refresh the registration date. 
                # Little hack to force the control label associated to the registration date 
                 # to refresh.
                set_registration_date(get_registration_date())
            control_labels["year_ctrl"].configure(text="", image = check_image)
            control_labels["year_ctrl"].image=check_image
            filled_mandatory_fields[YEAR] = 1
    else: # no year has been specified.
        reset_control_label(lbl="year_ctrl")
        filled_mandatory_fields[YEAR] = 0
    transition()

def registration_fee_updated():
    """Invoked when the registration fee is updated.
    """
    registration_fee = get_registration_fee()
    # No registration fee specified.
    if len(registration_fee) > 0:
        # The registration fee is not correct.
        if not utils.is_valid_fee(registration_fee):
            control_labels["registration_fee_ctrl"].configure(text=messages_bundle["invalid_registration_fee"], image = "")
            filled_mandatory_fields[REGISTRATION_FEE] = 0
        else: # everything is OK.
            control_labels["registration_fee_ctrl"].configure(text="", image = check_image)
            control_labels["registration_fee_ctrl"].image=check_image
            filled_mandatory_fields[REGISTRATION_FEE] = 1   
    else: # no registration fee specified.
        reset_control_label(lbl="registation_fee_ctrl")
        filled_mandatory_fields[REGISTRATION_FEE] = 0
    transition()

def registration_date_updated():
    """Invoked when the registration date is updated.
    """
    global payment_date_ok
    date = get_registration_date()
    year = get_year()
    # If the date is specified
    if len(date) > 0:
        # The date is not in the correct format.
        if not utils.is_valid_date(date, empty=False):
            control_labels["registration_date_ctrl"].configure(text=messages_bundle["invalid_date"], image = "")
            filled_mandatory_fields[REGISTRATION_DATE] = 0
            # The registration year must be edition year - 1 
        elif len(year) > 0 and not utils.check_registration_year(get_registration_date(), int(year)):
            control_labels["registration_date_ctrl"].configure(\
                text=messages_bundle["invalid_registration_date"] + str(int(year)-1), image = "")
            filled_mandatory_fields[REGISTRATION_DATE] = 0
        else: # registration date is OK
            # The payment must occurs the same day as the registration or later.
            if not utils.payment_date_after_registration(get_payment_date(), date):
                control_labels["payment_date_ctrl"].configure(text=messages_bundle["invalid_payment_date"], image = "")
                payment_date_ok = False
            else: # The payment date is consistent.
                # Little hack to force the control label associated to the payment date 
                # to refresh.
                set_payment_date(get_payment_date())
            control_labels["registration_date_ctrl"].configure(text="", image = check_image)
            control_labels["registration_date_ctrl"].image=check_image
            filled_mandatory_fields[REGISTRATION_DATE] = 1
            if not payment_date_ok and utils.is_valid_date(get_payment_date()):
                payment_date_ok = True
    else: # no registration date specified.
        reset_control_label(lbl="registration_date_ctrl")
        filled_mandatory_fields[REGISTRATION_DATE] = 0
    transition()

def payment_date_updated():
    """Invoked when  the payment date is updated.
    """
    global payment_date_ok
    payment_date = get_payment_date()
    # Payment date specified.
    if len(payment_date) > 0:
        # The date is not in the right format.
        if not utils.is_valid_date(payment_date):
            control_labels["payment_date_ctrl"].configure(text=messages_bundle["invalid_date"], image = "")
            payment_date_ok = False
        # The payment date is not greater than the registration date.
        elif not utils.payment_date_after_registration(payment_date, get_registration_date()):
            control_labels["payment_date_ctrl"].configure(text=messages_bundle["invalid_payment_date"], image = "")
            payment_date_ok = False
        else: # Everything is OK.
            control_labels["payment_date_ctrl"].configure(text="", image = check_image)
            control_labels["payment_date_ctrl"].image=check_image
            payment_date_ok = True
    else: # No payment date specified.
        reset_control_label(lbl="payment_date_ctrl")
        payment_date_ok = True
    transition()

def find_pistus_edition(event):
    """Invoked when the user specifies an edition year.
    This functions looks if a Pistus edition in the specified year exists in the database;
    if so, it fills in the field "registration fee".
    """
    year = get_year()
    edition = mreg.get_pistus_edition(year, cursor)
    if not edition:
        set_registration_fee("")
        entries["registration_fee"][0].state(["!disabled"])
    else:
        set_registration_fee(edition[1])
        entries["registration_fee"][0].state(["disabled"])

def find_student(event):
    """Invoked when the student specifies a student number and presses the <Tab> key.

    This function looks for a student with the specified number in the database. If 
    a student is found, the other data fields (first and last name) are filled with the values loaded from the 
    database.

    Parameters
    ----------
    event
        The event information.
    """
    # Get the student from the database.
    stud_number = get_stud_number()
    student = mstud.get_student(stud_number, cursor)

    if student is None:
        write_message(messages_bundle["unexpected_error"])
        return

    # Clear all fields except the student number
    clear_fields_student_except_stud_number()

    # If the student exists, first and family names are filled in automatically.
    if student:
        set_first_name(student[1])
        set_last_name(student[2])
        filled_mandatory_fields[FIRST_NAME] = 1
        filled_mandatory_fields[LAST_NAME] = 1
    else: # We display an error message on the control label associated with the student number text field.
        control_labels["stud_number_ctrl"].configure(text=messages_bundle["student_not_found"], image = "")
        filled_mandatory_fields[FIRST_NAME] = 0
        filled_mandatory_fields[LAST_NAME] = 0
    
    transition()

def add_registration():
    """Adds a new registration to the database. Invoked when the user clicks on the 
    button Add.
    """
    stud_number = get_stud_number()
    year = get_year()
    registration_fee = get_registration_fee()
    registration_date = get_registration_date()
    payment_date = get_payment_date()

    cursor.execute("BEGIN")
    # If there's no Pistus edition in the specified year, we add one to the database.
    if not mreg.get_pistus_edition(year, cursor):
        res = mreg.add_pistus_edition(year, registration_fee, cursor)
        if not res[0]:
            write_message(messages_bundle["unexpected_error"] + res[2])
    
    # We add the registration.
    res = None
    if len(payment_date) == 0:
        res = mreg.add_registration(stud_number, year, registration_date, cursor)
    else:
        res = mreg.add_registration(stud_number, year, registration_date, cursor, payment_date=payment_date)

    if res[0]:
        conn.commit()
        write_message(messages_bundle["registration_added"])
        transition(event=REGISTRATION_ADDED_EVENT)
    else: # else we rollback the transaction, the modifications are not written to the database.
        if res[1] == mreg.UNEXPECTED_ERROR:
            write_message(messages_bundle["unexpected_error"])
        elif res[1] == mreg.DUPLICATE_REGISTRATION_ERROR:
            write_message(messages_bundle["duplicate_registration"] + res[2])
        conn.rollback()

def cancel_action():
    """Invoked when the user clicks on the button Cancel.
    """
    reset()
    new_reg_tab.destroy()

def clear_action():
    """Invoked when the user clicks on the button Clear.
    """
    reset()
    clear_fields()

def add_stud_number_control_label(label):
    """Adds the student number control label.

    Parameters
    ----------
    label : ttk.Label
        The control label.
    """
    control_labels["stud_number_ctrl"] = label

def add_year_control_label(label):
    """Adds the edition year control label.

    Parameters
    ----------
    label : ttk.Label
        The control label.
    """
    control_labels["year_ctrl"] = label

def add_registration_fee_control_label(label):
    """Adds the registration fee control label.

    Parameters
    ----------
    label : ttk.Label
        The control label.
    """
    control_labels["registration_fee_ctrl"] = label

def add_registration_date_control_label(label):
    """Adds the registration date control label.

    Parameters
    ----------
    label : ttk.Label
        The control label.
    """
    control_labels["registration_date_ctrl"] = label

def add_payment_date_control_label(label):
    """Adds the payment date control label.

    Parameters
    ----------
    label : ttk.Label
        The control label.
    """
    control_labels["payment_date_ctrl"] = label

def add_message_area_control_label(label):
    """Adds the message area control label.

    Parameters
    ----------
    label : ttk.Label
        The control label.
    """
    control_labels["message_ctrl"] = label

def add_stud_number_entry(entry):
    """Adds the student number entry.

    Parameters
    ----------
    entry : (ttk.Entry, tk.StringVar)
        The student number entry and the text variable contaning the current value of the entry.
    """
    entries["stud_number"] = entry

def add_first_name_entry(entry):
    """Adds the first name entry.

    Parameters
    ----------
    entry : (ttk.Entry, tk.StringVar)
        The first name entry and the text variable contaning the current value of the entry.
    """
    entries["first_name"] = entry

def add_last_name_entry(entry):
    """Adds the last name entry.

    Parameters
    ----------
    entry : (ttk.Entry, tk.StringVar)
        The last name entry and the text variable contaning the current value of the entry.
    """
    entries["last_name"] = entry

def add_year_entry(entry):
    """Adds the edition year entry.

    Parameters
    ----------
    entry : (ttk.Entry, tk.StringVar)
        The edition year entry and the text variable contaning the current value of the entry.
    """
    entries["year"] = entry

def add_registration_fee_entry(entry):
    """Adds the registration fee entry.

    Parameters
    ----------
    entry : (ttk.Entry, tk.StringVar)
        The registration fee entry and the text variable contaning the current value of the entry.
    """
    entries["registration_fee"] = entry

def add_registration_date_entry(entry):
    """Adds the registration date entry.

    Parameters
    ----------
    entry : (ttk.Entry, tk.StringVar)
        The registration date entry and the text variable contaning the current value of the entry.
    """
    entries["registration_date"] = entry

def add_payment_date_entry(entry):
    """Adds the payment date entry.

    Parameters
    ----------
    entry : (ttk.Entry, tk.StringVar)
        The payment date entry and the text variable contaning the current value of the entry.
    """
    entries["payment_date"] = entry

def add_add_button(button):
    """Adds the button Add.

    Parameters
    ----------
    button : ttk.Button
        The button Add.
    """
    buttons["add_btn"] = button

def add_clear_button(button):
    """Adds the button Clear.

    Parameters
    ----------
    button : ttk.Button
        The button Clear.
    """
    buttons["clear_btn"] = button

def add_cancel_button(button):
    """Adds the button Cancel.

    Parameters
    ----------
    button : ttk.Button
        The button Cancel.
    """
    buttons["cancel_btn"] = button

def get_stud_number():
    """Gets the student number.

    Returns
    -------
    string
        The student number.
    """
    return entries["stud_number"][1].get().strip()

def set_stud_number(stud_number):
    """Sets the student number.

    Parameters
    ----------
    stud_number : string 
        The student number.
    """
    entries["stud_number"][1].set(stud_number)

def get_first_name():
    """Gets the first name.

    Returns
    -------
    string
        The first name.
    """
    return entries["first_name"][1].get().strip()

def set_first_name(first_name):
    """Sets the first name.

    Parameters
    ----------
    first_name : string 
        The first name.
    """
    return entries["first_name"][1].set(first_name)

def get_last_name():
    """Gets the last name.

    Returns
    -------
    string
        The last name.
    """
    return entries["last_name"][1].get().strip()

def set_last_name(last_name):
    """Sets the last name.

    Parameters
    ----------
    last_name : string 
        The last name.
    """
    return entries["last_name"][1].set(last_name)

def get_year():
    """Gets the edition year.

    Returns
    -------
    string
        The edition year.
    """
    return entries["year"][1].get().strip()

def set_year(year):
    """Sets the edition year.

    Parameters
    ----------
    year : string 
        The edition year.
    """
    return entries["year"][1].set(year)

def get_registration_fee():
    """Gets the registration fee.

    Returns
    -------
    float
        The registration fee.
    """
    return entries["registration_fee"][1].get().strip()

def set_registration_fee(registration_fee):
    """Sets the registration fee.

    Parameters
    ----------
    registration_fee : float 
        The registration fee.
    """
    entries["registration_fee"][1].set(registration_fee)

def get_registration_date():
    """Gets the registration date.

    Returns
    -------
    string
        The registration date.
    """
    return entries["registration_date"][1].get().strip()

def set_registration_date(registration_date):
    """Sets the registration date.

    Parameters
    ----------
    registration_date : string 
        The registration date.
    """
    return entries["registration_date"][1].set(registration_date) 

def get_payment_date():
    """Gets the payment date.

    Returns
    -------
    string
        The payment date.
    """
    return entries["payment_date"][1].get().strip()

def set_payment_date(payment_date):
    """Sets the payment date.

    Parameters
    ----------
    payment_date : string 
        The payment date.
    """
    return entries["payment_date"][1].set(payment_date) 

def write_message(message):
    """Write a message in the message area.

    Parameters
    ----------
    message : string
        The message to write.
    """
    control_labels["message_ctrl"].configure(text=message)