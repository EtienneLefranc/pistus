"""Configuration of the GUI.

"""

import tkinter.font as tkfont
from tkinter import ttk
from PIL import Image, ImageTk

# The PistusResa main window has a menu with three buttons. 
# We store here the currently active (selected) button, it'll change 
# color.
active_button = None

def load_icon_image():
    """Loads the icon image of PistusResa
    """
    icon = Image.open("./gui/icons/wacs-logo.jpg")
    icon = icon.resize((32, 32), Image.ANTIALIAS)
    icon = ImageTk.PhotoImage(icon)
    return icon

def reset_active_button():
    """Resets the active button (no button is selected).
    """
    global active_button
    if active_button is not None:
        active_button.configure(style="Menu.TButton")
        active_button = None

def set_active_button(btn):
    """Sets the active button. It'll change its color.

    Parameters
    ----------
    btn : ttk.Button
        The button that is set to become active.
    """
    global active_button
    btn.configure(style="Active.Menu.TButton")
    active_button = btn

def configure_style():
    """Configures the style of the GUI.
    """
    default_font_size = tkfont.nametofont("TkDefaultFont").cget("size")
    s = ttk.Style()
    s.theme_use("clam")
    
    s.configure('Menu.TFrame', background="#222323")
    s.configure('Error.TEntry', fieldbackground="red")
    s.configure('TNotebook', background="#f1f1f1", padding="20 10 20 10")
    s.configure('Tab.TFrame', background="#f1f1f1")
    s.configure('Sample.TFrame', background="yellow")
    s.configure('SampleBottom.TFrame', background="blue")
    s.configure('Empty.TFrame', background="white")
    s.configure('Table.TFrame', background="#dcdad5")
    s.configure('TLabel', background="#f1f1f1")
    s.configure('Sample.TLabel', background="red")
    s.configure('SampleTwo.TLabel', background="blue")
    s.configure('SampleThree.TLabel', background="yellow")
    s.configure('SampleFour.TLabel', background="green")
    s.configure('Header.TLabel', background="#dcdad5", font=('TkDefaultFont', default_font_size + 2, tkfont.BOLD) )
    s.configure('Check.TLabel', background="#f1f1f1", foreground='red')
    s.configure('TRadiobutton', background="#f1f1f1")

    s.configure('Menu.TButton', background="#222323", \
        foreground="white", font=('TkDefaultFont', default_font_size + 5), borderwidth=0)
    s.map("Menu.TButton",
        background=[('active', 'black')]
    )
    s.configure('Active.Menu.TButton', background="#0074a2")
    s.map("Active.Menu.TButton",
        background=[]
    )