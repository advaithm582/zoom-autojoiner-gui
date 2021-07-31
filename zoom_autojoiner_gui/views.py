import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import N, S, E, W
import tkinter.font as tkFont
import time, logging
from zoom_autojoiner_gui.constants import ICON_FILE, THEME_FILE, DB_URL, PYAG_PICS_DIR
from zoom_autojoiner_gui.controllers import TkinterTheme, DatabaseHandler, Autojoiner
from zoom_autojoiner_gui.dialogs import NewMeetingDialog, EditMeetingDialog

logger = logging.getLogger(__name__)

class ApplicationMenuBar(tk.Menu):
    def __init__(self, root_element):
        """Creates the menu bar for the application."""
        # Init Menu Bar
        super().__init__(root_element)

        self.root_element = root_element
        
        # Format
        #    [
        #        ["Main Menu", [
        #            ["SubItem", Command, shortcut key, command],
        #            ["SubItem2", COmmand, shortcut key],
        #            ],
        #         ],
        #    ]

        # Make List to Menu
        try:
            # logger.info("Attepting to render menu bar..")
            self.make_list_to_menu([
                ["Application", [
                    ["Clear Data", None, None, None],
                    ["Quit", lambda: root_element.destroy(), "<Control-q>", lambda event: root_element.destroy()],
                    ],
                ],
                ["Meetings", [
                    ["Add Meeting", lambda: self.launch_add_meeting_dialog(), "<Control-n>", lambda event: self.launch_add_meeting_dialog()],
                    ["Edit Meeting", None, None, None],
                    ["Delete Meeting", None, None, None],
                    ],
                ],
                ])
        except Exception as e:
            logger.error("Failed to render menu bar, exiting...", exc_info=True)
            messagebox.showerror("Error", "An exception has occured.\nError Details:\n%s" % (str(e)))
            exit(1)
        else:
            logger.info("Rendered menu bar")

        # Configure menu to be used by the application.
        root_element.config(menu=self)

    def make_list_to_menu(self, main_menu):
        """Makes a list to a usuable menu."""
        for menu_item in main_menu:
            menu = tk.Menu(self, tearoff = "off") # Init menu
            for submenu_item in menu_item[1]:
                # Create subitem
                skey = submenu_item[2][1:-1] if submenu_item[2] != None else None
                menu.add_command(label=submenu_item[0], command=submenu_item[1], accelerator=skey)
                # Shortcut key
                if submenu_item[2] != None:
                    self.root_element.bind_all(submenu_item[2], submenu_item[3])

            # Add menu to app
            self.add_cascade(label=menu_item[0], menu=menu)

    

    def launch_add_meeting_dialog(self):
        """Launch 'ADD MEETING' dialog"""
        # root = tk.Tk()
        # app = 
        NewMeetingDialog(tk_root_element = self.root_element)
        # root.mainloop()
        
        
        
class MeetingListFrame(tk.Frame):
    __components = []        # TK/TTK widgets
    __current_table_row = 1  # Current row of the table
    def __init__(self, root_element, tk_theme_object = None):
        """This class creates the frame that displays the list of meetings."""
        super().__init__(root_element)

        # DB handle
        self.__dbh = DatabaseHandler(DB_URL)

        self.root_element = root_element

        # If the theme object is not provided, make one, else use the one given
        if tk_theme_object == None:
            self.tk_theme = TkinterTheme(THEME_FILE)
        else:
            self.tk_theme = tk_theme_object

        # Sticky grid that resizes according to window size.
        # tk.Grid.rowconfigure(root_element, row, weight=1)
        # tk.Grid.columnconfigure(root_element, column, weight=1)

        # Grid
        # self.grid(row=row, column=column, sticky=N+S+E+W)

        # Widgets
        # for i in range(0, 10):
        #     for j in range(0, 10):
        #         self.create_ttk_button("Row:%d Column:%d" % (i, j), i, j)
        self.create_column_headers(["Meeting Start Time", "Meeting ID", "Meeting Password", "Join Meeting", "Edit/Delete Meeting"])

        # Populate table
        self.populate_table_from_db()
        
    def __stickify(self, row = 0, column = 0):
        """Auto resize the TK widget acc. to window size"""
        # Should only stick vertically.
        # tk.Grid.rowconfigure(self, row, weight=1)
        tk.Grid.columnconfigure(self, column, weight=1)

    def create_ttk_button(self, text, row = 0, column = 0, command = None, sticky=N+S+E+W, stickify=True):
        """Creates a TTK Button and adds resizing capability."""
        # Auto resize
        if stickify: self.__stickify(row, column)

        # Create component
        btn = ttk.Button(self, text=text, command=command)
        btn.grid(row=row, column=column, sticky=sticky)

        # Append to component list and return index
        self.__components.append(btn)
        return len(self.__components) - 1

    def create_tk_label(self, text, row = 0, column = 0, sticky=N+S+E+W, stickify=True, *args, **kwargs):
        """Creates a TK Label and adds resizing capability."""
        # Auto resize
        if stickify: self.__stickify(row, column)

        # Create component
        lbl = tk.Label(self, text=text, *args, **kwargs)
        lbl.grid(row=row, column=column, sticky=sticky)

        # Append to component list and return index
        self.__components.append(lbl)
        return len(self.__components) - 1

    # Table populating functions:
    def create_column_headers(self, col_headers):
        """Creates the column headers."""
        col_no = 0
        for col_header in col_headers:
            theme_dict = self.tk_theme.get_styling("table_header")
            self.create_tk_label(col_header, column = col_no, **theme_dict)
            col_no += 1

        return col_no
    
    def create_table_row(self, record_id, meeting_time, meeting_id, meeting_password):
        """Creates a row for the table."""
        row_no = self.__current_table_row
        styling = self.tk_theme.get_styling("table_content")
        self.create_tk_label(meeting_time.strftime("%a %d %B %Y %I:%M:%S %p"), row=row_no, column=0, **styling)
        self.create_tk_label(meeting_id, row=row_no, column=1, **styling)
        self.create_tk_label(meeting_password, row=row_no, column=2, **styling)
        self.create_ttk_button("Join meeting", row=row_no, column=3)
        self.create_ttk_button("Edit/Delete meeting", row=row_no, column=4, command=lambda: EditMeetingDialog(record_id, tk_root_element = self.root_element))
        self.__current_table_row += 1

    # Controller/View Interface
    def populate_table_from_db(self):
        """Populate the table from the Database."""
        try:
            # logger.info("Attempting to load meeting data from DB...")
            meetings = self.__dbh.get_mtg_data_to_list()
            for mtg in meetings:
                self.create_table_row(mtg["id"], mtg["mtg_time"], mtg["mtg_id"], mtg["mtg_password"])
        except Exception as e:
            logger.error("Failed to load meeting data, exiting...", exc_info=True)
            messagebox.showerror("Error", "An exception has occured.\nError Details:\n%s" % (str(e)))
            exit(1)
        else:
            logger.info("Loaded meeting data successfully.")

    def reload_table(self):
        for cell in self.winfo_children():
            cell.destroy()
        self.create_column_headers(["Meeting Start Time", "Meeting ID", "Meeting Password", "Join Meeting", "Edit/Delete Meeting"])

        # Populate table
        self.populate_table_from_db()

class ApplicationStatusBar(tk.Label):
    """Status bar"""
    def __init__(self, root_element):
        super().__init__(root_element, text="Loading…", bd=1, relief=tk.SUNKEN, anchor=W)

        # Autojoiner
        self.__autojoiner_handle = Autojoiner(PYAG_PICS_DIR)

        self.iterator()

    def check_for_meeting(self):
        """Repeatedly check for meetings"""
        if self.__autojoiner_handle.check_for_meeting():
            logger.info("Status Bar - Meeting now.")
            self["text"] = "There is a meeting now. Zoom Autojoiner is initiating the joining process."
            (mtg_id, mtg_pw) = (self.__autojoiner_handle.check_for_meeting()["mtg_id"], self.__autojoiner_handle.check_for_meeting()["mtg_password"])
            self["text"] = "There is a meeting now. Zoom Autojoiner has initiated the joining process."
            logger.info("Status Bar - Joining Meeting")
            self.__autojoiner_handle.join_zm_mtg(mtg_id, mtg_pw)
            self["text"] = "Zoom Autojoiner has finished the joining process. There will be a pause for 60 seconds now."
            logger.info("Status Bar - Sleeping")
            time.sleep(60)

    def iterator(self):
        logger.info("Status Bar - Iterating")
        self["text"] = "Checking for meeting"
        self.check_for_meeting()
        self["text"] = "Running"
        self.after(10000, self.iterator)


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TK Styling object
        self.__tk_theme = TkinterTheme(THEME_FILE)

        # Window Titles
        self.title('Zoom Autojoiner')
        try:
            self.iconbitmap(ICON_FILE)
        except:
            logger.warning("Could not load Window icon", exc_info=True)

        # Menu Bar
        self.menu_bar = ApplicationMenuBar(self)

        # Title
        self.create_tk_label("Zoom AutoJoiner - My Meeting List", sticky=N+E+W, stickify=False, **self.__tk_theme.get_styling("title"))
        
        # Window Elements
        # Meetings List
        self.meeting_list_frame = MeetingListFrame(self, self.__tk_theme)
        # Elasticity
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        # Positioning
        self.meeting_list_frame.grid(row=1, column=0, sticky=N+S+E+W)

        self.statusbar = ApplicationStatusBar(self)
        # Elasticity
        # tk.Grid.rowconfigure(self, 2, weight=1)
        # tk.Grid.columnconfigure(self, 0, weight=1)
        # Positioning
        self.statusbar.grid(row=2, column=0, sticky=N+S+E+W)

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
# -[] After theming class, make GUI
# -[] After PyAG autojoin, add 1s refresher to a label
        
