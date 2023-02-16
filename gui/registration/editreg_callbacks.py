"""Functions associated with the edit registration tab.

In this file, we define all the functions that are used to 
create the edit registration tab and make it react to events.
All the callbacks associated to users' actions on the edit registration tab are
defined here.
"""

import mstudent as mstud
import mregistration as mreg

import utils
from datetime import datetime
from datetime import date

import tkinter as tk
from tkinter import ttk

# Here we store all the different widgets of the student tab.
control_labels = {}
entries = {}
buttons = {}

# Number of mandatory fields in the new registration tab.
# Each mandatory field is associated to a numeric code.
nb_mandatory_fields = 3
STUD_NUMBER = 0
FIRST_NAME = 1
LAST_NAME = 2

# Bit vector associated to the mandatory fields in the new registration tab.
# Each mandatory field is assigned a value: 1 if the mandatory field is 
# correctly filled by the user, 0 otherwise. 
# The position in the array of the value assigned to a field is given by 
# the numeric code of the field.
# For instance, filled_mandatory_fields[STUD_NUMBER] = 0 means that the user 
# did not specify the student number as required.
filled_mandatory_fields = [0 for i in range(nb_mandatory_fields)]

# Depending on the user's actions, the edit registration tab might 
# be in one of several states; the appearance of the interface changes depending 
# on the state. 
# In the INIT state, the button Edit is disabled
# because the user hasn't filled the student data fields yet.
INIT_STATE = 0
# In the STUDENT_LOADED state, the button Edit is still disabled, because 
# we didn't modify anything yet.
STUDENT_LOADED = 1
# In the DELETE state, the button Delete is enabled because the user has selected 
# at least one registration.
DELETE_STATE = 2
# In the EDIT state, the button Edit is enabled (a student has been loaded from the database and 
# there is something to edit).
EDIT_STATE = 3

# The current state.
current_state = INIT_STATE

# The number of selected rows in the registration list.
# When nb_rows_selected > 0, we transition to the DELETE state.
nb_rows_selected = 0

# When we load from the database the list of all registrations of a student,
# we create a table, where each cell contains a widget (a label, a text entry or a check button).
# All the widgets are stored in this list.
# Specifically, each item of the list is a tuple that contains the widgets on one row of the table.
#
# The first item is a tuple (ttk.Checkbutton, ttk.Label, ttk.Label, ttk.Label).
# The check button is used to select all rows in the table; the three labels contain the headers 
# of the table (edition year, registration date and payment date).
#
# Each subsequent item is a tuple (ttk.Checkbutton, ttk.Entry, ttk.Entry, ttk.Entry);
# the check button is used to select the corresponding row; the three entries contain
# the edition year, the registration and payment date of a registration.
registration_data = []

# It contains all the variables that track the current value of the widgets stored in 
# registration_data.
# registration_data_var[i][j] is the variable with the current value of the widget 
# registration_data[i][j]
registration_data_var = []

# It contains the registrations of the current student as they are loaded from the database.
# The values in registration_data_var reflect the changes of the user; 
# the values in current_student_registrations reflect the original values.
# By comparing registration_data_var against current_student_registrations we know if 
# some values have been changed, which justifies a transition to the EDIT state.
# 
# Each item of this list contains a tuple (a registratiion) with three values: edition year, registration date,
# payment_date. 
# The registration current_student_registrations[i] corresponds to the registration 
# registration_data_var[i]. 
# Note that since registration_data_var contains some header values in the first position, 
# the first item in current_student_registrations is ("", "", ""); this way a registration 
# is stored at the same index in both lists.
current_student_registrations = [("", "", "")]

# The dictionary containing all the messages shown in the GUI.
messages_bundle = {}

# The image used to indicate that a field contains a correct value.
check_image = None

# Reference to the edit registration tab.
edit_reg_tab = None

# Reference to the frame that contains the table withe registrations of the current student.
scroll_registration_frm = None

# The object used to query the database.
cursor = None

# The object used to connect to the database.
conn = None

def init(_messages_bundle, _check_image, _edit_reg_tab, _scroll_registration_frm, _cursor, _conn):
    """Initializes some of the global variables defined in the file.

    Parameters
    ----------
    _messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    _check_image : ImageTk.PhotoImage
        The image used to indicate that a field contains a correct value.
    _edit_reg_tab : ttk.Frame
        The edit registration tab.
    _cursor : 
        The object used to query the database.
    _conn : 
        The object used to connect to the database.
    """
    global messages_bundle
    global check_image
    global edit_reg_tab
    global scroll_registration_frm
    global cursor
    global conn

    messages_bundle = _messages_bundle
    check_image = _check_image
    edit_reg_tab = _edit_reg_tab
    scroll_registration_frm = _scroll_registration_frm
    cursor = _cursor
    conn = _conn

def reset():
    """Resets some of the global variables defined in this file.

    This function is invoked when clearing all the fields in the new registration tab.
    """
    global filled_mandatory_fields
    global current_student_registrations
    global nb_rows_selected
    
    filled_mandatory_fields = [0 for i in range(nb_mandatory_fields)]
    current_student_registrations = [("", "", "")]
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
    if lbl == "all" or lbl == "message_ctrl":
        control_labels["message_ctrl"].configure(text=" \n ")

def init_state():
    """Sets the state of the widgets in the state INIT_STATE
    """
    global current_state

    current_state = INIT_STATE
    # We disable the buttons Edit and Delete.
    buttons["edit_btn"].state(["disabled"])
    reset_control_label("message_ctrl")
    buttons["delete_btn"].state(["disabled"])
    # We enable the student number entry (we let the user specify a student number).
    entries["stud_number"][0].state(["!disabled"])

def student_loaded_state(_are_dates_ok):
    """Sets the state of the widgets in the state STUDENT_LOADED.

    Parameters
    ----------
    _are_dates_ok : bool
        True if all dates are OK.
    """
    global current_state

    current_state= STUDENT_LOADED
    # If some dates are not ok, an error is shown in the message area.
    if not _are_dates_ok:
        write_message(
            messages_bundle["edit_reg_date_format_error"] + \
            messages_bundle["edit_reg_payment_error"] + "\n" + \
            messages_bundle["edit_reg_registration_error"]
        )
    
    # We disable the button Edit and the student number text field.
    # The second is particularly important to avoid that the user 
    # modifies the registrations of the current student by specifying the 
    # number of another student.
    buttons["edit_btn"].state(["disabled"])
    buttons["delete_btn"].state(["disabled"])
    entries["stud_number"][0].state(["disabled"])

def edit_state():
    """Sets the state of the widgets in the state EDIT.
    """
    global current_state

    current_state = EDIT_STATE
    # We enable the button Edit
    buttons["edit_btn"].state(["!disabled"])
    buttons["delete_btn"].state(["disabled"])
    reset_control_label(lbl = "message_ctrl")

def delete_state():
    """Sets the state of the widgets in the state DELETE.
    """
    global current_state

    current_state = DELETE_STATE
    # We enable the button Delete and we disable the button Edit.
    buttons["delete_btn"].state(["!disabled"])
    buttons["edit_btn"].state(["disabled"])

def transition():
    """Defines the transitions between the states.
    """
    # All mandatory fields have been correctly filled in.
    if mandatory_fields_ok():
        # If we are in the INIT state, we transition to
        # the STUDENT_LOADED state, and all dates are OK (we assume the data in the db are OK).
        if current_state == INIT_STATE:
            student_loaded_state(True)
        # Whatever state we are in, if the user selects at least one row we transition to the 
        # DELETE state.
        elif nb_rows_selected > 0:
            delete_state()
        # If we are in the STUDENT_LOADED state
        elif current_state == STUDENT_LOADED:
            _are_dates_ok = are_dates_ok()
            # If dates are OK and there is something to edit, we transition to the EDIT state.
            if _are_dates_ok and something_to_edit():
                edit_state()
            else: # Otherwise we stay in the STUDENT_LOADED state, with possibly an error message if 
                # the dates are not OK.
                student_loaded_state(_are_dates_ok)
        # If we are in the EDIT state
        elif current_state == EDIT_STATE:
            _are_dates_ok =  are_dates_ok()
            # If the dates are not OK, or there is nothing to edit, we transition to 
            # the STUDENT_LOADED state.
            if not _are_dates_ok or not something_to_edit():
                student_loaded_state(_are_dates_ok)
        # If we are in the DELETE state and number of selected rows is 0
        elif current_state == DELETE_STATE and nb_rows_selected == 0:
            _are_dates_ok = are_dates_ok()
            # If dates are OK and there is something to edit, we transition to the EDIT state.
            if _are_dates_ok and something_to_edit():
                edit_state()
            else: # Otherwise, we transition to the STUDENT_LOADED state, with possibly an error 
                # message is some dates are not OK.
                student_loaded_state(_are_dates_ok)
    # Some of the mandatory fields are not filled in: we transition back to the INIT state.
    elif current_state != INIT_STATE:
        init_state()

def are_dates_ok():
    """Returns whether all dates are OK.

    Returns
    -------
    bool
        True if all dates are OK, False otherwise.
    """
    for i in range(1, len(registration_data_var)):
        year = int(get_edition_year(i))
        registration_date = get_registration_date(i)
        payment_date = get_payment_date(i)
        if not utils.is_valid_date(registration_date, empty=False) \
            or not utils.is_valid_date(payment_date) \
            or not utils.payment_date_after_registration(payment_date, registration_date) \
            or not utils.check_registration_year(registration_date, year):
            return False
    return True

def something_to_edit():
    """Returns whether the user has changed some values.

    Returns
    -------
    bool
        True if the user has changed some values, False otherwise.
    """
    for i in range(1, len(registration_data_var)):
        registration_date = get_registration_date(i)
        payment_date = get_payment_date(i)
        if registration_date != current_student_registrations[i][1] or \
            payment_date != current_student_registrations[i][2]:
            return True
    return False

def mandatory_fields_ok():
    """Returns whether all mandatory fields have been correctly filled in.

    Returns
    -------
    bool
        True if all mandatory fields have been correctly filled in, False otherwise.
    """
    return sum(filled_mandatory_fields) == nb_mandatory_fields

def is_button_checked(index):
    """Returns whether the check button at the specified index (row) is checked or not.

    Returns
    -------
    bool
        True if the specified check button is checked, False otherwise.
    """
    return registration_data_var[index][0].get()

def check_button(index):
    """Sets the check button at the specified index (row) as checked.
    """
    registration_data_var[index][0].set(1)
        

def check_all_buttons():
    """Sets all the check buttons as checked.
    """
    for i in range(len(registration_data_var)):
        if not is_button_checked(i):
            check_button(i)

def uncheck_button(index):
    """Sets the check button at the specified index as unchecked.
    """
    registration_data_var[index][0].set(0)

def uncheck_all_buttons():
    """Sets all the check buttons as unchecked.
    """
    for i in range(len(registration_data_var)):
        if is_button_checked(i):
            uncheck_button(i)

def row_selected(index):
    """Invoked when the user selects/deselects a row.
    """
    global nb_rows_selected
    # if row selected, we increment nb_rows_selected, otherwise we decrement it.
    nb_rows_selected = nb_rows_selected + 1 if registration_data_var[index][0].get() else nb_rows_selected - 1

    for i in range(1, len(registration_data_var)):
        if not is_button_checked(i):
            uncheck_button(0)
            break
    else:
        check_button(0)

    transition()

def clear_fields_student_except_stud_number():
    """Clears all fields except the student number.
    """
    set_first_name("")
    set_last_name("")

    clear_registration_table()
    
def clear_registration_table():
    """Clears the table containing all the registrations of the current student.
    """
    global registration_data
    global registration_data_var
    global current_student_registrations
    
    if len(registration_data) > 0:
        for row in registration_data[1:]:
            for item in row:
                item.grid_remove()
                item.destroy()
        
        for header in registration_data[0]:
            header.grid_remove()
            header.destroy()
        
        scroll_registration_frm.update()
        scroll_registration_frm.configure(style="Empty.TFrame")

        uncheck_all_buttons()
        registration_data = []
        registration_data_var = []
        current_student_registrations = [("", "")]

def clear_fields():
    """Clears all the fields
    """
    set_stud_number("")
    clear_fields_student_except_stud_number()


def check_all_selected():
    """Invoked when the user checks/unchecks the button on the first row (indicating that s/he wants to select/
    deselect all rows).
    """
    # If the button is checked, we select all rows
    if is_button_checked(0):
        check_all_buttons()
    else: # otherwise, we deselect all rows.
        uncheck_all_buttons()

def stud_number_updated():
    """Invoked when the user types the student number in the corresponding text field.
    """
    stud_number = get_stud_number()
    if len(stud_number) > 0:
        if not stud_number.isdigit():
            control_labels["stud_number_ctrl"].configure(text=messages_bundle["invalid_identifier"], image = "")
            filled_mandatory_fields[STUD_NUMBER] = 0
        else:   
            control_labels["stud_number_ctrl"].configure(text="", image = check_image)
            control_labels["stud_number_ctrl"].image=check_image
            filled_mandatory_fields[STUD_NUMBER] = 1
    else:
        reset_control_label(lbl="stud_number_ctrl")
        filled_mandatory_fields[STUD_NUMBER] = 0
    transition()

def registration_date_updated(index):
    """Invoked when the user modifies the registration date at a specified index/row.

    Parameter
    ---------
    index : int
        The index/row of the registration of which the registration date has been modified.

    """
    year = int(get_edition_year(index))
    new_registration_date = get_registration_date(index)
    payment_date = get_payment_date(index)
    
    # We highlight in red the date if it's not valid.
    if not utils.is_valid_date(new_registration_date, empty=False):
        registration_data[index][2].configure(style="Error.TEntry")
    else: # the format is OK but....
        # We compare the registration date against the payment date to make sure that
        # the latter is greater than  or equal to the former.
        # If that's not the case, both dates are highlighted in red.
        if utils.is_valid_date(payment_date) and \
            not utils.payment_date_after_registration(payment_date, new_registration_date):
                registration_data[index][2].configure(style="Error.TEntry")
                registration_data[index][3].configure(style="Error.TEntry")
        else: # the payment date is OK
            registration_data[index][3].configure(style="TEntry")
            # We still need to compare the registration year against the edition year. 
            # If the registration year is not (edition year - 1), we highlight the 
            # registration date in red.
            if not utils.check_registration_year(new_registration_date, year):
                registration_data[index][2].configure(style="Error.TEntry")
            else: #  registration date is OK
                registration_data[index][2].configure(style="TEntry")
    transition()

def payment_date_updated(index):
    """Invoked when the user modifies the payment date at a specified index/row.

    Parameter
    ---------
    index : int
        The index/row of the registration of which the payment date has been modified.
    """
    new_payment_date = get_payment_date(index)
    registration_date = get_registration_date(index)
    
    # We hightlight in red the payment date if its format is not correct.
    if not utils.is_valid_date(new_payment_date):
        registration_data[index][3].configure(style="Error.TEntry")
    else:
        # We compare the registration date against the payment date to make sure that
        # the latter is greater than  or equal to the former.
        # If that's not the case, both dates are highlighted in red.
        registration_data[index][3].configure(style="TEntry")
        if utils.is_valid_date(registration_date, empty=False):
            if not utils.payment_date_after_registration(new_payment_date, registration_date):
                registration_data[index][2].configure(style="Error.TEntry")
                registration_data[index][3].configure(style="Error.TEntry")
            else: # The payment date is OK, the registration date must be checked against the year.
                # We reload the value so as to force a new check on the registration date (dirty hack).
                registration_data_var[index][2].set(get_registration_date(index))
                registration_data[index][3].configure(style="TEntry")
    transition()
        
def get_student_registrations(stud_number):
    """Invoked when the user presses the key <Tab> after entering the 
    student number

    Parameters
    ----------
    stud_number : int
        The student number.
    """
    # Get all the registrations from the database.
    stud_regs = mreg.get_student_registrations(stud_number, cursor)
    if stud_regs is None:
        write_message(messages_bundle["unexpected_error"])
        return 
    
    # Nothing to do if the list is empty.
    if len(stud_regs) == 0:
        return

    scroll_registration_frm.configure(style="Table.TFrame")

    # In registration_data_var, we add the first item, that corresponds to the 
    # variables with the current content of the reegistration table header.
    # The header contains a check button that is used to select/deselect 
    # all the rows. The tk.IntVar is used to track the current value of 
    # this check button. 
    # The header also contains three labels, but they have no associated variable.
    registration_data_var.append((tk.IntVar(),))

    # Here we add the widgets of the registration table. 
    # Each row is represented as a tuple.
    # Here we add the header: a check button (to select/deselect all rows) and three labels 
    # with the headers of the table.
    registration_data.append(
        (
            ttk.Checkbutton(scroll_registration_frm, width=5, variable=registration_data_var[0][0], \
                command=check_all_selected),
            ttk.Label(scroll_registration_frm, anchor=tk.CENTER, \
                text=messages_bundle["edition_year"], style="Header.TLabel"), 
            ttk.Label(scroll_registration_frm, anchor=tk.CENTER, \
                text=messages_bundle["registration_date"], style="Header.TLabel"),
            ttk.Label(scroll_registration_frm, anchor=tk.CENTER, \
                text=messages_bundle["payment_date"], style="Header.TLabel")
        )
    )
    
    # We add the widgets to the frame.
    registration_data[0][0].grid(row=0, column=0, padx=10, pady=5, sticky='ew')
    registration_data[0][1].grid(row=0, column=1, padx=10, pady=5, sticky='ew')
    registration_data[0][2].grid(row=0, column=2, pady=5, sticky='ew')
    registration_data[0][3].grid(row=0, column=3, pady=5, sticky='ew')
    
    # We iterate over all the registrations and 
    # we add a row to the registration table for each registration.
    # Each row contains four widgets: a check button (used to select/deselect a row) and 
    # three text fields (edition year, registration date and payment date).
    for i in range(len(stud_regs)):
        # Each row is a tuple: tk.IntVar contains the current value of the 
        # check button; the three tk.StringVar() contain the current values of the 
        # edition year, the registration date and the payment date respectively.
        registration_data_var.append(
            (
                tk.IntVar(),
                tk.StringVar(),
                tk.StringVar(),
                tk.StringVar()
            )
        )

        # The values loaded from the database.
        year = stud_regs[i][0] 
        registration_date = stud_regs[i][1]
        payment_date = "" if stud_regs[i][2] is None else stud_regs[i][2]

        # We trace the value of the check button. 
        # Whenever the user checks/unchecks the button, the 
        # function row_selected() is invoked.
        registration_data_var[i+1][0].trace("w", \
            lambda name, index, mode, var_index=i+1: row_selected(var_index))

        # Wev set eh values of the three text fields.
        registration_data_var[i+1][1].set(year)
        registration_data_var[i+1][2].set(registration_date)
        registration_data_var[i+1][3].set(payment_date)

        # The values loaded from the database are stored in the list 
        # current_student_registrations. This way, we can track the values that the user
        # changed.
        current_student_registrations.append((year, registration_date, payment_date))
        
        # We add the four widgets to the list registration_data.
        registration_data.append(
            (
                ttk.Checkbutton(scroll_registration_frm, width=5, variable=registration_data_var[i+1][0]),
                ttk.Entry(scroll_registration_frm, state="disabled", justify='center', textvariable=registration_data_var[i+1][1]),
                ttk.Entry(scroll_registration_frm, justify='center', textvariable=registration_data_var[i+1][2]),
                ttk.Entry(scroll_registration_frm, justify='center', textvariable=registration_data_var[i+1][3])
            )
        )
        # The four widgets are added to the frame.
        registration_data[i+1][0].grid(row=i+1, column=0, padx=10, sticky='ew')
        registration_data[i+1][1].grid(row=i+1, column=1, padx=10, sticky='ew')
        registration_data[i+1][2].grid(row=i+1, column=2, padx=10, sticky='ew')
        registration_data[i+1][3].grid(row=i+1, column=3, padx=10, sticky='ew')

        # Whenever the user types a registration date and presses the  key <Tab>, 
        # the function registration_date_updated is invoked.
        registration_data[i+1][2].bind(
            '<FocusOut>', 
            lambda event, index=i+1: registration_date_updated(index)
        )

        # Whenever the user types a payment date and presses the  key <Tab>, 
        # the function payment_date_updated is invoked.
        registration_data[i+1][3].bind(
            '<FocusOut>', 
            lambda event, index=i+1: payment_date_updated(index)
        )

def find_student(event):
    """Invoked when the user types a student number in the corresponding 
    text field and then presses the <Tab> key.

    Parameters
    ----------
    event:
        Information on the event.
    """
    
    # Get the student from the database.
    stud_number = get_stud_number()
    student = mstud.get_student(stud_number, cursor)
    clear_fields_student_except_stud_number()

    if student is None:
        write_message(messages_bundle["unexpected_error"])
    # If the student exists, first and family name are automatically filled in.
    elif student:
        set_first_name(student[1])
        set_last_name(student[2])
        filled_mandatory_fields[FIRST_NAME] = 1
        filled_mandatory_fields[LAST_NAME] = 1
        # We also get all the student registrations from the database 
        # and we display them.
        get_student_registrations(stud_number)
    else: # We display an error message is the student is not found.
        control_labels["stud_number_ctrl"].configure(text=messages_bundle["student_not_found"], image = "")
        filled_mandatory_fields[FIRST_NAME] = 0
        filled_mandatory_fields[LAST_NAME] = 0
    
    transition()

def edit_registration():
    """Invoked when the user clicks on the button Edit.
    """

    # We iterate over all the registrations and we update the ones for which 
    # the user has entered new values.
    cursor.execute("BEGIN")
    for i in range(1, len(registration_data_var)):
        stud_number = get_stud_number()
        edition_year = get_edition_year(i)
        registration_date = get_registration_date(i)
        payment_date = get_payment_date(i)
        if registration_date != current_student_registrations[i][1]:
            # We update the registration date.
            res = mreg.update_registration_date(stud_number, edition_year, registration_date, cursor)
            # If a database error occurs, we stop the update and we exit the loop
            if not res[0]:
                write_message(messages_bundle["unexpected_error"] + res[2])
                conn.rollback()
                break
        if payment_date != current_student_registrations[i][2]:
            # We update the payment date.
            res = mreg.update_payment_date(stud_number, edition_year, payment_date, cursor)
            # If a database error occurs, we stop the update and we exit the loop.
            if not res[0]:
                write_message(messages_bundle["unexpected_error"] + res[2])
                conn.rollback()
                break
    # If no error has occurred, we commit the modifications.
    else:
        conn.commit()
        clear_registration_table()
        # We get the new values.
        get_student_registrations(stud_number)
        write_message(messages_bundle["registration_edited"])
        transition()
    

def delete_registration():
    """Invoked when  the user clicks on the button Delete.
    """
    stud_number = get_stud_number()
    cursor.execute("BEGIN")
    for i in range(1, len(registration_data_var)):
        # We delete the row if it's selected.
        if is_button_checked(i):
            res = mreg.delete_registration(stud_number, get_edition_year(i), cursor)
            if not res[0]:
                write_message(messages_bundle["unexpected_error"] + res[2])
                conn.rollback()
                break
    else:
        conn.commit()
        clear_registration_table()
        get_student_registrations(stud_number)
        transition()
        

def cancel_action():
    """Invoked when the user clicks on the button Cancel.
    """
    reset()
    clear_fields()
    edit_reg_tab.destroy()

def clear_action():
    """Invoked when the user clicks on the button Clear.
    """
    reset()
    clear_fields()

def add_stud_number_control_label(label):
    """Adds the student number control label.

    Parameters
    ----------
    label: ttk.Label
        The control label to add.
    """
    control_labels["stud_number_ctrl"] = label

def add_message_control_label(label):
    """Adds the control label for the message area.

    Parameters
    ----------
    label: ttk.Label
        The control label to add.
    """
    control_labels["message_ctrl"] = label

def add_stud_number_entry(entry):
    """Adds the student number text field.

    Parameters
    ----------
    entry: a tuple (ttk.Entry, tk.StringVar)
        The text field and the text variable holding the current content of the text field.
    """
    entries["stud_number"] = entry

def add_first_name_entry(entry):
    """Adds the first name text field.

    Parameters
    ----------
    entry: a tuple (ttk.Entry, tk.StringVar)
        The text field and the text variable holding the current content of the text field.
    
    """
    entries["first_name"] = entry

def add_last_name_entry(entry):
    """Adds the last name text field.

    Parameters
    ----------
    entry: a tuple (ttk.Entry, tk.StringVar)
        The text field and the text variable holding the current content of the text field.
    """
    entries["last_name"] = entry

def add_edit_button(button):
    """Adds the button Edit.

    Parameters
    ----------
    button: ttk.Button
        The button to add.

    """
    buttons["edit_btn"] = button

def add_delete_button(button):
    """Adds the button Delete.

    Parameters
    ----------
    button: ttk.Button
        The button to add.

    """
    buttons["delete_btn"] = button

def add_clear_button(button):
    """Adds the button Clear.

    Parameters
    ----------
    button: ttk.Button
        The button to add.

    """
    buttons["clear_btn"] = button

def add_cancel_button(button):
    """Adds the button Cancel.

    Parameters
    ----------
    button: ttk.Button
        The button to add.

    """
    buttons["cancel_btn"] = button

def get_stud_number():
    """Returns the current value of the student number text field.

    Returns
    -------
    string
        The current value of the student number text field.
    """
    return entries["stud_number"][1].get().strip()

def set_stud_number(stud_number):
    """Sets the current value of the student number text field.

    Parameters
    ----------
    stud_number : string
        The current value of the student number text field.
    """
    entries["stud_number"][1].set(stud_number)

def get_first_name():
    """Returns the current value of the first name text field.

    Returns
    -------
    string
        The current value of the first name text field.
    """
    return entries["first_name"][1].get().strip()

def set_first_name(first_name):
    """Sets the current value of the first name text field.

    Parameters
    ----------
    first_name : string
        The current value of the first name text field.
    """
    return entries["first_name"][1].set(first_name)

def get_last_name():
    """Returns the current value of the last name text field.

    Returns
    -------
    string
        The current value of the last name text field.
    """
    return entries["last_name"][1].get().strip()

def set_last_name(last_name):
    """Sets the current value of the last name text field.

    Parameters
    ----------
    last_name : string
        The current value of the last name text field.
    """
    return entries["last_name"][1].set(last_name)

def get_edition_year(index):
    """Returns the current value of the edition year text field at the 
    given index/row in the registration table.

    Parameters
    ----------
    index : int
        The index/row of the registration table where the text field is.

    Returns
    -------
    string
        The current value of the edition year text field.
    """
    return registration_data_var[index][1].get().strip()

def get_registration_date(index):
    """Returns the current value of the registration date text field at the 
    given index/row in the registration table.

    Parameters
    ----------
    index : int
        The index/row of the registration table where the text field is.

    Returns
    -------
    string
        The current value of the registration date text field.
    """
    return registration_data_var[index][2].get().strip()

def get_payment_date(index):
    """Returns the current value of the payment date text field at the 
    given index/row in the registration table.

    Parameters
    ----------
    index : int
        The index/row of the registration table where the text field is.

    Returns
    -------
    string
        The current value of the payment date text field.
    """

    return registration_data_var[index][3].get().strip()

def write_message(message):
    """Write a message in the message area.

    Parameters
    ----------
    message : string
        The message to write.
    """
    control_labels["message_ctrl"].configure(text=message)