"""The main window of the PistusResa GUI.
"""

import tkinter as tk
import csv

from tkinter import ttk
import gui.gui_config as config
from gui.student.frame import add_widgets as stud_add_widgets
from gui.registration.newreg_frame import add_widgets as reg_add_widgets
from gui.registration.editreg_frame import add_widgets as reg_edit_widgets
import mdeadline
from PIL import Image, ImageTk

# The messages bundle
messages_bundle = {}

# The object used to query the database.
cursor = None

# The object used to connect to the database.
conn = None

# The language of the application.
lang = None

# When the user clicks one of the buttons on the left menu, 
# a tab is opened on the right side of the window.
# There are three tabs: one for managing the student data, another to
# add a new registration and another to edit the registrations.
tabs = {"student" : None, "add_registration": None, "edit_registration": None}

# The ttk.Notebook (frame) containing the above tabs.
nb = None

def destroy_tab(event, tab_name, button):
    """Destroys a given tab.

    Parameters
    ----------
    event : 
        Information on the event.
    tab_name : string
        The name of the tab to destroy.
    button : ttk.Button
        The button on the left side used to open the tab.
    """
    global nb
    config.reset_active_button()
    button.state(["!disabled"])
    tabs[tab_name] = None
    if not is_tab_open():
        nb.destroy()
        nb = None

def select_tab(event, button):
    """Invoked when a tab is selected.

    Parameters
    ----------
    event : 
        The information about the selection event.
    button : ttk.Button
        The button used to open the selected tab.
    """
    # When a tab is selected, the button used to open it becomes the active one and 
    # changes its color.
    config.reset_active_button()
    config.set_active_button(button)

def is_tab_open():
    """Checks whether any tab is open.

    Returns
    -------
    bool
        True if any of the three tabs is open, False otherwise.
    """
    for value in list(tabs.values()):
        if value is not None:
            return True
    return False

def open_add_edit_student_tab(window, btn_add_edit_student):
    """Opens the tab used to manage the student data.

    Parameters
    ----------
    window : tk.Tk
        The PistusResa main window.
    btn_add_edit_student : ttk.Button
        The button used to open the tab.

    """
    global nb
    # If no tab is open already, we have to create the notebook that will 
    # contain the tab.
    if not is_tab_open():
        nb = ttk.Notebook(window)
    
    # We set the button used to open the tab as active
    config.reset_active_button()
    config.set_active_button(btn_add_edit_student)
    # The button will be disabled. This means that we cannot open this tab twice.
    btn_add_edit_student.state(["disabled"])
    
    # Create the frame that contains the tab.
    stud_tab = ttk.Frame(nb, style="Tab.TFrame")

    # Specify the callback to invoke when the tab is destroyed.
    stud_tab.bind("<Destroy>", lambda event: destroy_tab(event, "student", btn_add_edit_student))
    
    # Specify the callback to invoke when the tab is selected.
    stud_tab.bind("<Visibility>", lambda event: select_tab(event, btn_add_edit_student))
    
    # Add the widgets to the tab.
    stud_add_widgets(stud_tab, messages_bundle, cursor, conn, lang)
    
    # Adds the tab to the notebook in the proper position.
    if tabs["add_registration"] is not None:
        nb.insert(tabs["add_registration"], stud_tab, text=messages_bundle["add_edit_student"], sticky='nsew')
    elif tabs["edit_registration"] is not None:
        nb.insert(tabs["edit_registration"], stud_tab, text=messages_bundle["add_edit_student"], sticky='nsew')
    else:
        nb.insert("end", stud_tab, text=messages_bundle["add_edit_student"], sticky='nsew')
    
    # Adds the notebook to the window.
    nb.grid(row=0, column=0, ipadx=10, sticky="nsew")

    # Sets the newly created tab as selected.
    nb.select(stud_tab)
    tabs["student"] = stud_tab

    # Updates the window to force the tab to display.
    window.update()

def open_add_registration_tab(window, btn_add_registration):
    """Opens the tab used to add a new registration.

    Parameters
    ----------
    window : tk.Tk()
        The PistusResa main window.
    btn_add_registration : ttk.Button
        The button used to open the tab.
    """
    global nb
    # If no tab is open already, we have to create the notebook that will 
    # contain the tab.
    if not is_tab_open():
       nb = ttk.Notebook(window)

    # We set the button used to open the tab as active
    config.reset_active_button()
    config.set_active_button(btn_add_registration)
    # The button will be disabled. This means that we cannot open this tab twice.
    btn_add_registration.state(["disabled"])

    # Create the frame that contains the tab.   
    add_reg_tab = ttk.Frame(nb, style="Tab.TFrame")

    # Specify the callback to invoke when the tab is destroyed.
    add_reg_tab.bind("<Destroy>", lambda event: destroy_tab(event, "add_registration", btn_add_registration))

    # Specify the callback to invoke when the tab is selected.
    add_reg_tab.bind("<Visibility>", lambda event: select_tab(event, btn_add_registration))
    
    # Add the widgets to the tab.
    reg_add_widgets(add_reg_tab, messages_bundle, cursor, conn, lang)

    # Adds the tab to the notebook in the proper position.
    if tabs["edit_registration"] is not None:
        nb.insert(tabs["edit_registration"], add_reg_tab, text=messages_bundle["add_registration"], sticky='nsew')
    else:
        nb.insert("end", add_reg_tab, text=messages_bundle["add_registration"], sticky='nsew')
    
    # Adds the notebook to the window.
    nb.grid(row=0, column=0, ipadx=10, sticky="nsew")

    # Sets the newly created tab as selected.
    nb.select(add_reg_tab)

    tabs["add_registration"] = add_reg_tab 

def open_edit_registration_tab(window, btn_edit_registration):
    """Opens the tab used to edit a  registration.

    Parameters
    ----------
    window : tk.Tk()
        The PistusResa main window.
    btn_edit_registration : ttk.Button
        The button used to open the tab.
    """
    # If no tab is open already, we have to create the notebook that will 
    # contain the tab.
    global nb
    if not is_tab_open():
        nb = ttk.Notebook(window)

    # We set the button used to open the tab as active
    config.reset_active_button()
    config.set_active_button(btn_edit_registration)
    # The button will be disabled. This means that we cannot open this tab twice.
    btn_edit_registration.state(["disabled"])

    # Create the frame that contains the tab. 
    edit_reg_tab = ttk.Frame(nb, style="Tab.TFrame")

    # Specify the callback to invoke when the tab is destroyed.
    edit_reg_tab.bind("<Destroy>", lambda event: destroy_tab(event, "edit_registration", btn_edit_registration))

    # Specify the callback to invoke when the tab is selected.
    edit_reg_tab.bind("<Visibility>", lambda event: select_tab(event, btn_edit_registration))
    
    # Add the widgets to the tab.
    reg_edit_widgets(edit_reg_tab, messages_bundle, cursor, conn, lang)
    
    # Adds the tab to the notebook in the proper position.
    nb.insert("end", edit_reg_tab, text=messages_bundle["edit_registration"], sticky='nsew')
    
    # Adds the notebook to the window.
    nb.grid(row=0, column=0, ipadx=10, sticky="nsew")

    # Sets the newly created tab as selected.
    nb.select(edit_reg_tab)
    tabs["edit_registration"] = edit_reg_tab
    

def open_main_window(_cursor, _conn, _messages_bundle, _lang):
    """Opens the PistusResa main window.

    Parameters
    ----------
    _cursor : 
        The object used to query the database.
    _conn : 
        The object used to connect to the database.
    _messages_bundle : dictionary
        The messages bundle
    _lang : string
        The language of the application.
    """
    global messages_bundle
    global cursor
    global conn
    global lang
    
    # Initializes the global variables.
    messages_bundle = _messages_bundle
    cursor = _cursor
    conn = _conn
    lang = _lang

    # Open a new window
    window = tk.Tk()
    window.title("PistusResa")

    # Add an icon to the window.
    icon = config.load_icon_image()
    window.iconphoto(False, icon)

    # Set the window as non-resizable.
    window.resizable(False, False)

    # The main window consists of a 1x2 grid. 
    # We configure the row so as the widgets span the height of the window.
    # THe second column (the one that hosts the tabs) spans the whole space after the column 0
    # (that contains the left menu).
    window.rowconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)

    # Configure the style of the window.
    config.configure_style()

    # The frame that contains the image of the association WACS.
    frm_intro = ttk.Frame(window)

    # Add this frame to the second column (next to the left menu).
    frm_intro.grid(row=0, column=1, sticky='nsew')

    # Add the background image.
    image = Image.open("./gui/icons/wacs-logo.jpg")
    image = image.resize((400, 400), Image.ANTIALIAS)
    image.putalpha(128)
    image = ImageTk.PhotoImage(image)
    ttk.Label(frm_intro, borderwidth=0, image=image).grid(row=0, column=0)
    
    # Add the left menu with the three buttons.
    frm_menu = ttk.Frame(window, style="Menu.TFrame")
    btn_add_edit_stud = ttk.Button(frm_menu, text=messages_bundle["add_edit_student"], style="Menu.TButton", \
        command=lambda: open_add_edit_student_tab(frm_intro, btn_add_edit_stud))
    btn_add_edit_stud.grid(row=0, column=0, padx=5, pady=5, ipadx=20, ipady=5, sticky='ew')
    
    btn_add_registration = ttk.Button(frm_menu, text=messages_bundle["add_registration"], style="Menu.TButton", \
        command=lambda: open_add_registration_tab(frm_intro, btn_add_registration))
    btn_add_registration.grid(row=1, column=0, padx=5, pady=0, ipadx=20, ipady=5, sticky='ew')
    
    btn_edit_registration = ttk.Button(frm_menu, text=messages_bundle["edit_registration"], style="Menu.TButton", \
        command=lambda: open_edit_registration_tab(frm_intro, btn_edit_registration))
    btn_edit_registration.grid(row=2, column=0, padx=5, pady=0, ipadx=20, ipady=5, sticky='ew')
    
    frm_menu.grid(row=0, column=0, sticky='nsew')
    frm_menu.columnconfigure(0, weight=1)

    # Start the deadline module that runs in the background.
    mdeadline.deadline_management_init(window, cursor, conn)
    window.after(0, mdeadline.deadline_management)

    # Start the event loop
    window.mainloop()