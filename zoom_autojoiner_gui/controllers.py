import json, time, pyautogui, platform, logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zoom_autojoiner_gui.models import Meetings
from zoom_autojoiner_gui.constants import DB_URL, MY_NAME

logger = logging.getLogger(__name__)

class TkinterTheme():
    """
    TkinterTheme Class

    This class deals with the styling of the GUI
    interface. Theme files end in the extension
    `.thm.json`. These sre simple JSON files. 
    An example is gilen in the constant
    DEFAULT_THEME.

    Incase the theme file fails to open (maybe 
    file not found?), the class defaults to the
    DEFAULT_THEME str (or docstring to be more 
    specific.)

    There are a few bugs in this class, which
    occur when there is a space in the font name.
    I am not sure how to fix the same, hence 
    leaving as is.
    """
    DEFAULT_THEME:str = """
            {
                "title" : {
                    "fg" : "white",
                    "bg" : "gray",
                    "font" : {
                        "name" : "Lato",
                        "size" : "20",
                        "style" : "bold"
                    },
                    "padding" : {
                        "x" : "5",
                        "y" : "5"
                    },
                    "border" : {
                        "width" : null,
                        "relief" : null
                    },
                    "sticky" : "EW"
                },
                "table_header" : {
                    "fg" : "white",
                    "bg" : "#142E54",
                    "font" : {
                        "name" : "Lato",
                        "size" : "12",
                        "style" : "bold"
                    },
                    "padding" : {
                        "x" : "5",
                        "y" : "5"
                    },
                    "border" : {
                        "width" : 2,
                        "relief" : "groove"
                    },
                    "sticky" : "NSEW"
                },
                "table_content" : {
                    "fg" : "black",
                    "bg" : "white",
                    "font" : {
                        "name" : "Lato",
                        "size" : "8",
                        "style" : "bold"
                    },
                    "padding" : {
                        "x" : "5",
                        "y" : "5"
                    },
                    "border" : {
                        "width" : 2,
                        "relief" : "groove"
                    },
                    "sticky" : "NSEW"
                }
            }
            """
    def __init__(self, theme_file_uri:str) -> None:
        try:
            with open(theme_file_uri, "r") as file_handle:
                self.json = json.loads(file_handle.read())
        except Exception as e:
            logger.warning("Failed to load theme file, using default...", exc_info=True)
            self.json = json.loads(self.DEFAULT_THEME)
        else:
            logger.info("Loaded theme file")

    # def get_table_header_styling(self):
    #     """Gets the style to be used for the table header"""
    #     the_dict = {
    #             "fg" : self.json["table_header"]["fg"],
    #             "bg" : self.json["table_header"]["bg"],
    #             "padx" : self.json["table_header"]["padding"]["x"],
    #             "pady" : self.json["table_header"]["padding"]["y"],
    #             "borderwidth" : self.json["table_header"]["border"]["width"],
    #             "relief" : self.json["table_header"]["border"]["relief"],
    #             "font" : self.json["table_header"]["font"]["name"] + " " + self.json["table_header"]["font"]["size"] + " " + self.json["table_header"]["font"]["style"]
    #         }
    #     return the_dict

    def get_styling(self, style_name):
        """Gets the style to be used for the <style_name>"""
        if style_name in self.json:
            the_dict = {
                    "fg" : self.json[style_name]["fg"],
                    "bg" : self.json[style_name]["bg"],
                    "padx" : self.json[style_name]["padding"]["x"],
                    "pady" : self.json[style_name]["padding"]["y"],
                    "borderwidth" : self.json[style_name]["border"]["width"],
                    "relief" : self.json[style_name]["border"]["relief"],
                    "font" : self.json[style_name]["font"]["name"] + " " + self.json["table_header"]["font"]["size"] + " " + self.json["table_header"]["font"]["style"]
                }
            return the_dict
        else:
            # no style available
            return {}

class DatabaseHandler():
    def __init__(self, database_uri):
        # engine = create_engine(DB_URL)
        engine = create_engine(database_uri)
        Session = sessionmaker(bind=engine)
        self.__db_session = Session()

    def add_mtg(self, meeting_id, meeting_password, meeting_time, meeting_provider = "ZM", auto_commit = True):
        """Adds a mtg to the portfolio"""
        mtg = Meetings(mtg_provider=meeting_provider, mtg_id=meeting_id, mtg_password=meeting_password, mtg_time=meeting_time)
        self.__db_session.add(mtg)
        if auto_commit:
            self.commit_changes()

    def delete_mtg(self, rec_id, auto_commit = True):
        """Deletes a mtg from the portfolio"""
        to_delete = self.__db_session.query(Meetings).filter_by(id=rec_id).one()
        self.__db_session.delete(to_delete)
        if auto_commit:
            self.commit_changes()

    def update_mtg(self,db_id, meeting_id, meeting_password, meeting_time, meeting_provider = "ZM", auto_commit = True):
        """Updates the mtg data in the database"""
        to_update = self.__db_session.query(Meetings).filter_by(id=db_id).one()
        (to_update.mtg_provider, to_update.mtg_id, to_update.mtg_password, to_update.mtg_time) = (meeting_provider, meeting_id, meeting_password, meeting_time)
        if auto_commit:
            self.commit_changes()

    def get_mtg_data_to_list(self):
        """Queries meeting data from SQL database and outputs it as a list cum dict"""
        output_list = [] # Output list
        query = self.__db_session.query(Meetings).order_by(Meetings.mtg_time)
        for record in query:
            mtg_data = {
                "id" : record.id,
                "mtg_provider" : record.mtg_provider, # mtg_provider
                "mtg_id" : record.mtg_id, # No. of mtg owned
                "mtg_password" : record.mtg_password,
                "mtg_time": record.mtg_time # Price per mtg at time of purchase
            }
            # print(type(record.mtg_time))
            output_list.append(mtg_data)
        return output_list

    def get_single_mtg_data_to_list(self, record_id):
        """Queries only one meeting from SQL database and outputs it as a list cum dict"""
        # output_list = [] # Output list
        record = self.__db_session.query(Meetings).filter_by(id=record_id).one()
        output_list = {
            "id" : record.id,
            "mtg_provider" : record.mtg_provider, # mtg_provider
            "mtg_id" : record.mtg_id, # No. of mtg owned
            "mtg_password" : record.mtg_password,
            "mtg_time": record.mtg_time # Price per mtg at time of purchase
        }
        # output_list.append(mtg_data)
        return output_list
    
    def get_mtg_with_time(self, time):
        """Get the meeting data, using time as a filter.
        Used for checking if it is time to join the meeting"""
        query = self.__db_session.query(Meetings).filter(Meetings.mtg_time == time).order_by(Meetings.mtg_time)
        return query

    def truncate_table(self, auto_commit = True):
        """Remove all meetings"""
        self.__db_session.query(Meetings).delete()
        if auto_commit:
            self.commit_changes()


    def commit_changes(self):
        """Make changes reflect in database"""
        self.__db_session.commit()

class ATLParser():
    """
    AuTomation Language (ATL) parser

    This class parses ATL code, wj=hick ends in the file extension
    .atl. These are simple JSON files. For the format, see 
    specification.atl in the 'scripts' folder.

    ATL code is used internally by Zoom Autojoiner to enable joining
    of meetings on different platforms (OSes).
    """
    
class Autojoiner():
    """
    Zoom Autojoiner Class

    This class contains functions that will help in automatically joining meetings.
    """
    def __init__(self, image_dir = ""):
        self.__dbh = DatabaseHandler(DB_URL) # dbh is DB handle
        self.IMG_DIR = image_dir # e.g /usr/share/

    def get_image_path(self, filename):
        """Get the path of the image from the filename."""
        # Get the directory slash.
        # Why couldn't Windows be like the rest? :(
        OS_SLASH = "\\" if platform.system() == "Windows" else "/"

        # Get the directory/folder.
        if self.IMG_DIR[-1] == "\\" or self.IMG_DIR[-1] == "/":
            img_directory = self.IMG_DIR
        else:
            img_directory = self.IMG_DIR + OS_SLASH

        # Get Filename
        if filename[0] == "\\" or filename[0] == "/":
            final_filename = filename[1:]
        else:
            final_filename = filename

        # Return the file directory.
        return img_directory + final_filename

    def check_for_meeting(self):
        logger.debug("Check For Meeting Block entered")
        mtgs_list = self.__dbh.get_mtg_data_to_list()
        logger.debug(str(mtgs_list))
        now = datetime.now()
        now_string = now.strftime("%d-%m-%y %H:%M")
        logger.debug("Nowstring %s", now_string)
        return_str = ""
        return_dict = {}
        for mtg_dict in mtgs_list:
            mtg_date = mtg_dict["mtg_time"].strftime("%d-%m-%y %H:%M")
            logger.debug("Mtg date string %s", mtg_date)
            if mtg_date == now_string:
                logger.debug("True")
                return_str = True
                return_dict = mtg_dict
            else:
                logger.debug("False")
                return_str = False
        
        logger.debug("Return Dict %s", str(return_dict))
        return return_dict if return_str else False

    def join_zm_mtg(self, id, password):
        """join zm mtg"""
        try:
            # IMG_DIR = self.IMG_DIR
            # (start_x, start_y) = pyautogui.center(pyautogui.locateOnScreen(IMG_DIR + "start.png"))
            # print(start_x, start_y)
            pyautogui.click(self.get_image_path("zoom_taskbar.png"))
            time.sleep(0.75)
            pyautogui.click(self.get_image_path("join_btn.png"))
            time.sleep(0.75)
            pyautogui.write(id, interval=0.25)
            time.sleep(0.75)
            pyautogui.click(self.get_image_path("name_box.png"))
            time.sleep(0.25)
            pyautogui.hotkey('ctrl','a')
            time.sleep(0.25)
            pyautogui.press('backspace')
            time.sleep(0.25)
            pyautogui.write(MY_NAME, interval=0.25)
            time.sleep(0.75)
            pyautogui.click(self.get_image_path("join_btn_after_mtg_id.png"))
            time.sleep(5)
            pyautogui.write(password, interval=0.25)
            time.sleep(0.75)
            pyautogui.click(self.get_image_path("join_meeting_btn.png"))
        except:
            logger.error("Failed to join meeting", exc_info=True)
        else:
            logger.info("Joined Meeting successfully")

# Todo:
# Finish theming class
# After that finish Autojoiner class
