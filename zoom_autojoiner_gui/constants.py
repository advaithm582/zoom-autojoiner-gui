import json, logging, configparser

logger = logging.getLogger(__name__)
try:
    logger.info("Attempting to load config...")
    # with open("config/config.json", "r") as cfg_file:
    #     cfg = json.loads(cfg_file.read())
    #     ICON_FILE = cfg["ICON_FILE"]
    #     DB_URL = cfg["DB_URL"]
    #     PYAG_PICS_DIR = cfg["PYAG_PICS_DIR"]
    #     MY_NAME = cfg["MY_NAME"]
    #     THEME_FILE = "themes/" + cfg["THEME_FILE"]

    # Parse the config file.
    config = configparser.ConfigParser()
    

    # read it
    config.read("config/application.ini")
    # Tkinter configuration
    ICON_FILE = config["tkinter"]["icon"]
    THEME_FILE = "themes/" + config["tkinter"]["theme"] + ".thm.json"

    # Database configuration
    DB_URL = config["database"]["uri"]

    # Autojoiner configuration
    PYAG_PICS_DIR = config["autojoiner"]["pictures_dir"]
    MY_NAME = config["autojoiner"]["name"]

    """The Extensions Config Variable"""
    EXTENSIONS = config["extensions"]
    
except Exception as e:
    logger.error("Failed to load config, exiting...", exc_info=True)
    exit(1)
else:
    logger.info("Config loaded.")

# from datetime import datetime

# # Theme
# COLOR_SCHEME = {
#     "title" : {
#         "fg" : "black",
#         "bg" : None,
#         "font" : {
#             "name" : "Calibri",
#             "size" : "20",
#             "style" : "bold"
#         },
#         "padding" : {
#             "x" : "5",
#             "y" : "5"
#         },
#         "border" : {
#             "width" : None,
#             "relief" : None
#         }
#     },
#     "header" : {
#         "fg" : "white",
#         "bg" : "#142E54",
#         "font" : {
#             "name" : "Calibri",
#             "size" : "12",
#             "style" : "bold"
#         },
#         "padding" : {
#             "x" : "5",
#             "y" : "5"
#         },
#         "border" : {
#             "width" : 2,
#             "relief" : "groove"
#         }
#     },
#     "content" : {
#         "fg" : "black",
#         "bg" : "white",
#         "font" : {
#             "name" : "Calibri",
#             "size" : "12",
#             "style" : ""
#         },
#         "padding" : {
#             "x" : "5",
#             "y" : "5"
#         },
#         "border" : {
#             "width" : 2,
#             "relief" : "groove"
#         }
#     },
#     "button" : {
#         "fg" : "black",
#         "bg" : "#cccccc",
#         "font" : {
#             "name" : "Serif",
#             "size" : "10",
#             "style" : ""
#         },
#         "padding" : {
#             "x" : "5",
#             "y" : "5"
#         },
#         "border" : {
#             "width" : 1,
#             "relief" : "solid"
#         }
#     },
#     "entry" : {
#         "fg" : "black",
#         "bg" : "white",
#         "font" : {
#             "name" : "Serif",
#             "size" : "10",
#             "style" : ""
#         },
#         "border" : {
#             "width" : 1,
#             "relief" : "solid"
#         }
#     }
# }
# logging.basicConfig(filename='logs/%s.log' % (datetime.now().strftime("%Y%m%d-%H%M%S")), filemode='w', format='[%(asctime)s] [%(name)s:%(levelname)s] [pid:%(process)d, tid:%(thread)d] %(message)s', datefmt='%c', level=logging.INFO)
