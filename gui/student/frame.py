"""Student tab

Definition of the tab where all the personal information of a student are
displayed and can be edited.
"""

import tkinter as tk
import gui.gui_config as config
import gui.student.callbacks as clb
from tkinter import ttk
import mstudent as mstud
import utils

# The preferred width of the control labels.
# This is set to prevent the window to shrink and to enlarge depending on the length of the error messages.
# The width is different based on the language of the interface.
control_labels_width = {"fr": 24, "en" : 24}

def add_widgets(stud_tab, messages_bundle, cursor, conn, lang):
    """Adds the widgets to the student tab
    
    Parameters
    ----------
    stud_tab : ttk.Frame
        The frame where all the widgets are added.
    messages_bundle : dictionary.
        The dictionary containing all the messages shown in the GUI.
    cursor : 
        The object used to query the database.
    conn : 
        The object used to connect to the database.
    lang : string
        The language of the interface.
    """
    
    # Loads the image used to indicate that a field contains a correct value.
    check_image = utils.load_check_image()
    
    # Create the "student frame" containing all the student data fields.
    student_frm = ttk.Frame(stud_tab, style="Tab.TFrame")
    _student_widgets(student_frm, messages_bundle, cursor, lang)

    # Create the message area frame, where messages are shown to the users to give them
    # a feedback on their actions.
    message_area_frm = ttk.Frame(stud_tab, style="Tab.TFrame")
    _message_area_widgets(message_area_frm)

    # Create the "buttons frame" containing the buttons (add, edit...).
    buttons_frm = ttk.Frame(stud_tab, style="Tab.TFrame")
    _buttons_frame_widgets(buttons_frm, messages_bundle)

    # Add the two frames to the student tab.
    student_frm.pack(fill="both", expand=True, padx=20, pady=10)
    message_area_frm.pack(fill="both", expand=True, padx=20, pady=10)
    buttons_frm.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Initialization of the interface.
    clb.init(messages_bundle, check_image, stud_tab, cursor, conn)
    clb.reset()

def _student_widgets(student_frm, messages_bundle, cursor, lang):
    """Creates the widgets of the student frame.

    Parameters
    ----------
    student_frm : ttk.Frame
        The student frame.
    messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    cursor : 
        The object used to query the database.
    lang : string
        The language of the interface.
    """
    
    # Adds the labels of the data fields
    _add_labels(student_frm, messages_bundle)

    # Adds the control labels, used to show messages 
    # as to the correctness of the data fields
    _add_control_labels(student_frm, lang)

    _add_data_fields(student_frm, cursor)

def _message_area_widgets(message_area_frm):
    """Adds the widgets in the message area frame.

    Parameters
    ----------
    message_area_frm : ttk.Frame
        The message area frame.
    """
    message_ctrl_label = ttk.Label(message_area_frm, borderwidth=0, anchor= tk.CENTER, style="Check.TLabel")
    message_ctrl_label.pack(fill="both", expand=True, padx=20, pady=10)
    clb.add_control_label("message_ctrl", message_ctrl_label)

def _buttons_frame_widgets(buttons_frm, messages_bundle):
    """Adds the buttons to the buttons frame.
    Four buttons are added: 
    * "add", to add a student.
    * "edit", to edit a student.
    * "clear", to clear the data fields.
    * "cancel", to close the student tab with no further action.

    Parameters
    ----------
    buttons_frm : ttk.Frame
        The student frame.
    messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    """

    # Configures the grid of the frame so that the buttons are uniformely spread across the frame,
    # both horizontally and vertically.
    buttons_frm.rowconfigure(0, weight=1)
    for i in range(4):
        buttons_frm.columnconfigure(i, weight=1)
    
    # The add button.
    clb.add_button("add_btn", ttk.Button(buttons_frm, state="disabled", \
        text=messages_bundle["add_button"], command=clb.add_student_db))
    clb.buttons["add_btn"].grid(row=0, column=0, padx=10, pady=10)
    
    # The edit button.
    clb.add_button("edit_btn",  ttk.Button(buttons_frm, text=messages_bundle["edit_button"], state="disabled", \
        command=clb.edit_student))
    clb.buttons["edit_btn"].grid(row=0, column=1, padx=10, pady=10)
    
    # The clear button.
    clb.add_button("clear_btn", ttk.Button(buttons_frm, text=messages_bundle["clear_button"], command=clb.clear_action))
    clb.buttons["clear_btn"].grid(row=0, column=2, padx=10, pady=10)

    # The cancel button.
    clb.add_button("cancel_btn", ttk.Button(buttons_frm, text=messages_bundle["cancel_button"], command=clb.cancel_action))
    clb.buttons["cancel_btn"].grid(row=0, column=3, padx=10, pady=10)
 
def _add_labels(student_frm, messages_bundle):
    """Adds the labels of the data fields

    Parameters
    ----------
    student_frm : ttk.Frame
        The student frame.
    messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    """
    
    ttk.Label(student_frm, text=messages_bundle["stud_number"] + " *").grid(row=0, padx=10, pady=10, sticky='W')
    ttk.Label(student_frm, text=messages_bundle["first_name"] + " *").grid(row=1, padx=10, pady=10, sticky='W')
    ttk.Label(student_frm, text=messages_bundle["last_name"] + " *").grid(row=2, padx=10, pady=10, sticky='W')
    ttk.Label(student_frm, text=messages_bundle["gender"] + " *").grid(row=3, padx=10, pady=10, sticky='W')
    ttk.Label(student_frm, text=messages_bundle["email_address"] + " *").grid(row=4, padx=10, pady=10, sticky='W')
    ttk.Label(student_frm, text=messages_bundle["alternate_email_address"]).grid(row=5, padx=10, pady=10, sticky='W')
    ttk.Label(student_frm, text=messages_bundle["first_association"]).grid(row=6, padx=10, pady=10, sticky='W')
    ttk.Label(student_frm, text=messages_bundle["second_association"]).grid(row=7, padx=10, pady=10, sticky='W')
    ttk.Label(student_frm, text=messages_bundle["third_association"]).grid(row=8, padx=10, pady=10, sticky='W')


def _add_control_labels(student_frm, lang):
    """Adds the labels of the data fields

    Parameters
    ----------
    student_frm : ttk.Frame
        The student frame.
    messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    lang : string
        The language of the interface.
    """

    clb.add_control_label("stud_number_ctrl", ttk.Label(student_frm, width=control_labels_width[lang], \
        borderwidth=0, style="Check.TLabel"))
    clb.control_labels["stud_number_ctrl"].grid(row=0, column=2, pady=10, sticky='w')

    clb.add_control_label("first_name_ctrl", ttk.Label(student_frm, width=control_labels_width[lang], \
        borderwidth=0, style="Check.TLabel"))
    clb.control_labels["first_name_ctrl"].grid(row=1, column=2, pady=10, sticky='w')

    clb.add_control_label("last_name_ctrl", ttk.Label(student_frm, width=control_labels_width[lang], \
        borderwidth=0, style="Check.TLabel"))
    clb.control_labels["last_name_ctrl"].grid(row=2, column=2, pady=10, sticky='w')

    clb.add_control_label("gender_ctrl", ttk.Label(student_frm, width=control_labels_width[lang], \
        borderwidth=0, style="Check.TLabel"))
    clb.control_labels["gender_ctrl"].grid(row=3, column=2, pady=10, sticky='w')

    clb.add_control_label("email_address_ctrl", ttk.Label(student_frm, borderwidth=0, \
        width=control_labels_width[lang], style="Check.TLabel"))
    clb.control_labels["email_address_ctrl"].grid(row=4, column=2, pady=10, sticky='w')

    clb.add_control_label("alternate_email_address_ctrl", ttk.Label(student_frm, borderwidth=0, \
        width=control_labels_width[lang], style="Check.TLabel"))
    clb.control_labels["alternate_email_address_ctrl"].grid(row=5, column=2, pady=10, sticky='w')

def _add_data_fields(student_frm, cursor):
    """Adds the data fields (text entries, radio buttons and combo boxes)

    Parameters
    ----------
    student_frm : ttk.Frame
        The student frame.
    cursor : 
        The object used to query the database.
    """
    
    # Adds the text entries
    _add_entries(student_frm)

    # Adds the radio buttons
    _add_radio_buttons(student_frm)

    # Adds the combo boxes
    _add_combo_boxes(student_frm, cursor)


def _add_entries(student_frm):
    """Adds the text entries to the student frame.
    Each text entry is used to enter a specific student data field (student number, first name...).

    Parameters
    ----------
    student_frm : ttk.Frame
        The student frame.
    """

    # Stud number text entry.
    stud_number = tk.StringVar("")
    stud_number.trace("w", \
        lambda name, index, mode: clb.stud_number_updated())
    stud_number_ent = ttk.Entry(student_frm, textvariable=stud_number)    
    clb.add_entry("stud_number", (stud_number_ent, stud_number))
    stud_number_ent.grid(row=0, column=1, sticky='W')
    stud_number_ent.bind('<FocusOut>', lambda event: clb.find_student(event))
    
    # First name text entry.
    first_name = tk.StringVar("")
    first_name.trace("w", \
        lambda name, index, mode: clb.first_name_updated())
    first_name_ent = ttk.Entry(student_frm, textvariable=first_name)
    clb.add_entry("first_name", (first_name_ent, first_name))
    first_name_ent.grid(row=1, column=1, sticky='W')
    
    # Last name text entry.
    last_name = tk.StringVar("")
    last_name.trace("w", \
        lambda name, index, mode: clb.last_name_updated())
    last_name_ent = ttk.Entry(student_frm, textvariable=last_name)
    clb.add_entry("last_name", (last_name_ent, last_name))
    last_name_ent.grid(row=2, column=1, sticky='W')
    
    # Email addresses text entries.
    email_addresses = [tk.StringVar("") for _ in range(2)]
    email_addresses[0].trace("w", \
        lambda name, index, mode: clb.email_address_updated())
    email_addresses[1].trace("w", \
        lambda name, index, mode: clb.alternate_email_address_updated())
    email_addresses_ent = [ttk.Entry(student_frm, textvariable=email_addresses[i]) for i in range(2)]   
    clb.add_entry("email_addresses", [(email_addresses_ent[i], email_addresses[i]) for i in range(2)])
    init_row = 4
    for i in range(2):
        email_addresses_ent[i].grid(row=init_row, column=1, sticky='W')
        init_row += 1

def _add_radio_buttons(student_frm):
    """Adds the radio buttons to the student frame (to select the gender).

    Parameters
    ----------
    student_frm : ttk.Frame
        The student frame.
    """

    gender = tk.StringVar("")
    gender.trace("w", \
        lambda name, index, mode: clb.gender_selected())
    clb.add_radio_button("gender", (ttk.Radiobutton(student_frm, text='M', value='M', variable=gender), \
        ttk.Radiobutton(student_frm, text='F', value='F', variable=gender), gender))
    clb.radio_buttons["gender"][0].grid(row=3, column=1, sticky='W') 
    clb.radio_buttons["gender"][1].grid(row=3, column=1, padx=50, sticky='W')    

def _add_combo_boxes(student_frm, cursor):
    """Adds the combo boxes to the student frame.
    Combo boxes are used to select associations and the student role
    in those associations.

    Parameters
    ----------
    student_frm : ttk.Frame
        The student frame.
    cursor : 
        The object used to query the database.
    """

    # Get the associations and the student roles from the database
    associations = [""] + (list(map(lambda x: x[0], mstud.get_associations(cursor))))
    stud_roles = mstud.get_roles(cursor) 
    
    # We create three combo boxes for the associations and three for the student roles.
    asso_names_combo = [ttk.Combobox(student_frm,values=associations, state="readonly") for _ in range(3)]
    stud_roles_combo = [ttk.Combobox(student_frm,values=stud_roles, state="readonly") for _ in range(3)]
    clb.add_combo_box("asso_name", asso_names_combo)
    clb.add_combo_box("stud_role", stud_roles_combo)
    
    # We add them to the interface.
    row_index = 6
    for i in range(3):
        asso_names_combo[i].grid(row=row_index+i, column=1, sticky='W')
        stud_roles_combo[i].grid(row=row_index+i, column=2, padx=10, sticky='W')  
        # We attach a callback invoked when the combo boxes are selected.
        asso_names_combo[i].bind("<<ComboboxSelected>>", \
            lambda event, index=i: clb.asso_name_selected(event, index))
        stud_roles_combo[i].bind("<<ComboboxSelected>>", \
            lambda event: clb.stud_role_selected(event))