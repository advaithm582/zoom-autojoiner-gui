import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import datetime
import platform
from zoom_autojoiner_gui.controllers import DatabaseHandler
from zoom_autojoiner_gui.constants import DB_URL

class NewMeetingDialog(tk.Toplevel):
    def __init__(self, tk_frame_handle = None, tk_root_element = None):
        """This class shows the New Meeting Dialog box."""
        # DB handle
        self.__dbh = DatabaseHandler(DB_URL)

        # TK Root Element
        if tk_root_element:
            # Attach it to var
            self.tk_root_element = tk_root_element
        else:
            # Get Root element from frame
            self.tk_root_element = None

        # Toplevel Initialization
        try:
            # print("HI")
            super().__init__(self.tk_root_element)
        except:
            super().__init__()

        # TK Frame
        if tk_frame_handle:
            # If given use it
            self.tk_frame_handle = tk_frame_handle
        elif self.tk_root_element:
            # Take from root element
            self.tk_frame_handle = self.tk_root_element.meeting_list_frame
        else:
            # None it
            self.tk_frame_handle = None

        #setting title
        self.title("New Meeting")
        #setting window size
        width=338
        height=200
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        # For modal dialog
        self.grab_set()
        try:
            # if platform.system() == "Windows": self.attributes('-toolwindow', True)
            self.transient(self.tk_root_element)
            # self.attributes('-topmost', True)
        except:
            pass

        # Meeting Time Label
        self.GLabel_3=ttk.Label(self)
        self.GLabel_3["text"] = "Mtg. Time"
        self.GLabel_3.place(x=0,y=40,width=101,height=30)

        # Title Label
        self.GLabel_276=ttk.Label(self)
        self.GLabel_276["justify"] = "center"
        self.GLabel_276["text"] = "New Meeting"
        self.GLabel_276.place(x=0,y=0,width=350,height=30)

        # Meeting Time Entry
        self.DateTimeEntry=ttk.Entry(self)
        self.DateTimeEntry.place(x=110,y=40,width=220,height=30)

        # Meeting ID label
        self.GLabel_378=ttk.Label(self)
        # ft = tkFont.Font(family='Times',size=10)
        self.GLabel_378["text"] = "Meeting ID"
        self.GLabel_378.place(x=0,y=80,width=100,height=30)

        # Meeting ID entry
        self.MeetingIDEntry=ttk.Entry(self)
        self.MeetingIDEntry.place(x=110,y=80,width=220,height=30)

        # Meeting Passcode Label
        self.GLabel_48=ttk.Label(self)
        self.GLabel_48["text"] = "Passcode"
        self.GLabel_48.place(x=0,y=120,width=101,height=30)

        # Meeting Password Entry
        self.MeetingPasscodeEntry=ttk.Entry(self)
        self.MeetingPasscodeEntry.place(x=110,y=120,width=220,height=30)

        # Create Meeting Button
        self.CreateMtgButton=ttk.Button(self)
        # CreateMtgButton["bg"] = "#f0f0f0"
        # ft = tkFont.Font(family='Times',size=10)
        # CreateMtgButton["font"] = ft
        # CreateMtgButton["fg"] = "#000000"
        # CreateMtgButton["justify"] = "center"
        self.CreateMtgButton["text"] = "Create"
        self.CreateMtgButton.place(x=260,y=160,width=70,height=35)
        self.CreateMtgButton["command"] = self.CreateMtgButton_command

        # Cancel New Meeting Button
        self.CancelButton=ttk.Button(self)
        # CancelButton["bg"] = "#f0f0f0"
        # ft = tkFont.Font(family='Times',size=10)
        # CancelButton["font"] = ft
        # CancelButton["fg"] = "#000000"
        # CancelButton["justify"] = "center"
        self.CancelButton["text"] = "Cancel"
        self.CancelButton.place(x=170,y=160,width=70,height=35)
        self.CancelButton["command"] = self.CancelButton_command

    def CreateMtgButton_command(self):
        try:
            datetimeobj=datetime.datetime.strptime(self.DateTimeEntry.get(), "%Y-%m-%d %H:%M:%S")
            self.__dbh.add_mtg(self.MeetingIDEntry.get(), self.MeetingPasscodeEntry.get(), datetimeobj)
        except Exception as e:
            messagebox.showerror("Error", "An exception has occured.\nError Details:\n%s" % (str(e)))
        else:
            messagebox.showinfo("Information", "Meeting Added.")
            try:
                self.tk_frame_handle.reload_table()
            except:
                messagebox.showinfo("Information", "Failed to refresh table data. Please refresh manually.")
            self.destroy()
            

    def CancelButton_command(self):
        self.destroy()

class EditMeetingDialog(tk.Toplevel):
    def __init__(self, record_id, tk_frame_handle = None, tk_root_element = None):
        # DB handle
        self.__dbh = DatabaseHandler(DB_URL)

        # TK Root Element
        if tk_root_element:
            # Attach it to var
            self.tk_root_element = tk_root_element
        else:
            # Get Root element from frame
            self.tk_root_element = None

        # Toplevel Initialization
        try:
            # print("HI")
            super().__init__(self.tk_root_element)
        except:
            super().__init__()

        self.record_id = record_id

        # TK Frame
        if tk_frame_handle:
            # If given use it
            self.tk_frame_handle = tk_frame_handle
        elif self.tk_root_element:
            # Take from root element
            self.tk_frame_handle = self.tk_root_element.meeting_list_frame
        else:
            # None it
            self.tk_frame_handle = None

        # Get values from DB
        try:
            mtg_data = self.__dbh.get_single_mtg_data_to_list(self.record_id)
        except Exception as e:
            messagebox.showerror("Error", "An exception has occured.\nError Details:\n%s" % (str(e)))
            self.destroy()

        #setting title
        self.title("Edit Meeting")
        
        #setting window size
        width=338
        height=200
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        # For modal dialog
        self.grab_set()
        try:
            # if platform.system() == "Windows": self.attributes('-toolwindow', True)
            self.transient(self.tk_root_element)
            # self.attributes('-topmost', True)
        except:
            pass

        # Title Label
        self.GLabel_276=ttk.Label(self)
        self.GLabel_276["justify"] = "center"
        self.GLabel_276["text"] = "Edit Meeting (Record ID %d)" % (self.record_id)
        self.GLabel_276.place(x=0,y=0,width=350,height=30)
        
        # Meeting Time Label
        self.GLabel_3=ttk.Label(self)
        self.GLabel_3["text"] = "Mtg. Time"
        self.GLabel_3.place(x=0,y=40,width=101,height=30)

        # Meeting Time Entry
        self.DateTimeEntry=ttk.Entry(self)
        self.DateTimeEntry.insert(0, mtg_data["mtg_time"])
        self.DateTimeEntry.place(x=110,y=40,width=220,height=30)

        # Meeting ID label
        self.GLabel_378=ttk.Label(self)
        self.GLabel_378["text"] = "Meeting ID"
        self.GLabel_378.place(x=0,y=80,width=100,height=30)

        # Meeting ID entry
        self.MeetingIDEntry=ttk.Entry(self)
        self.MeetingIDEntry.insert(0, mtg_data["mtg_id"])
        self.MeetingIDEntry.place(x=110,y=80,width=220,height=30)

        # Meeting Passcode Label
        self.GLabel_48=ttk.Label(self)
        self.GLabel_48["text"] = "Passcode"
        self.GLabel_48.place(x=0,y=120,width=101,height=30)

        # Meeting Password Entry
        self.MeetingPasscodeEntry=ttk.Entry(self)
        self.MeetingPasscodeEntry.insert(0, mtg_data["mtg_password"])
        self.MeetingPasscodeEntry.place(x=110,y=120,width=220,height=30)

        # Update Meeting Button
        self.UpdateMtgButton=ttk.Button(self)
        # UpdateMtgButton["bg"] = "#f0f0f0"
        # ft = tkFont.Font(family='Times',size=10)
        # UpdateMtgButton["font"] = ft
        # UpdateMtgButton["fg"] = "#000000"
        # UpdateMtgButton["justify"] = "center"
        self.UpdateMtgButton["text"] = "Update"
        self.UpdateMtgButton.place(x=260,y=160,width=70,height=35)
        self.UpdateMtgButton["command"] = self.UpdateMtgButton_command

        # Delete New Meeting Button
        self.DeleteMtgButton=ttk.Button(self)
        # CancelButton["bg"] = "#f0f0f0"
        # ft = tkFont.Font(family='Times',size=10)
        # CancelButton["font"] = ft
        # CancelButton["fg"] = "#000000"
        # CancelButton["justify"] = "center"
        self.DeleteMtgButton["text"] = "Delete"
        self.DeleteMtgButton.place(x=170,y=160,width=70,height=35)
        self.DeleteMtgButton["command"] = self.DeleteMtgButton_command

        # Cancel New Meeting Button
        self.CancelButton=ttk.Button(self)
        self.CancelButton["text"] = "Cancel"
        self.CancelButton.place(x=80,y=160,width=70,height=35)
        self.CancelButton["command"] = self.CancelButton_command

    def UpdateMtgButton_command(self):
        """Update meeting data."""
        try:
            datetimeobj=datetime.datetime.strptime(self.DateTimeEntry.get(), "%Y-%m-%d %H:%M:%S")
            self.__dbh.update_mtg(self.record_id, self.MeetingIDEntry.get(), self.MeetingPasscodeEntry.get(), datetimeobj)
        except Exception as e:
            messagebox.showerror("Error", "An exception has occured.\nError Details:\n%s" % (str(e)))
        else:
            messagebox.showinfo("Information", "Meeting Updated.")
            try:
                self.tk_frame_handle.reload_table()
            except:
                messagebox.showinfo("Information", "Failed to refresh table data. Please refresh manually.")
            self.destroy()
            

    def CancelButton_command(self):
        """Close the Window"""
        self.destroy()

    def DeleteMtgButton_command(self):
        """Delete meeting"""
        result = messagebox.askquestion("Warning", "Deleted meetings are DELETED FOREVER.\nThis action is IRREVERSIBLE!!. \nProceed?")
        if result == "yes":
            try:
                self.__dbh.delete_mtg(self.record_id)
            except Exception as e:
                messagebox.showerror("Error", "An exception has occured.\nError Details:\n%s" % (str(e)))
            else:
                messagebox.showinfo("Information", "Meeting Deleted.")
                try:
                    self.tk_frame_handle.reload_table()
                except:
                    messagebox.showinfo("Information", "Failed to refresh table data. Please refresh manually.")
                self.destroy()
                
    


if __name__ == "__main__":
    app = NewMeetingDialog()
