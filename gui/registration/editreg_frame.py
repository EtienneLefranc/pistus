"""Edit registration tab

Definition of the tab where the user can edit a new registration to a Pistus edition.
"""

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from PIL import Image, ImageTk
import gui.registration.editreg_callbacks as clb
import utils

# The preferred width of the control labels.
# This is set to prevent the window to shrink and to enlarge depending on the length of the error messages.
# The width is different based on the language of the interface.
control_labels_width = {"en": 24, "fr": 35}

def add_widgets(edit_reg_tab, messages_bundle, cursor, conn, lang):
    """Adds the widgets to the tab
    
    Parameters
    ----------
    edit_reg_tab : ttk.Frame
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
    check_image = utils.load_check_image()

    # The student frame, where we find all the data fields relative to a student.
    student_frm = ttk.Frame(edit_reg_tab, style="Tab.TFrame")
    student_widgets(student_frm, messages_bundle, lang)
    
    # The registration frame, where we find the list of all the registrations of a student.
    registration_frm = ttk.Frame(edit_reg_tab, style="Tab.TFrame")
    scroll_registration_frm = registration_widgets(registration_frm, messages_bundle)

    # The message area, where we find the message area (where messages are displayed to the user).
    message_area_frm = ttk.Frame(edit_reg_tab, style="Tab.TFrame")
    message_ctrl_label = ttk.Label(message_area_frm, borderwidth=0, width=control_labels_width[lang], \
        anchor= tk.CENTER, style="Check.TLabel")
    message_ctrl_label.pack(fill="both", expand=True, padx=20, pady=10)
    clb.add_message_control_label(message_ctrl_label)

    # The buttons frame, where we find the buttons.
    buttons_frm = ttk.Frame(edit_reg_tab, style="Tab.TFrame")
    buttons_frame_widgets(buttons_frm, messages_bundle)

    # We add the frames to the edit registration tab.
    student_frm.pack(fill="both", expand=True, padx=20, pady=10)
    registration_frm.pack(fill="both", expand=True, padx=20, pady=10)
    message_area_frm.pack(fill="both", expand=True, padx=20, pady=10)
    buttons_frm.pack(fill="both", expand=True, padx=20, pady=10)
    
    # We initialize the fields.
    clb.init(messages_bundle, check_image, edit_reg_tab, scroll_registration_frm, cursor, conn)
    clb.reset()

def student_widgets(student_frm, messages_bundle, lang):
    """Creates the widgets of the student frame.

    Parameters
    ----------
    student_frm : ttk.Frame
        The student frame.
    messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    lang : string
        The language of the interface.
    """

    # We add the labels.
    ttk.Label(student_frm, text=messages_bundle["stud_number"] + " *").grid(row=0, column=0, padx=10, pady=10, sticky='w')
    ttk.Label(student_frm, text=messages_bundle["first_name"]).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    ttk.Label(student_frm, text=messages_bundle["last_name"]).grid(row=2, column=0, padx=10, pady=10, sticky='w')

    # Student number text entry.
    stud_number = tk.StringVar("")
    stud_number.trace("w", \
        lambda name, index, mode: clb.stud_number_updated())
    stud_number_entry = ttk.Entry(student_frm, textvariable=stud_number)
    stud_number_entry.bind('<FocusOut>', lambda event: clb.find_student(event))
    stud_number_entry.grid(row=0, column=1, sticky="we")
    clb.add_stud_number_entry((stud_number_entry, stud_number))

    # First name text entry.
    first_name = tk.StringVar("")
    first_name_entry = ttk.Entry(student_frm, state="disabled", textvariable=first_name)
    first_name_entry.grid(row=1, column=1, sticky="w")
    clb.add_first_name_entry((first_name_entry, first_name))

    # Last name text entry.
    last_name = tk.StringVar("")
    last_name_entry = ttk.Entry(student_frm, state="disabled", textvariable=last_name)
    last_name_entry.grid(row=2, column=1, sticky="w")
    clb.add_last_name_entry((last_name_entry, last_name))

    # The control labels.
    stud_number_control_label = ttk.Label(student_frm, borderwidth=0, \
        width=control_labels_width[lang], style="Check.TLabel")
    stud_number_control_label.grid(row=0, column=2, padx=10, sticky='w')
    clb.add_stud_number_control_label(stud_number_control_label)

    # We add the control labels for first and last name even if they are not used.
    # This way, the width of the window does not change depending on the length of the message 
    # in the username control area.
    ttk.Label(student_frm, borderwidth=0, \
        width=control_labels_width[lang], style="Check.TLabel").grid(row=1, column=2, padx=10, sticky='w')
    ttk.Label(student_frm, borderwidth=0, \
        width=control_labels_width[lang], style="Check.TLabel").grid(row=2, column=2, padx=10, sticky='w')

def registration_widgets(registration_frm, messages_bundle):
    """Creates the widgets of the registration frame.

    Parameters
    ----------
    registration_frm : ttk.Frame
        The registration frame
    messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.

    Returns:
    ttk.Frame
        A scrollable frame that is bound to contain the list of all registrations of a student.
    """
    
    # We create a frame with a vertical scrollbar. 
    # In this frame, we find the list of all registrations of a student.
    # If the list is larger than the frame, a vertical scrollbar appears that 
    # helps the student browse the list.
    canvas = tk.Canvas(registration_frm)
    scrollbar = ttk.Scrollbar(registration_frm, orient="vertical", command=canvas.yview)
    scroll_registration_frm = ttk.Frame(canvas, style="Table.TFrame")

    # Configuration of the canvas containing the frame with the scrollbar
    def config_canvas(e):
        # Define the scrollable region.
        canvas.configure(scrollregion=canvas.bbox("all"))
        # The scrollbar must appear at the top of the frame.
        canvas.yview_moveto(0)

    scroll_registration_frm.bind(
        "<Configure>",
        config_canvas
    )
    
    canvas_frm = canvas.create_window((0, 0), window=scroll_registration_frm, anchor="center")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Configuration of the frame so that it covers that whole scrollable region.
    canvas.bind(
        "<Configure>", 
        lambda e: canvas.itemconfig(canvas_frm, width=e.width)
    )
    
    # We configure the scrollable frame so that its widgets 
    # are uniformly spread across the frame.
    for i in range(4):
        scroll_registration_frm.columnconfigure(i, weight=1)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return scroll_registration_frm

def buttons_frame_widgets(buttons_frm, messages_bundle):
    """Creates the widgets of the buttons frame.

    Parameters
    ----------
    buttons_frm : ttk.Frame
        The buttons frame
    messages_bundle : dictionary
        The dictionary containing all the messages shown in the GUI.
    """

    # The button Edit.
    edit_button = ttk.Button(buttons_frm, state="disabled", \
        text=messages_bundle["edit_button"], command=clb.edit_registration)
    edit_button.grid(row=0, column=0, padx=10, pady=10, sticky='n')
    clb.add_edit_button(edit_button)

    # The button Delete.
    delete_button = ttk.Button(buttons_frm, state="disabled", \
        text=messages_bundle["delete_button"], command=clb.delete_registration)
    delete_button.grid(row=0, column=1, padx=10, pady=10, sticky='n')
    clb.add_delete_button(delete_button)

    # The button Clear.
    clear_button = ttk.Button(buttons_frm, \
        text=messages_bundle["clear_button"], command=clb.clear_action)
    clear_button.grid(row=0, column=2, padx=10, pady=10, sticky='n')
    clb.add_clear_button(clear_button)

    # The button Cancel.
    cancel_button = ttk.Button(buttons_frm, \
        text=messages_bundle["cancel_button"], command=clb.cancel_action)
    cancel_button.grid(row=0, column=3, padx=10, pady=10, sticky='n')
    clb.add_cancel_button(cancel_button)

    # We uniformly spread the buttons in the buttons frame.
    for i in range(4):
        buttons_frm.columnconfigure(i, weight=1)