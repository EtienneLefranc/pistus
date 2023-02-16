"""Functions associated with the student tab.

In this file, we define all the functions that are used to 
create the student tab and make it react to events.
All the callbacks associated to users' actions on the student tab are
defined here.
"""

import tkinter as tk
import mstudent as mstud
import utils

# Here we store all the different widgets of the student tab.
control_labels = {}
entries = {}
radio_buttons = {}
combo_boxes = {}
buttons = {}

# Event that occurs when a student is successfully added to the database.
STUDENT_UPDATED_EVENT = 0

# Number of mandatory fields in the student tab.
# Each mandatory field is associated to a numeric code.
nb_mandatory_fields = 5
STUD_NUMBER = 0
FIRST_NAME = 1
LAST_NAME = 2
GENDER = 3
EMAIL_ADDRESS = 4

# Bit vector associated to the mandatory fields in the student tab.
# Each mandatory field is assigned a value: 1 if the mandatory field is 
# correctly filled by the user, 0 otherwise. 
# The position in the array of the value assigned to a field is given by 
# the numeric code of the field.
# For instance, filled_mandatory_fields[STUD_NUMBER] = 0 means that the user 
# did not specify the student number as required.
filled_mandatory_fields = [0 for i in range(nb_mandatory_fields)]

# Depending on the user's actions, the student tab might 
# be in one of several states; the appearance of the interface changes depending 
# on the state. 
# In the INIT state, the buttons Add and Edit are both disabled
# because the user hasn't filled the student data fields yet.
INIT_STATE = 0
# In the STUDENT_LOADED state, an existing student has been loaded from the database, 
# but no values have been changed yet, or the changes are not acceptable 
# (e.g., invalid email addresses). The edit button will be disabled.
STUDENT_LOADED_STATE = 1
# In the EDIT state, a existing student has been loaded from the database
# and some values have been changed and can be stored into the database.
# The edit button will be enabled.
EDIT_STATE = 2
# In the ADD state, all the data fields relative to a new student have been 
# correctly filled in; the add button will be enabled.
ADD_STATE = 3
# When a student is successfully added or updated to the database, we transition to this state, where
# all fields are disabled and a message is displayed to the user in the message area.
STUDENT_UPDATED_STATE = 4

# Keeps track of the current state
current_state = INIT_STATE

# This dictionary contains the data on a student loaded from the database
# after the user specifies his/her student number.
# This is used to check whether the user changes any data on the student.
loaded_student = {}

# This fields is True when no email address is specified (the alternate email address is not 
# mandatory), or the specified email address has the right format.
alternate_email_address_ok = True

# The dictionary containing all the messages shown in the GUI.
messages_bundle = {}

# The image used to indicate that a field contains a correct value.
check_image = None

# Reference to the student tab.
stud_tab = None

# The object used to query the database.
cursor = None

# The object used to connect to the database.
conn = None

def init(_messages_bundle, _check_image, _stud_tab, _cursor, _conn):
    """Initializes some of the global variables defined in the file.

    Parameters
    ----------
    _messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    _check_image : ImageTk.PhotoImage
        The image used to indicate that a field contains a correct value.
    _stud_tab : ttk.Frame
         The frame where all the widgets are added.
    _cursor : 
        The object used to query the database.
    _conn : 
        The object used to connect to the database.
    """
    
    global messages_bundle
    global check_image
    global stud_tab
    global cursor
    global conn

    messages_bundle = _messages_bundle
    check_image = _check_image
    stud_tab = _stud_tab
    cursor = _cursor
    conn = _conn

def reset():
    """Resets some of the global variables defined in this file.

    This function is invoked when clearing all the fields in the student tab.
    """
    
    global loaded_student
    global filled_mandatory_fields
    
    filled_mandatory_fields = [0 for i in range(nb_mandatory_fields)]
    loaded_student = {}
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
    
    if lbl == "all" or lbl == "first_name_ctrl":
        control_labels["first_name_ctrl"].configure(image = "", text=messages_bundle["enter_first_name"])
    
    if lbl == "all" or lbl == "last_name_ctrl":
        control_labels["last_name_ctrl"].configure(image = "", text=messages_bundle["enter_last_name"])
    
    if lbl == "all" or lbl == "gender_ctrl":
        control_labels["gender_ctrl"].configure(image = "", text=messages_bundle["select_gender"])
    
    if lbl == "all" or lbl == "email_address_ctrl":
        control_labels["email_address_ctrl"].configure(image = "", text=messages_bundle["enter_email_address"])
    
    if lbl == "alternate_email_address_ctrl":
        control_labels["alternate_email_address_ctrl"].configure(image = "", text="")

    if lbl == "all" or lbl == "message_area_ctrl":
        control_labels["message_ctrl"].configure(text="")

def init_state():
    """Sets the state of the widgets in the state INIT_STATE
    """
    
    global current_state

    # The add and edit buttons are disabled; the field student number is enabled.
    current_state = INIT_STATE

    # All widgets are enabled except the add and edit buttons
    entries["stud_number"][0].state(["!disabled"])
    entries["first_name"][0].state(["!disabled"])
    entries["last_name"][0].state(["!disabled"])
    for i in range(2):
        radio_buttons["gender"][i].state(["!disabled"])
    for i in range(2):
        entries["email_addresses"][i][0].state(["!disabled"])
    for i in range(3):
        combo_boxes["asso_name"][i].state(["!disabled"])
        combo_boxes["stud_role"][i].state(["!disabled"])
    
    buttons["add_btn"].state(["disabled"])
    buttons["edit_btn"].state(["disabled"])
    

def edit_state():
    """Sets the state of the widgets in the state EDIT_STATE
    """

    global current_state

    # The edit button is enabled.
    # The add button is disabled; in this state, an existing student is 
    # loaded from the database for editing, we prevent the user from adding the student 
    # a second time to the database, which would result in a primary key error. 
    # The student number field is disabled. We prevent the user from changing the student number.
    current_state = EDIT_STATE
    buttons["add_btn"].state(["disabled"])
    buttons["edit_btn"].state(["!disabled"])
    entries["stud_number"][0].state(["disabled"])

def student_loaded_state():
    """Sets the state of the widgets in the state STUDENT_LOADED_STATE
    """
    
    global current_state

    # Both add and edit buttons are disabled.
    # In this state, an existing student has been loaded from the database.
    # The user did not modify the original values of the student, or the new values are not correct.
    # In either case, the student number of the existing student cannot be changed, hence the 
    # student number field is disabled.
    current_state = STUDENT_LOADED_STATE
    buttons["add_btn"].state(["disabled"])
    buttons["edit_btn"].state(["disabled"])
    entries["stud_number"][0].state(["disabled"])

def add_state():
    """Sets the state of the widgets in the state ADD_STATE
    """
    
    global current_state

    # The add button is enabled.
    # The edit button is disabled. In this state, the user is trying to add a new user 
    # (the specified student number is not in the database).
    # The student number field is enabled.
    current_state = ADD_STATE
    buttons["add_btn"].state(["!disabled"])
    buttons["edit_btn"].state(["disabled"])
    entries["stud_number"][0].state(["!disabled"])

def student_updated_state():
    """Sets the state of the widgets in the state STUDENT_UPDATED_STATE
    """
    global current_state

    # We disable all the widgets
    current_state = STUDENT_UPDATED_STATE
    entries["stud_number"][0].state(["disabled"])
    entries["first_name"][0].state(["disabled"])
    entries["last_name"][0].state(["disabled"])
    for i in range(2):
        radio_buttons["gender"][i].state(["disabled"])
    for i in range(2):
        entries["email_addresses"][i][0].state(["disabled"])
    for i in range(3):
        combo_boxes["asso_name"][i].state(["disabled"])
        combo_boxes["stud_role"][i].state(["disabled"])
    
    buttons["add_btn"].state(["disabled"])
    buttons["edit_btn"].state(["disabled"])

def transition(event=None):
    """Defines the transitions between the states.

    Parameters
    ----------
    event : string
        The event that triggers the transition (default: None)
    """

    # First case: all mandatory fields are correctly filled in, as well as the alternate
    # email address.
    if mandatory_fields_ok() and alternate_email_address_ok:
        # If we are in the INIT_STATE, we transition to STUDENT_LOADED_STATE if
        # the user has specified a student number of an existing student; 
        # otherwise, we transition to ADD_STATE.
        if current_state == INIT_STATE:
            if bool(loaded_student):
                student_loaded_state()
            else:
                add_state()
        # If we are in ADD_STATE, we transition to STUDENT_LOADED_STATE.
        # In fact, it might happen that the user specifies all the mandatory fields for
        # a new user, then s/he specifies the student number of an existing student.
        elif current_state == ADD_STATE:
            if bool(loaded_student):
                student_loaded_state()
            elif event == STUDENT_UPDATED_EVENT:
                student_updated_state()
        # If we are in STUDENT_LOADED_STATE and some values have been correctly edited, 
        # we transition to the EDIT_STATE.
        elif current_state == STUDENT_LOADED_STATE and something_to_edit():
            edit_state()
        # If we are in EDIT_STATE and we have nothing to edit (the user undoes any previous modification), 
        # we transition back to STUDENT_LOADED_STATE
        elif current_state == EDIT_STATE:
            if not something_to_edit():
                student_loaded_state()
            elif event == STUDENT_UPDATED_EVENT:
                student_updated_state()
    # Mandatory fields are not OK, or the alternate email address is invalid.
    else:
        # If we are in EDIT_STATE, we transition to STUDENT_LOADED_STATE if 
        # a student has already been loaded.
        if current_state == EDIT_STATE and bool(loaded_student):
            student_loaded_state()
        elif not current_state == STUDENT_LOADED_STATE or not filled_mandatory_fields[STUD_NUMBER] == 1:
            init_state()
    
def something_to_edit():
    """Checks whether some values have been edited by the user, which justifies 
    a transition from  STUDENT_LOADED_STATE to EDIT_STATE.

    Returns
    -------
    bool
        True if some values have been edited, False otherwise.
    """

    # We compare the old values against the new values (first and last name and gender)
    new_values = (get_first_name(), get_last_name(), get_gender()) 
    old_values = (loaded_student["first_name"], \
        loaded_student["last_name"], loaded_student["gender"])
    for i in range(len(new_values)):
        if new_values[i] != old_values[i]:
            return True
    
    # We compare the old and new email addresses.
    new_email_addresses = get_email_addresses()
    old_email_addresses = loaded_student["email_addresses"]
    if len(new_email_addresses) != len(old_email_addresses):
        return True
    for i in range(len(new_email_addresses)):
        if new_email_addresses[i] != old_email_addresses[i]:
            return True

    # Finally we compare the old and new membership values.
    new_memberships = get_memberships()
    old_memberships = loaded_student["memberships"]
    if len(new_memberships) != len(old_memberships):
        return True
    for i in range(len(new_memberships)):
        if new_memberships[i][0] != old_memberships[i][0] or \
            new_memberships[i][1] != old_memberships[i][1]:
            return True
    
    # If no change is detected, we return False
    return False

def mandatory_fields_ok():
    """Checks whether the mandatory fields have been correctly filled.

    Returns
    -------
    bool
        True if all the mandatory fields have been correctly filled, False otherwise.

    """
    return sum(filled_mandatory_fields) == nb_mandatory_fields

def clear_fields():
    """ Clears all the fields in the student tab.
    """
    set_stud_number("")
    clear_fields_except_stud_number()

def clear_fields_except_stud_number():
    """Clears all the fields in the student tab except the student number.
    """
    set_first_name("")
    set_last_name("")
    for i in range(len(entries["email_addresses"])):
        set_email_address("", i)
    set_gender("")
    for i in range(len(combo_boxes["asso_name"])):
        set_membership(("", ""), i)

def asso_name_selected(event, index):
    """Callback invoked when the name of an association is selected.

    Parameters
    ----------
    event
        The event information.
    index : int
        The index of the combobox where the selection happened.
    """
    selected_value = combo_boxes["asso_name"][index].get()
    # When an association name is selected, the student role is automatically set to
    # "member". If no association name is selected, the student role is set to ""
    if len(selected_value) == 0:
        combo_boxes["stud_role"][index].set("")    
    else:
        combo_boxes["stud_role"][index].set("member")
    transition()

def stud_role_selected(event):
    """Invoked when a student role is selected

    Parameters
    ----------
    event
        The event information.
    """
    transition()
    
def stud_number_updated():
    """Invoked when the student number is updated.
    """
    stud_number = get_stud_number()
    # If some value is specified, we check that the format is correct.
    if len(stud_number) > 0:
        # The student number must be composed of digits only.
        if not stud_number.isdigit():
            control_labels["stud_number_ctrl"].configure(text=messages_bundle["invalid_identifier"], image = "")
            filled_mandatory_fields[STUD_NUMBER] = 0
        else: # the value is correct   
            control_labels["stud_number_ctrl"].configure(text="", image = check_image)
            control_labels["stud_number_ctrl"].image=check_image
            filled_mandatory_fields[STUD_NUMBER] = 1
    else: # No value has been specified, we reset the associated control label.
        reset_control_label(lbl="stud_number_ctrl")
        filled_mandatory_fields[STUD_NUMBER] = 0
    transition()

def first_name_updated():
    """Invoked when the first name is updated. 
    """
    first_name = get_first_name()
    if len(first_name) > 0:
        control_labels["first_name_ctrl"].configure(text="", image = check_image)
        control_labels["first_name_ctrl"].image=check_image
        filled_mandatory_fields[FIRST_NAME] = 1
    else:
        reset_control_label(lbl="first_name_ctrl")
        filled_mandatory_fields[FIRST_NAME] = 0
    transition()

def last_name_updated():
    """Invoked when the last name is updated.
    """
    last_name = get_last_name()
    if len(last_name) > 0:
        control_labels["last_name_ctrl"].configure(text="", image = check_image)
        control_labels["last_name_ctrl"].image=check_image
        filled_mandatory_fields[LAST_NAME] = 1
    else:
        reset_control_label(lbl="last_name_ctrl")
        filled_mandatory_fields[LAST_NAME] = 0
    transition()

def gender_selected():
    """Invoked when the gender is selected
    """
    gender = get_gender()
    if len(gender) > 0:
        control_labels["gender_ctrl"].configure(text="", image = check_image)
        control_labels["gender_ctrl"].image=check_image
        filled_mandatory_fields[GENDER] = 1
    else:
        reset_control_label(lbl="gender_ctrl")
        filled_mandatory_fields[GENDER] = 0
    transition()

def email_address_updated():
    """Invoked when the email address is updated.
    """
    email_address = get_email_address()
    # We check the correctness of the specified email address.
    if len(email_address) > 0:
        if not utils.is_valid_email_address(email_address):
            control_labels["email_address_ctrl"].configure(text=messages_bundle["invalid_email_address"], image="")
            filled_mandatory_fields[EMAIL_ADDRESS] = 0
        else:
            control_labels["email_address_ctrl"].configure(text="", image = check_image)
            control_labels["email_address_ctrl"].image=check_image
            filled_mandatory_fields[EMAIL_ADDRESS] = 1
    else:
        reset_control_label(lbl="email_address_ctrl")
        filled_mandatory_fields[EMAIL_ADDRESS] = 0
    transition()

def alternate_email_address_updated():
    """Invoked when the alternate email address is updated.
    """
    global alternate_email_address_ok
    email_address = get_alternate_email_address()
    if len(email_address) > 0:
        # if a value is specified, we make sure that the format of the address is correct.
        if not utils.is_valid_email_address(email_address):
            control_labels["alternate_email_address_ctrl"].configure(text=messages_bundle["invalid_email_address"], image="")
            alternate_email_address_ok = False
        else: 
            control_labels["alternate_email_address_ctrl"].configure(text="", image = check_image)
            control_labels["alternate_email_address_ctrl"].image=check_image
            alternate_email_address_ok = True
    else: 
        # If no value is specified, we display no error message (the alternate email address is not a 
        # mandatory field).
        reset_control_label(lbl="alternate_email_address_ctrl")
        alternate_email_address_ok = True
    transition()

def find_student(event):
    """Invoked when the user inserts the stud number and then presses <Tab>.

    This function looks for a student with the specified number in the database. If 
    a student is found, the other data fields are filled with the values loaded from the 
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
    # If the student exists, the data fields are filled in automatically.
    elif student:

        # Clear all fields except the student number
        clear_fields_except_stud_number()

        # The student loaded from the database is stored in the dictionary 
        # loaded_student. This way, we can check whether the user modifies some of the data 
        # at any time.
        loaded_student["first_name"] = student[1]
        loaded_student["last_name"] = student[2]
        loaded_student["gender"] = student[3]
        loaded_student["email_addresses"] = [student[4][i] for i in range(len(student[4]))]
        memberships = mstud.get_memberships(stud_number, cursor)
        if memberships is None:
            write_message(messages_bundle["unexpected_error"])
        else:
            loaded_student["memberships"] = [(memberships[i][0], memberships[i][1]) \
                for i in range(len(memberships))]
            
            # Fill in the first and last name and the gender.
            set_first_name(student[1])
            set_last_name(student[2])
            set_gender(student[3]) 

            # Fill in the email addresses.   
            for i in range(len(student[4])):
                set_email_address(student[4][i], i)
            
            # Fill in the membership data.
            for i in range(len(memberships)):
                set_membership(memberships[i], i)
            
            transition()

def add_student_db():
    """Invoked when the user clicks on the add button.

    This function adds a new student to the database.
    """
    # Add the student to the database
    stud_number = get_stud_number()
    # Begin a transaction
    cursor.execute("BEGIN")
    res = mstud.add_student(stud_number, get_first_name(), get_last_name(), \
        get_gender(), get_email_addresses(), cursor)
    
    # Error while adding the student
    if not res[0]:
        # Duplicate student number
        if res[1] == mstud.DUPLICATE_STUD_NUMBER:
            write_message(messages_bundle["duplicate_stud_number"])
        # Duplicate email address
        elif res[1] == mstud.DUPLICATE_EMAIL_ADDRESS:
            write_message(messages_bundle["duplicate_email_address"] + res[2])
        else:
            write_message(messages_bundle["unexpected_error"] + res[2])
        conn.rollback()
    else:    
        # Try to add the student to the associations.
        stud_associations = get_memberships()
        for stud_association in stud_associations:
            res = mstud.add_membership(stud_number, stud_association, cursor)
            if not res[0]:
                # Error while adding the student to the associations
                if res[1] == mstud.DUPLICATE_MEMBERSHIP:
                    write_message(messages_bundle["duplicate_membership"] + res[2])
                else: 
                    write_message(messages_bundle["unexpected_error"] + res[2])
                conn.rollback()
                break
        else:
            # If no error arises, we can commit the modifications to the database and 
            # show a positive message to the user.
            conn.commit()
            write_message(messages_bundle["student_added"])
            transition(event=STUDENT_UPDATED_EVENT)  
    

def edit_student():
    """Invoked when the user clicks on the edit button.
    """
    stud_number = get_stud_number()
    first_name = get_first_name()
    last_name = get_last_name()
    gender = get_gender()

    # We start a transaction.
    # We may have multiple fields to update. Either all are updated correctly, or none.
    cursor.execute("BEGIN")
    # This variable is set to True when an error arises (in which case the transaction is aborted).
    error = False

    # In the following code, we compare the values in the loaded_student dictionary against the values
    # in the data fields of the student tab. The loaded_student dictionary contains the values as they
    # have been loaded from the database. If the value in a data field differs from the corresponding value
    # in student_loaded, then we need to update the database.
    
    # We update the first name.
    if first_name != loaded_student["first_name"]:
        res = mstud.update_first_name(stud_number, first_name, cursor)
        if not res[0]:
            write_message(messages_bundle["unexpected_error"] + res[2])
            error = True
    
    # We update the last name.
    if last_name != loaded_student["last_name"]:
        res = mstud.update_last_name(stud_number, last_name, cursor)
        if not res[0]:
            write_message(messages_bundle["unexpected_error"] + res[2])
            error = True
    
    # We update the gender.
    if gender != loaded_student["gender"]:
        res = mstud.update_gender(stud_number, gender, cursor)
        if not res[0]:
            write_message(messages_bundle["unexpected_error"] + res[2])
            error = True

    # We update the email addresses.
    for i in range(len(loaded_student["email_addresses"])):
        new_email_address = get_email_address_by_index(i)
        if new_email_address != loaded_student["email_addresses"][i]:
            # If a field in the student tab is empty (and before it was not), 
            # an email address has been deleted.
            if len(new_email_address) == 0:
                res = mstud.delete_email_address(stud_number, loaded_student["email_addresses"][i], cursor)
                if not res[0]:
                    error = True
                    write_message(messages_bundle["unexpected_error"] + res[2])
            else: # Otherwise, the old email address was updated
                res = mstud.update_email_address(stud_number, loaded_student["email_addresses"][i], \
                    new_email_address, cursor)
                if not res[0]:
                    error = True
                    if res[1] == mstud.DUPLICATE_EMAIL_ADDRESS:
                        write_message(messages_bundle["duplicate_email_address"] + res[2])
                    elif res[1] == mstud.UNEXPECTED_ERROR:
                        write_message(messages_bundle["unexpected_error"] + res[2])
    
    # If the fields in the student tab contain email addresses that were not in the database
    # before, this means that a new email address was added.
    for i in range(len(loaded_student["email_addresses"]), len(entries["email_addresses"])):
        new_email_address = get_email_address_by_index(i)
        if len(new_email_address) > 0:
            res = mstud.add_email_address(stud_number, new_email_address, cursor)
            if not res[0]:
                error = True
                if res[1] == mstud.DUPLICATE_EMAIL_ADDRESS:
                    write_message(messages_bundle["duplicate_email_address"] + res[2])
                elif res[1] == mstud.UNEXPECTED_ERROR:
                    write_message(messages_bundle["unexpected_error"] + res[2])

    # Update the membership. Similar code to the email update.
    for i in range(len(loaded_student["memberships"])):
        new_membership = get_membership_by_index(i)
        if new_membership[0] != loaded_student["memberships"][0]:
            if len(new_membership[0]) == 0:
                res = mstud.delete_membership(stud_number, loaded_student["memberships"][i][0], cursor)
                if not res[0]:
                    error = True
                    write_message(messages_bundle["unexpected_error"] + res[2])
            else:
                res = mstud.update_membership(stud_number, loaded_student["memberships"][i][0], \
                    new_membership[0], new_membership[1], cursor)
                if not res[0]:
                    error = True
                    if res[1] == mstud.DUPLICATE_MEMBERSHIP:
                        write_message(messages_bundle["duplicate_membership"] + res[2])
                    elif res[1] == mstud.UNEXPECTED_ERROR:
                        write_message(messages_bundle["unexpected_error"] + res[2])

    for i in range(len(loaded_student["memberships"]), len(combo_boxes["asso_name"])):
        new_membership = get_membership_by_index(i)
        if len(new_membership[0]) > 0:
             res = mstud.add_membership(stud_number, new_membership, cursor)
             if not res[0]:
                error = True
                if res[1] == mstud.DUPLICATE_MEMBERSHIP:
                    write_message(messages_bundle["duplicate_membership"] + res[2])
                elif res[1] == mstud.UNEXPECTED_ERROR:
                    write_message(messages_bundle["unexpected_error"] + res[2])

    # If no error occurs, the modifications are commited to the database and a positive 
    # message is shown to the user.
    if not error:
        conn.commit()
        write_message(messages_bundle["student_edited"])
        transition(event=STUDENT_UPDATED_EVENT)
    else: # Otherwise we rollback the transaction
        conn.rollback()
    
def cancel_action():
    """Invoked when the user clicks on the cancel button 
    """
    reset()
    stud_tab.destroy()

def clear_action():
    """Invoked when the user clicks on the clear button 
    """
    reset()
    clear_fields()

def add_control_label(key, label):
    """Adds a control label.

    Parameters
    ----------
    key : string
        A key identifying the control label.
    label : ttk.Label
        The label
    """
    control_labels[key] = label

def add_entry(key, entry):
    """Adds a data entry.

    Parameters
    ----------
    key : string
        A key identifying the entry.
    entry : A tuple T(ttk.Entry, tk.StringVar)
        T[0] is the entry widget.
        T[1] is the variable with the content of the text field.
    """
    entries[key] = entry

def add_radio_button(key, radio_button):
    """Adds a group of two radio buttons.

    Parameters
    ----------
    key : string
        A key identifying the radio button group.
    radio_button : A tuple T(ttk.Radiobutton, ttk.Radiobutton, tk.StringVar)
        T[0] is the first radio button in the group.
        T[1] is the second radio button in the group.
        T[2] is the variable with the current selected value.
    """
    radio_buttons[key] = radio_button

def add_combo_box(key, combo_box):
    """Adds a list of  combo boxes.

    Parameters
    ----------
    key : string
        A key identifying the combo boxes.
    combo_box : 
        A list of objects of type ttk.Combobox.
    """
    combo_boxes[key] = combo_box

def add_button(key, button):
    """Adds a button

    Parameters
    ----------
    key : string
        A key identifying the button.
    button : ttk.Button
        The button.
    """
    buttons[key] = button

def get_stud_number():
    """Gets the current value of the student number.

    Returns
    -------
    A string.
        The current value of the student number text field.
    """
    return entries["stud_number"][1].get().strip()

def set_stud_number(stud_number):
    """Sets the value of the student number.

    Parameters
    ----------
    stud_number : string
        The student number.
    """
    entries["stud_number"][1].set(stud_number)

def get_first_name():
    """Gets the current value of the first name text field.

    Returns
    -------
    A string.
        The current value of the first name text field.
    """
    return entries["first_name"][1].get().strip()

def set_first_name(first_name):
    """Sets the student first name.

    Parameters
    ----------
    first_name : string
        The student first name.
    """
    return entries["first_name"][1].set(first_name)

def get_last_name():
    """Gets the current value of the last name text field.

    Returns
    -------
    A string.
        The current value of the last name text field.
    """
    return entries["last_name"][1].get().strip()

def set_last_name(last_name):
    return entries["last_name"][1].set(last_name)

def get_gender():
    """Gets the current value of the gender radio button group.

    Returns
    -------
    A string.
        The current value of the gender radio button group.
    """
    return radio_buttons["gender"][2].get()

def set_gender(gender):
    """Sets the current value of the gender.

    Parameters
    ----------
    gender : string
        The student gender.
    """
    return radio_buttons["gender"][2].set(gender)

def get_email_address_by_index(i):
    """Gets the email address at the specified index in the list

    Parameters
    ----------
    i : int
        The index at which the email address is to be found.
    
    Returns
    -------
    A string.
        The email address at the specified index.
    """
    return entries["email_addresses"][i][1].get().strip()

def get_email_address():
    """Gets the main email address of the current student.

    Returns
    -------
    A string.
        The main email address of the current student.
    """
    return get_email_address_by_index(0)

def get_alternate_email_address():
    """Gets the alternate email address of the current student.

    Returns
    -------
    A string.
        The alternate email address of the current student.
    """
    return get_email_address_by_index(1)

def get_email_addresses():
    """Gets the all the email address of the current student.

    Returns
    -------
    A list.
        All the email addresses of the current student.
    """
    email_addresses = [get_email_address(), get_alternate_email_address()]
    return [email_addresses[i] for i in range(len(email_addresses)) if len(email_addresses[i]) > 0]

def set_email_address(email_address, i):
    """Sets the email address of the current student at a specific index.

    Parameters
    ----------
    email_address : string
        The student email address.
    i : int
        The index at which the email address is added.
    """
    entries["email_addresses"][i][1].set(email_address)

def get_membership_by_index(i):
    """Gets the membership the current student at the specified index.

    Parameters
    ----------
    i : int
        The index of the membership to return.
    
    Returns
    -------
    A tuple T.
        T[0] is the association name, T[1] is the student role.
    """
    return (combo_boxes["asso_name"][i].get(), combo_boxes["stud_role"][i].get())

def get_memberships():
    """Gets all memberships of the current student.

    Returns
    -------
    A list.
        All the memberships of the current student.
    """
    return [(combo_boxes["asso_name"][i].get(), combo_boxes["stud_role"][i].get()) \
        for i in range(3) if len(combo_boxes["asso_name"][i].get()) > 0]

def set_membership(membership, i):
    """Sets the membership of the current student at a specific index.

    Parameters
    ----------
    membership : a tuple T
        The student membership. T[0] is the association name, T[1] is the student role.
    i : int
        The index at which the membership is added.
    """
    combo_boxes["asso_name"][i].set(membership[0])
    combo_boxes["stud_role"][i].set(membership[1])

def write_message(message):
    """Write a message in the message area.

    Parameters
    ----------
    message : string
        The message to write.
    """
    control_labels["message_ctrl"].configure(text=message)