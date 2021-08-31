# This file is part of Zoom Autojoiner GUI.

# Zoom Autojoiner GUI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Zoom Autojoiner GUI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Zoom Autojoiner GUI.  If not, see <https://www.gnu.org/licenses/>.

import time
import logging
import datetime
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox
from tkinter import N, S, E, W
from typing import Callable

from zoom_autojoiner_gui.constants import (
    ICON_FILE, 
    THEME_FILE, 
    DB_URL, 
    PYAG_PICS_DIR,
    EXTENSIONS
)
from zoom_autojoiner_gui.controllers import (
    TkinterTheme,
    DatabaseHandler,
    Autojoiner
)
from zoom_autojoiner_gui.dialogs import (
    NewMeetingDialog,
    EditMeetingDialog
)
from zoom_autojoiner_gui.extensions import (
    load_extensions,
    ExtensionHandler
)


logger = logging.getLogger(__name__)


class ApplicationMenuBar(tk.Menu):
    """ApplicationMenuBar

    Creates the menu bar for the application.
    
    Args:
        root_element: The root MainWindow compatible class.
        meeting_list_frame: The MeetingListFrame compatible class.
    """
    def __init__(self, root_element: tk.Tk, 
            meeting_list_frame: tk.Frame = None) -> None:
        # Initialise the TK Menu Bar
        super().__init__(root_element)

        # The Root Element of tk.Tk
        self.root_element = root_element

        # If the meeting list frame has been supplied, store
        # it, or else leave it as None
        self.__meeting_list_frame = meeting_list_frame

        # Make List to Menu
        try:
            # logger.info("Attepting to render menu bar..")
            self.make_list_to_menu([
                # Application menu
                ["Application", [
                    # ["Clear Data", None, None, None],

                    # Quit the application
                    ["Quit", lambda: root_element.destroy(), "<Control-q>", 
                        lambda event: root_element.destroy()],
                    ],
                ],
                # Meetings menu
                ["Meetings", [
                    # Add meeting submenu
                    ["Add Meeting", lambda: self.launch_add_meeting_dialog(), 
                        "<Control-n>", lambda event: \
                            self.launch_add_meeting_dialog()],
                    # ["Edit Meeting", None, None, None],
                    # ["Delete Meeting", None, None, None],
                    ],
                ],
                ])
        except Exception as e:
            # If an error occured while rendering the menu bar,
            # put that in the error log and exit.
            logger.error("Failed to render menu bar, exiting...", 
                exc_info=True)
            messagebox.showerror("Error", ("An exception has occured.\n"
                "Error Details:\n%s") % (str(e)))
            exit(1)

        # Configure menu to be used by the application.
        root_element.config(menu=self)

    def set_meeting_list_frame(self, frame:tk.Frame) -> None:
        """set_meeting_list_frame

        Sets the frame of the meeting list.

        Args:
            frame: 
                A TK frame which has similar methods to MeetingListFrame.

        Returns:
            Nothing.
        """
        self.__meeting_list_frame = frame

    def make_list_to_menu(self, main_menu: list) -> None:
        """make_list_to_menu
        
        Makes a list to a usuable menu.
        
        Args:
            main_menu: 
                This list contains the menu to be made in the below
                format.
                [
                    ["Main Menu", [
                        ["SubItem", Command, shortcut key, command],
                        ["SubItem2", COmmand, shortcut key],
                        ],
                    ],
                ]
        """
        for menu_item in main_menu:
            menu = tk.Menu(self, tearoff = "off") # Init menu
            for submenu_item in menu_item[1]:
                # Create subitem
                if submenu_item[2] != None:
                    skey = submenu_item[2][1:-1]
                else:
                    skey = None
                menu.add_command(label=submenu_item[0], 
                    command=submenu_item[1], accelerator=skey)
                # Shortcut key
                if submenu_item[2] != None:
                    self.root_element.bind_all(submenu_item[2], 
                        submenu_item[3])

            # Add menu to app
            self.add_cascade(label=menu_item[0], menu=menu)

    def launch_add_meeting_dialog(self) -> None:
        """launch_add_meeting_dialog
        
        Launch 'ADD MEETING' dialog
        """
        # root = tk.Tk()
        # app = 
        NewMeetingDialog(tk_root_element = self.root_element, 
            tk_frame_handle=self.__meeting_list_frame)
        # root.mainloop()


class MeetingListFrame(tk.Frame):
    """MeetingListFrame
        
    This class creates the frame that displays 
    the list of meetings.
    
    Args:
        root_element:
            The MainWindow compatible class that is passed to the buttons.
        tk_theme_object:
            The TKTheme object used for styling elements.
        autojoiner_handle:
            The Autojoiner object used for Join 
            Meeting buttons.
    """
    __components = []        # TK/TTK widgets
    __current_table_row = 1  # Current row of the table
    def __init__(self, root_element: tk.Tk, 
            tk_theme_object: TkinterTheme = None, 
            autojoiner_handle: Autojoiner = None) -> None:
        super().__init__(root_element)

        #: We create a Database Handler here.
        self.__dbh = DatabaseHandler(DB_URL)

        self.root_element = root_element #: The root element.

        # If the theme object is not provided, make one, else use the one 
        # given
        if tk_theme_object == None:
            self.tk_theme = TkinterTheme(THEME_FILE) #: Tkinter Theme object
        else:
            self.tk_theme = tk_theme_object

        # Autojoiner
        if autojoiner_handle:
            self.__autojoiner_handle = autojoiner_handle
        else:
            self.__autojoiner_handle = Autojoiner(PYAG_PICS_DIR)

        # Sticky grid that resizes according to window size.
        # tk.Grid.rowconfigure(root_element, row, weight=1)
        # tk.Grid.columnconfigure(root_element, column, weight=1)

        # Grid
        # self.grid(row=row, column=column, sticky=N+S+E+W)

        # Widgets
        # for i in range(0, 10):
        #     for j in range(0, 10):
        #         self.create_ttk_button("Row:%d Column:%d" % (i, j), i, j)
        self.create_column_headers(["Meeting Start Time", "Meeting ID", 
                "Meeting Password", "Join Meeting", "Edit/Delete Meeting"])

        # Populate table
        self.populate_table_from_db()

    def __stickify(self, row: int = 0, column: int = 0) -> None:
        """Auto resize the TK widget according to window size
        
        Args:
            row: The row in the TK grid system
            column: The column in TK grid.
        """
        # Should only stick vertically.
        # tk.Grid.rowconfigure(self, row, weight=1)
        tk.Grid.columnconfigure(self, column, weight=1)

    def create_ttk_button(self, text: str, row: int = 0, column: int = 0,
            command: Callable = None, sticky: str = N+S+E+W,
            stickify: bool = True) -> ttk.Button:
        """create_ttk_button
        
        Creates a TTK Button and adds resizing capability.
        
        Args:
            text: Text of the TTK button.
            row: The row in the TK grid system
            column: The column in TK grid.
            command: The command associated with the TK button.
            sticky: TK's sticky attribute
            stickify: Make the width adjust to that of parent container.

        Returns:
            The TTK Button object, for further manipulation.
        """
        # Auto resize
        if stickify: self.__stickify(row, column)

        # Create component
        btn = ttk.Button(self, text=text, command=command)
        btn.grid(row=row, column=column, sticky=sticky)

        # Append to component list and return index
        self.__components.append(btn)
        return self.__components[-1]
        # return len(self.__components) - 1

    def create_tk_label(self, text: str, row: int = 0, column: int = 0, 
            sticky :str = N+S+E+W, stickify: bool = True, 
            *args: tuple, **kwargs: dict) -> tk.Label:
        """create_tk_label
        
        Creates a TK Label and adds resizing capability.
        
        Args:
            text: Text of the TK label.
            row: The row in the TK grid system
            column: The column in TK grid.
            command: The command associated with the TK label.
            sticky: TK's sticky attribute
            stickify:
                Make the width adjust to that of parent container.

        Returns:
            The TK Label object, for further manipulation.
        """
        # Auto resize
        if stickify: self.__stickify(row, column)

        # Create component
        lbl = tk.Label(self, text=text, *args, **kwargs)
        lbl.grid(row=row, column=column, sticky=sticky)

        # Append to component list and return index
        self.__components.append(lbl)
        return self.__components[-1]
        # return len(self.__components) - 1

    # Table populating functions:
    def create_column_headers(self, col_headers: list) -> int:
        """create_column_headers

        Creates the column headers.
        
        Args:
            col_headers: The list of column headers.
                
        Returns:
            A integer with the total number of columns.
        """
        col_no = 0
        for col_header in col_headers:
            theme_dict = self.tk_theme.get_styling("table_header")
            self.create_tk_label(col_header, column = col_no, **theme_dict)
            col_no += 1

        return col_no

    def create_table_row(self, record_id: int, meeting_time: datetime.datetime,
                         meeting_id: str, meeting_password: str) -> None:
        """create_table_row
        
        Creates a row for the table.
        
        Args:
            record_id: The ID in database. Used for edit meeting dialog.
            meeting_time: The time of the meeting.
            meeting_id: The ID of the meeting.
            meeting_password: The meeting password.

        Returns:
            Nothing.
        """
        row_no = self.__current_table_row
        styling = self.tk_theme.get_styling("table_content")
        self.create_tk_label(meeting_time.strftime("%a %d %B %Y %I:%M:%S %p"),
            row=row_no, column=0, **styling)
        self.create_tk_label(meeting_id, row=row_no, column=1, **styling)
        self.create_tk_label(meeting_password, row=row_no, column=2, **styling)
        self.create_ttk_button("Join meeting", row=row_no, column=3, 
            command=lambda: self.__autojoiner_handle.join_zm_mtg(meeting_id,
                meeting_password))
        self.create_ttk_button("Edit/Delete meeting", row=row_no, column=4, 
            command=lambda: EditMeetingDialog(record_id, tk_root_element = \
                self.root_element, tk_frame_handle=self))
        self.__current_table_row += 1

    # Controller/View Interface
    def populate_table_from_db(self) -> None:
        """populate_table_from_db
        
        Populate the table from the Database.
        """
        try:
            # logger.info("Attempting to load meeting data from DB...")
            meetings = self.__dbh.get_mtg_data_to_list()
            for mtg in meetings:
                self.create_table_row(mtg["id"], mtg["mtg_time"], 
                    mtg["mtg_id"], mtg["mtg_password"])
        except Exception as e:
            logger.error("Failed to load meeting data, exiting...", 
                exc_info=True)
            messagebox.showerror("Error", 
                "An exception has occured.\nError Details:\n%s" % (str(e)))
            exit(1)
        else:
            logger.info("Loaded meeting data successfully.")

    def reload_table(self) -> None:
        """reload_table

        Reload and rebuilt the TK Table by calling the 
        applicable functions.
        """
        for cell in self.winfo_children():
            cell.destroy()
        self.create_column_headers(["Meeting Start Time", "Meeting ID", 
            "Meeting Password", "Join Meeting", "Edit/Delete Meeting"])

        # Populate table
        self.populate_table_from_db()


class ApplicationStatusBar(tk.Label):
    """ApplicationStatusBar
    
    Status bar is used for iteration tasks, for example, to find out if
    it is time to join the meeting.
    
    Args:
        root_element: the MainWindow compatible Tk class.
        autojoiner_handle: The Autojoiner class to use.
    """
    def __init__(self, root_element: tk.Tk, 
            autojoiner_handle: Autojoiner = None) -> None:
        super().__init__(root_element, text="Loading…", bd=1, 
            relief=tk.SUNKEN, anchor=W)

        # Autojoiner
        if autojoiner_handle:
            self.__autojoiner_handle = autojoiner_handle
        else:
            # Create one if not supplied
            self.__autojoiner_handle = Autojoiner(PYAG_PICS_DIR)

        self.iterator()

    def check_for_meeting(self) -> None:
        """check_for_meeting
        
        Check for meetings. If there is one now, join.
        Or else just continue.
        """
        if self.__autojoiner_handle.check_for_meeting():
            logger.info("Status Bar - Meeting now.")
            self["text"] = ("There is a meeting now. Zoom Autojoiner is"
                " initiating the joining process.")
            mtg_id = self.__autojoiner_handle.check_for_meeting()["mtg_id"]
            mtg_pw = self.__autojoiner_handle.check_for_meeting()["mtg_password"]
            self["text"] = ("There is a meeting now. Zoom Autojoiner has "
                "initiated the joining process.")
            logger.info("Status Bar - Joining Meeting")
            self.__autojoiner_handle.join_zm_mtg(mtg_id, mtg_pw)
            self["text"] = ("Zoom Autojoiner has finished the joining "
                "process. There will be a pause for 60 seconds now.")
            logger.info("Status Bar - Sleeping")

            # This line causes the program to hang. However, it prevents
            # the Autojoiner to rejoin the meeting repeatedly.
            time.sleep(60)

    def iterator(self) -> None:
        """iterator

        The iterator checks for meetings every 10 seconds.
        It calls the `check_for_meeting` method to find if
        a meeting is present.
        """
        logger.info("Status Bar - Iterating")
        self["text"] = "Checking for meeting"
        self.check_for_meeting()
        self["text"] = "Running"
        self.after(10000, self.iterator)
        #          ^ Todo - let this value be set in config file.


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Object instances
        self.__tk_theme = TkinterTheme(THEME_FILE)           # TK Styling object
        self.__autojoiner_handle = Autojoiner(PYAG_PICS_DIR) # Autojoiner handler

        # Window Titles
        self.title('Zoom Autojoiner')
        try:
            self.iconbitmap(ICON_FILE)
        except:
            logger.warning("Could not load Window icon", exc_info=True)

        # Menu Bar
        self.__menu_bar = ApplicationMenuBar(self)

        # Title
        self.create_tk_label("Zoom AutoJoiner - My Meeting List", sticky=N+E+W,
            stickify=False, **self.__tk_theme.get_styling("title"))
        
        # Window Elements
        # Meetings List
        self.__meeting_list_frame = MeetingListFrame(self, self.__tk_theme, 
            autojoiner_handle=self.__autojoiner_handle)
        # Elasticity
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        # Positioning
        self.__meeting_list_frame.grid(row=1, column=0, sticky=N+S+E+W)

        # Give menubar the meeting list farme
        self.__menu_bar.set_meeting_list_frame(self.__meeting_list_frame)

        # Statusbar
        self.__statusbar = ApplicationStatusBar(self, autojoiner_handle=
            self.__autojoiner_handle)
        
        # Elasticity
        # tk.Grid.rowconfigure(self, 2, weight=1)
        # tk.Grid.columnconfigure(self, 0, weight=1)
        # Positioning
        self.__statusbar.grid(row=2, column=0, sticky=N+S+E+W)

        # load extensions
        if EXTENSIONS.getboolean("enabled"):
            # if extensions are enabled
            self.__ext_class = ExtensionHandler(EXTENSIONS)
            if self.__ext_class.load_extensions():
                self.__ext_class.give_extensions_prefs()
                self.__ext_class.give_extensions_objects(self, self.__menu_bar,
                    self.__meeting_list_frame)
                self.__ext_class.run_extensions()

    def __stickify(self, row = 0, column = 0):
        """Auto resize the TK widget according to window size"""
        tk.Grid.rowconfigure(self, row, weight=1)
        tk.Grid.columnconfigure(self, column, weight=1)

    def create_tk_label(self, text, row = 0, column = 0, sticky=N+S+E+W, stickify=True, *args, **kwargs):
        """Creates a TK Label and adds resizing capability."""
        # Auto resize
        if stickify: self.__stickify(row, column)

        # Create component
        lbl = tk.Label(self, text=text, *args, **kwargs)
        lbl.grid(row=row, column=column, sticky=sticky)


if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1) # High DPI
    except:
        pass
    window = MainWindow()
    window.mainloop()


# Todo
# -[] After PyAG autojoin, add 1s refresher to a label