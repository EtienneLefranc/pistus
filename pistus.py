"""The Entry point of the application.

When you execute this file as a Python script, the PistusResa main window 
(or the login window, if authorization is enabled in the configuration file) shows up.

PistuResa works this way:

1) It loads the application configuration from ./config/config
    * The configuration provides the values for a certain number of settings, such as
    the application language and the path to the database file. See the file ./config/config 
    to see the current settings of the application.

2) It loads the messages bundle. The messages bundle is the collection of 
text (button labels, warnings...) that is displayed in PistusResa GUI.
Each text message is identified by a key, so that in the source code each message is 
referred to by using its key. The actual textual message is not hard-coded in the 
application; the advantage is that we can easily change the interface language by 
providing PistuResa with a messages bundle in that language. 

3) It connects to the database, of which the file path is specified in the configuration file.

4) If authorization is enabled in the configuration file, a login window is displayed. 
When the user successfully logs in, the main window of the application pops up.

5) If authorization is not enabled, the main window of the application pops up immediately.

6) Whenever the user closes the application main window, PistusResa closes the connection to the 
database and stops its execution.


"""

import tkinter as tk
import sqlite3
import utils
from gui.mainwindow import open_main_window
from gui.login import open_login_window

# Loads the application configuration
config = utils.load_config()

# Loads the messages bundle in the appropriate language.
messages_bundle = utils.load_messages_bundle(config["bundle"] + config["lang"])

# Connects to the database.
conn = sqlite3.connect(config["db"])
# Enables the foreign key contraints support in SQLite.
conn.execute("PRAGMA foreign_keys = 1")
# Get the cursor for the connection. This object is used to execute queries 
# in the database.
cursor = conn.cursor()

# If configuration is enabled, we open the login window.
if config["auth"] == "yes":
    open_login_window(cursor, conn, messages_bundle, config["lang"])
else: # Otherwise, we open the main window.
    open_main_window(cursor, conn, messages_bundle, config["lang"])

# The following instructions are executed only when the user closes the 
# application main window. That means that the user doesn't want to use the application anymore, 
# so we close the connection to the database and we exit.
# 
cursor.close()
conn.close()

print("PistuResa is not running anymore")