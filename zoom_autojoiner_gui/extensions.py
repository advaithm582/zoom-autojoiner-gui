import logging
import sys
import os
import json
import tkinter as tk
from importlib import import_module
from configparser import ConfigParser

# from zoom_autojoiner_gui.views import (
#     MainWindow,
#     ApplicationMenuBar,
#     MeetingListFrame
# )
from zoom_autojoiner_gui.constants import EXTENSIONS


logger = logging.getLogger(__name__) # This creates logger for this file.


#: bool : Whether extension API is enabled or not.
enabled = EXTENSIONS.getboolean("enabled")


class ExtensionHandler():
    """ExtensionHandler

    This class deals with the handling of ZAJ
    Python Extensions. 

    Args:
        config: The Extensions Config dict.

    Returns:
        NoneType
    """
    
    #: tuple : The tuple of permissions.
    permissions = (
        "main_window",
        "menu_bar",
        "meeting_list_frame"
    )

    def __init__(self, config: ConfigParser) -> None:
        self.basic_config = config
        self.config = ConfigParser()

        real_path = os.path.realpath(__file__)
        dir_path = os.path.dirname(real_path)

        # Extension configuration
        self.config.read(os.path.join(dir_path, "config", 
            self.basic_config['config'] + '.ini'))

        # Extension DIR
        
        self.extensions_dir = os.path.join(dir_path, self.basic_config['dir'])

        self.extensions = {}

        logger.debug(os.path.join(dir_path, "config", 
            self.basic_config['config'] + '.ini'))

    def get_ext(self) -> list:
        """get_ext

        Gets the enabled extensions from
        the extension configuration file.

        Returns:
            The list of enabled extensions.
        """
        return json.loads(self.config['enabled']['extensions'])

    def get_extension_permission(self, ext_name: str, 
            permission_name: str) -> bool:
        """get_extension_permissions

        Get the permission for an extension.

        Args:
            ext_name: The name of an extension.
            permission_name: The name of a permission to check.

        Returns:
            A boolean value. 
            If the permission is granted, it returns True. Or else it 
            returns False.
        """
        return self.config.getboolean(ext_name, permission_name, 
            fallback=False)

    def load_extensions(self) -> bool:
        """load_extensions

        Load all the extensions.

        Returns:
            True if everything went fine
            False if even one extension failed

        Note:
            If one extension failed, others are still executed.
            Like a parallel circuit, if one bulb fuses others don't.
        """
        all_ext_ran = True

        sys.path.insert(0, self.extensions_dir)

        for extension in self.get_ext():
            try:
                self.extensions[extension] = import_module(extension)
            except:
                logger.error(f"Failed to load extension {extension}!",
                    exc_info=True)
                all_ext_ran = False

        return all_ext_ran

    def give_extensions_prefs(self) -> bool:
        """give_extensions_prefs

        Give extensions their preferences. This is stored in the same 
        section where their permissions are stored. The preferences are
        passed to a function in the extension, `get_prefs` where they
        are given the ConfigParser Object of their section in an argument
        `prefs_dict`.

        Returns:
            True if everything went fine
            False if even one extension failed

        Note:
            An extension should have implemented the module level function
            `get_prefs` in order for this to work.
            If one extension failed, others are still executed.
            Like a parallel circuit, if one bulb fuses others don't.
        """
        all_ext_ran = True

        for extension in self.get_ext():
            try:
                self.extensions[extension].get_prefs(prefs_dict=self.config[extension])
            except:
                logger.error(f"Failed to give obj to ext {extension}!",
                    exc_info=True)
                all_ext_ran = False

        return all_ext_ran

    def give_extensions_objects(self, main_window: tk.Tk = None, 
            menu_bar: tk.Menu = None, 
            meeting_list_frame: tk.Frame = None) -> bool:
        """give_extensions_objects

        Give extensions the currently used Tkinter objects. It also depends
        on the permissions granted to the extensions. For example, if an 
        extension was not given meeting_list_frame permission, then a None
        object will be passed to it instead.

        Args:
            main_window: The Main window of the ZAJ.
            menu_bar: Application menu Bar
            meeting_list_frame: Meeting lsit frame object.

        Returns:
            True if everything went fine
            False if even one extension failed

        Note:
            An extension should have implemented the module level function
            `set_objects` in order for this to work.
            If one extension failed, others are still executed.
            Like a parallel circuit, if one bulb fuses others don't.
        """

        # Whether all extensions ran successfully
        all_ext_ran = True

        for extension in self.extensions:
            try:
                objects = {}
                for permission in self.permissions:
                    if self.get_extension_permission(extension, permission):
                        objects[permission] = locals()[permission]
                        # logger.debug(f"{objects}, {locals()}")
                    else:
                        objects[permission] = None
                self.extensions[extension].set_objects(
                        objects["main_window"],
                        objects["menu_bar"],
                        objects["meeting_list_frame"]
                    )
                logger.debug(f"EXT_NAME{extension}\nOBJECTS:{objects}")
            except:
                logger.error(f"Failed to set extension {extension}!", 
                    exc_info=True)
                all_ext_ran = False

        return all_ext_ran

    def run_extensions(self) -> bool:
        """run_extensions

        Run all the extensions.

        Returns:
            True if everything went fine
            False if even one extension failed

        Note:
            If one extension failed, others are still executed.
            Like a parallel circuit, if one bulb fuses others don't.
        """

        all_ext_ran = True

        for extension in self.extensions:
            try:
                self.extensions[extension].main()
            except:
                logger.error(f"Failed to run extension {extension}!", 
                    exc_info=True)
                all_ext_ran = False

        return all_ext_ran


def load_extensions():
    if EXTENSIONS.getboolean("enabled"):
        # if extensions are enabled
        global ext_class
        ext_class = ExtensionHandler(EXTENSIONS)
        if ext_class.load_extensions():
            ext_class.run_extensions()