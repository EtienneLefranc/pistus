"""Used to play with the code in order to learn the basics of Tkinter.

"""

# Import the library tkinter
import tkinter as tk
# Import the ttk widgets of tkinter
from tkinter import ttk
# Import the function configure_style
from gui_config import configure_style


###################### You'll copy here the code to play with ######################
combo_boxes = {}
buttons = {}
control_labels = {}

window = None


def combo_selected():
    current_color = combo_boxes["color"].get()
    control_labels["color_ctrl"].configure(
        text="The selected color is {}".format(current_color))


def destroy_window():
    window.destroy()


window = tk.Tk()
window.title("Playground")
configure_style()
first_frm = ttk.Frame(window, style="Tab.TFrame")

ctrl_label = ttk.Label(first_frm)
control_labels["color_ctrl"] = ctrl_label
ctrl_label.pack()

colors = ["red", "green", "blue", "yellow"]
color_combo = ttk.Combobox(first_frm, values=colors)
combo_boxes["color"] = color_combo
color_combo.bind("<<ComboboxSelected>>",
                 lambda event: combo_selected())
color_combo.pack()

button = ttk.Button(first_frm, text="Destroy", command=destroy_window)
buttons["OK"] = button
button.pack()

first_frm.pack()
window.mainloop()


#####################################################################################
