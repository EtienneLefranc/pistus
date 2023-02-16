"""New registration tab

Definition of the tab where the user can add a new registration to a Pistus edition.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import gui.registration.newreg_callbacks as clb
import utils

# The preferred width of the control labels.
# This is set to prevent the window to shrink and to enlarge depending on the length of the error messages.
# The width is different based on the language of the interface.
control_labels_width = {"fr": 26, "en": 18}

def add_widgets(new_reg_tab, messages_bundle, cursor, conn, lang):
    """Adds the widgets to the tab
    
    Parameters
    ----------
    new_reg_tab : ttk.Frame
        The frame where all the widgets are added.
    messages_bundle : dictionary
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
    
    # Create the "data fields frame" containing all the data fields to fill
    # in in order to create a new registration.
    data_fields_frm = ttk.Frame(new_reg_tab, style="Tab.TFrame")
    _data_fields_widgets(data_fields_frm, messages_bundle, lang)

    # Create the message area frame, where messages are shown to the users to give them
    # a feedback on their actions.
    message_area_frm = ttk.Frame(new_reg_tab, style="Tab.TFrame")
    _message_area_widgets(message_area_frm)

    # Create the "buttons frame" containing the buttons (add, cancel, clear...).
    buttons_frm = ttk.Frame(new_reg_tab, style="Tab.TFrame")
    _buttons_frame_widgets(buttons_frm, messages_bundle)

    # Add the two frames to the student tab.
    data_fields_frm.pack(fill="both", expand=True, padx=20, pady=10)
    message_area_frm.pack(fill="both", expand=True, padx=20, pady=10)
    buttons_frm.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Initialization of the interface.
    clb.init(messages_bundle, check_image, new_reg_tab, cursor, conn)
    clb.reset()

def _data_fields_widgets(data_fields_frm, messages_bundle, lang):
    """Creates the widgets of the data fields frame.

    Parameters
    ----------
    data_fields_frm : ttk.Frame
        The data fields frame.
    messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    lang : string
        The language of the interface.
    """
    _student_widgets(data_fields_frm, messages_bundle, lang)
    _edition_widgets(data_fields_frm, messages_bundle, lang)
   
def _student_widgets(data_fields_frm, messages_bundle, lang):
    """Creates the widgets relative to the student data (student number, first name, last name).

    Parameters
    ----------
    data_fields_frm : ttk.Frame
        The data fields frame.
    messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    lang : string
        The language of the interface.
    """

    # The labels.
    ttk.Label(data_fields_frm, text=messages_bundle["stud_number"] + " *").grid(row=0, column=0, padx=10, pady=10, sticky='w')
    ttk.Label(data_fields_frm, text=messages_bundle["first_name"]).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    ttk.Label(data_fields_frm, text=messages_bundle["last_name"]).grid(row=2, column=0, padx=10, pady=10, sticky='w')

    # Student number text field.
    stud_number = tk.StringVar("")
    stud_number.trace("w", \
        lambda name, index, mode: clb.stud_number_updated())
    stud_number_entry = ttk.Entry(data_fields_frm, textvariable=stud_number)
    stud_number_entry.bind('<FocusOut>', lambda event: clb.find_student(event))
    stud_number_entry.grid(row=0, column=1, sticky="we")
    clb.add_stud_number_entry((stud_number_entry, stud_number))

    # First name text field.
    first_name = tk.StringVar("")
    first_name_entry = ttk.Entry(data_fields_frm, state="disabled", textvariable=first_name)
    first_name_entry.grid(row=1, column=1, sticky="w")
    clb.add_first_name_entry((first_name_entry, first_name))

    # Last name text field.
    last_name = tk.StringVar("")
    last_name_entry = ttk.Entry(data_fields_frm, state="disabled", textvariable=last_name)
    last_name_entry.grid(row=2, column=1, sticky="w")
    clb.add_last_name_entry((last_name_entry, last_name))

    # The control labels for the three previous fields.
    stud_number_control_label = ttk.Label(data_fields_frm, borderwidth=0, width=control_labels_width[lang], style="Check.TLabel")
    stud_number_control_label.grid(row=0, column=2, padx=10, sticky='w')
    clb.add_stud_number_control_label(stud_number_control_label)

    # The control labels for the first and last names are not used, but we need to add them in order to 
    # prevent the tab from shrinking when no error is shown in the other control labels.
    ttk.Label(data_fields_frm, borderwidth=0, width=control_labels_width[lang], style="Check.TLabel").grid(row=1, column=2, padx=10, sticky='w')
    ttk.Label(data_fields_frm, borderwidth=0, width=control_labels_width[lang], style="Check.TLabel").grid(row=2, column=2, padx=10, sticky='w')


def _edition_widgets(data_fields_frm, messages_bundle, lang):
    """Creates the widgets relative to the Pistus edition (year, registration fee, registration and payment date).

    Parameters
    ----------
    data_fields_frm : ttk.Frame
        The data fields frame.
    messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    lang : string
        The language of the interface.
    """

    # The labels.
    ttk.Label(data_fields_frm, text=messages_bundle["edition_year"] + " *").grid(row=3, column=0, padx=10, pady=10, sticky='w')
    ttk.Label(data_fields_frm, text=messages_bundle["registration_fee"] + " *").grid(row=4, column=0, padx=10, pady=10, sticky='w')
    ttk.Label(data_fields_frm, text=messages_bundle["registration_date"] + " *").grid(row=5, column=0, padx=10, pady=10, sticky='w')
    ttk.Label(data_fields_frm, text=messages_bundle["payment_date"]).grid(row=6, column=0, padx=10, pady=10, sticky='w')

    # The year text field.
    year = tk.StringVar("")
    year.trace("w", \
        lambda name, index, mode: clb.year_updated())
    year_entry = ttk.Entry(data_fields_frm, textvariable=year)
    year_entry.grid(row=3, column=1, sticky='w')
    year_entry.bind('<FocusOut>', lambda event: clb.find_pistus_edition(event))
    clb.add_year_entry((year_entry, year))

    # The registration fee text field.
    registration_fee = tk.StringVar("")
    registration_fee.trace("w", \
        lambda name, index, mode: clb.registration_fee_updated())
    registration_fee_entry = ttk.Entry(data_fields_frm, textvariable=registration_fee)
    registration_fee_entry.grid(row=4, column=1, sticky='w')
    clb.add_registration_fee_entry((registration_fee_entry, registration_fee))

    # The registratioin date text field.
    registration_date = tk.StringVar("")
    registration_date.trace("w", \
        lambda name, index, mode: clb.registration_date_updated())
    registration_date_entry = ttk.Entry(data_fields_frm, textvariable=registration_date)
    registration_date_entry.grid(row=5, column=1, sticky='w')
    clb.add_registration_date_entry((registration_date_entry, registration_date))

    # The payment date text field.
    payment_date = tk.StringVar("")
    payment_date.trace("w", \
        lambda name, index, mode: clb.payment_date_updated())
    payment_date_entry = ttk.Entry(data_fields_frm, textvariable=payment_date)
    payment_date_entry.grid(row=6, column=1, sticky='w')
    clb.add_payment_date_entry((payment_date_entry, payment_date))

    # The control labels for the four previous fields.
    year_control_label = ttk.Label(data_fields_frm, borderwidth=0, width=control_labels_width[lang], style="Check.TLabel")
    year_control_label.grid(row=3, column=2, padx=10, sticky='w')
    clb.add_year_control_label(year_control_label)

    registration_fee_control_label = ttk.Label(data_fields_frm, borderwidth=0, width=control_labels_width[lang], style="Check.TLabel")
    registration_fee_control_label.grid(row=4, column=2, padx=10, sticky='w')
    clb.add_registration_fee_control_label(registration_fee_control_label)

    registration_date_control_label = ttk.Label(data_fields_frm, borderwidth=0, width=control_labels_width[lang], style="Check.TLabel")
    registration_date_control_label.grid(row=5, column=2, padx=10, sticky='w')
    clb.add_registration_date_control_label(registration_date_control_label)

    payment_date_control_label = ttk.Label(data_fields_frm, borderwidth=0, width=control_labels_width[lang], style="Check.TLabel")
    payment_date_control_label.grid(row=6, column=2, padx=10, sticky='w')
    clb.add_payment_date_control_label(payment_date_control_label)

def _message_area_widgets(message_area_frm):
    """Adds the widgets in the message area frame.

    Parameters
    ----------
    message_area_frm : ttk.Frame
        The message area frame.
    """

    message_ctrl_label = ttk.Label(message_area_frm, borderwidth=0, anchor= tk.CENTER, style="Check.TLabel")
    message_ctrl_label.pack(fill="both", expand=True, padx=20, pady=10)
    clb.add_message_area_control_label(message_ctrl_label)

def _buttons_frame_widgets(buttons_frm, messages_bundle):
    """Creates the buttons in the buttons frame.

    Parameters
    ----------
    buttons_frm : ttk.Frame
        The data fields frame.
    messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    """

    # Configures the grid of the frame so that the buttons are uniformely spread across the frame,
    # both horizontally and vertically.
    buttons_frm.rowconfigure(0, weight=1)
    for i in range(3):
        buttons_frm.columnconfigure(i, weight=1)
    
    # The add button.
    add_button = ttk.Button(buttons_frm, state="disabled", \
        text=messages_bundle["add_button"], command=clb.add_registration)
    add_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
    clb.add_add_button(add_button)

    # The clear button.
    clear_button = ttk.Button(buttons_frm, \
        text=messages_bundle["clear_button"], command=clb.clear_action)
    clear_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
    clb.add_clear_button(clear_button)

    # The cancel button.
    cancel_button = ttk.Button(buttons_frm, \
        text=messages_bundle["cancel_button"], command=clb.cancel_action)
    cancel_button.grid(row=0, column=2, padx=10, pady=10, sticky='ew')
    clb.add_cancel_button(cancel_button)