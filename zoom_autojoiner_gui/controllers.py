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

import json
import time
import platform
import logging
from datetime import datetime
from typing import Any, Union

import pyautogui
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query

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
    DEFAULT_THEME: str = """
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
        except:
            logger.warning("Failed to load theme file, using default...", 
                exc_info=True)
            self.json = json.loads(self.DEFAULT_THEME)
        else:
            logger.info("Loaded theme file")

    def get_styling(self, style_name: str) -> dict:
        """get_styling 
        
        Gets the style to be used for given style name.

        Args:
            style_name: The name of the style.

        Returns:
            dict: The dict of TK styling to be unpacked and passed.
        """
        if style_name in self.json:
            the_dict = {
                    "fg" : self.json[style_name]["fg"],
                    "bg" : self.json[style_name]["bg"],
                    "padx" : self.json[style_name]["padding"]["x"],
                    "pady" : self.json[style_name]["padding"]["y"],
                    "borderwidth" : self.json[style_name]["border"]["width"],
                    "relief" : self.json[style_name]["border"]["relief"],
                    "font" : (self.json[style_name]["font"]["name"] 
                        + " " 
                        + self.json["table_header"]["font"]["size"] 
                        + " " 
                        + self.json["table_header"]["font"]["style"])
                }
            return the_dict
        else:
            # no style available
            return {}


class DatabaseHandler():
    """DatabaseHandler
    
    This class handles database related stuff. It's like a waiter in a
    restaurant - it handles communications between the customer (view)
    and the cook (database). In technical terms, it is a controller in
    the MVC architecture.

    Args:
        database_uri:
            The URI of the database, in SQLAlchemy format.
    """
    def __init__(self, database_uri: str) -> None:
        # engine = create_engine(DB_URL)
        engine = create_engine(database_uri)
        Session = sessionmaker(bind=engine)
        self.__db_session = Session()

    def add_mtg(self, meeting_id: str, meeting_password: str, 
            meeting_time: datetime, meeting_provider: str = "ZM",
            auto_commit: bool = True) -> None:
        """add_mtg 
        
        Adds a meeting to the database.

        Args:
            meeting_id: The Meeting ID
            meeting_password: Mtg. passcode
            meeting_time: Datetime of meeting
            meeting_provider: Meeting Provider. Defaults to "ZM".
            auto_commit: Whether to autosave changes. Defaults to True.
        """
        mtg = Meetings(mtg_provider=meeting_provider, mtg_id=meeting_id, 
            mtg_password=meeting_password, mtg_time=meeting_time)
        self.__db_session.add(mtg)
        if auto_commit:
            self.commit_changes()

    def delete_mtg(self, rec_id: int, auto_commit: bool = True) -> None:
        """delete_mtg 
        
        Deletes a meeting from the database.

        Args:
            rec_id: The Record ID in database
            auto_commit:
                Whether to auto commit changes. Defaults to True.
        """
        to_delete = self.__db_session.query(Meetings).filter_by(id=
            rec_id).one()
        self.__db_session.delete(to_delete)
        if auto_commit:
            self.commit_changes()

    def update_mtg(self, db_id: int, meeting_id: str, meeting_password: str,
            meeting_time: datetime, meeting_provider: str = "ZM",
            auto_commit: bool = True) -> None:
        """update_mtg 
        
        Update meeting data in the database.

        Args:
            db_id (int): The Record ID in database.
            meeting_id (str): The Meeting ID.
            meeting_password (str): The Meeting password.
            meeting_time (datetime.datetime): The time of the meeting.
            meeting_provider (str, optional):
                Meeting provider code. Defaults to "ZM".
            auto_commit (bool, optional):
                Whether to autosave changes. Defaults to True.
        """
        to_update = self.__db_session.query(Meetings).filter_by(id=
            db_id).one()
        to_update.mtg_provider = meeting_provider
        to_update.mtg_id = meeting_id
        to_update.mtg_password = meeting_password
        to_update.mtg_time = meeting_time
        if auto_commit:
            self.commit_changes()

    def get_mtg_data_to_list(self) -> list[dict[str, Any]]:
        """get_mtg_data_to_list 
        
        Queries meeting data from SQL database and outputs it as a
        list cum dict

        Returns:
            list: List with dict of mtg data.
        """
        output_list = [] # Output list
        query = self.__db_session.query(Meetings).order_by(
            Meetings.mtg_time)
        for record in query:
            mtg_data = {
                "id" : record.id,
                "mtg_provider" : record.mtg_provider, 
                "mtg_id" : record.mtg_id, 
                "mtg_password" : record.mtg_password,
                "mtg_time": record.mtg_time 
            }
            # print(type(record.mtg_time))
            output_list.append(mtg_data)
        return output_list

    def get_single_mtg_data_to_list(self, record_id: str) -> dict[str, Any]:
        """get_single_mtg_data_to_list

        Queries only one meeting from SQL database and outputs it as a
        dict

        Note:
            The method name is redundant, as it was imported from 
            `cryptocurrency-portfolio`_. It will be changed before the 
            release of the 1.x.x series. To ensure backwards
            compatibility, this method will be made to call the dict
            method.

        Args:
            record_id (str): ID of record in database.

        Returns:
            dict[str, Any]: Dict containing meeting data of record ID.

        .. _cryptocurrency-portfolio: https://tinyurl.com/48a7y5cw
        """
        # output_list = [] # Output list
        record = self.__db_session.query(Meetings).filter_by(id=record_id) \
            .one()
        output_list = {
            "id" : record.id,
            "mtg_provider" : record.mtg_provider, # mtg_provider
            "mtg_id" : record.mtg_id, # No. of mtg owned
            "mtg_password" : record.mtg_password,
            "mtg_time": record.mtg_time # Price per mtg at time of purchase
        }
        # output_list.append(mtg_data)
        return output_list
    
    def get_mtg_with_time(self, time: datetime) -> list[Query]:
        """get_mtg_with_time 

        Get the meeting data, using time as a filter.
        Used for checking if it is time to join the meeting.

        Note:
            This API is not used and is kept for the future. The reason 
            is that this heavily depends on the seconds parameter, and
            if the autojoiner checks for meetings every second, it will
            consume too many resources.

            If you have a solution to this problem, please fork the 
            repo and feel free to open a PR.

        Args:
            time: The time filter.

        Returns:
            list[Query]:
                It is a normal SQLAlchemy object which has a list, and
                in each an object.
        """
        query = self.__db_session.query(Meetings).filter(Meetings.mtg_time \
            == time).order_by(Meetings.mtg_time)
        # logger.debug(type(query))
        return query

    def truncate_table(self, auto_commit: bool = True) -> None:
        """truncate_table 
        
        Clear all data in the table.
        This API is yet to be implemented. As always, this method was 
        taken from `cryptocurrency-portfolio`_.

        Args:
            auto_commit:
                Whether to autosave changes. Defaults to True.

        .. _cryptocurrency-portfolio: https://tinyurl.com/48a7y5cw
        """
        # Remove all meetings
        self.__db_session.query(Meetings).delete()
        if auto_commit:
            self.commit_changes()


    def commit_changes(self) -> None:
        """Make changes reflect in database"""
        self.__db_session.commit()


class ATLParser():
    """
    AuTomation Language (ATL) parser

    This class parses ATL code, wj=hick ends in the file extension
    .atl. These are simple JSON files. For the format, see 
    specification.atl in the 'scripts' folder.

    ATL code will be used internally by Zoom Autojoiner to enable 
    joining of meetings on different platforms (OSes).

    Note:
        The ATL parser will be implemented as an extension and not in
        the ZAJ core. Infact, this idea may be DROPPED itself, as it
        can impact performance.
    """
    pass


class Autojoiner():
    """
    Autojoiner

    This class contains functions that will help in automatically
    joining Zoom meetings.

    Note:
        This class may be moved to an extension in the next major
        release.

    Args:
        image_dir: The directory where images are stored.
    """
    def __init__(self, image_dir: str = "") -> None:
        self.__dbh = DatabaseHandler(DB_URL) # dbh is DB handle
        self.IMG_DIR = image_dir # e.g /usr/share/

    def get_image_path(self, filename: str) -> str:
        """get_image_path 

        Get the path to the image with correct slash for the OS.

        Note:
            It will be more efficient if os.path.join is used instead.

        Args:
            filename (str): The name of the file.

        Returns:
            str: The full directory path.
        """
        # Get the path of the image from the filename.
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

    def check_for_meeting(self) -> Union[dict, bool]:
        """check_for_meeting 
        
        Checks if there is a meeting at the current time.

        Returns:
            Optional[dict, bool]: 
                Returns list of meetings, if a meeting is present at
                that time.
        """
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

    def join_zm_mtg(self, id: str, password: str) -> None:
        """join_zm_mtg

        Joins a zoom meeting

        Args:
            id (str): Meeting ID
            password (str): Meeting Passcode
        """
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
