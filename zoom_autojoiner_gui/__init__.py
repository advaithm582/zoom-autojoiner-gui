import logging
from datetime import datetime
from multiprocessing import Process

# I am here because the ZAJ module has some logging work to do..
# Check that my level is set to logging.INFO
logging.basicConfig(filename='logs/%s.log' % (datetime.now().strftime("%Y%m%d-%H%M%S")), filemode='w', format='[%(asctime)s] [%(name)s:%(levelname)s] [pid:%(process)d, tid:%(thread)d] %(message)s', datefmt='%c', level=logging.INFO)

from zoom_autojoiner_gui.views import MainWindow

logger = logging.getLogger(__name__) # This creates logger for this file.

def load_window():
    """
    Load the Main Window

    Load the main Tk window. The reason this is here 
    is because a new process will be started to
    launch the Tk window.
    """
    try:
        # logger.info('Attempting to initialise Window')
        window = MainWindow() # Launch the Main Window.
    except:
        logger.error("Failed to initialise window, exiting...", exc_info=True)
        exit(1)
    else:
        logger.info("Window has been initialised.")

    window.mainloop()


def main():
    """
    Main Function
    
    Inspired by C/C++ main() function, that looks neat
    """
    try:
        # logger.info('Attempting to initialise High DPI awareness') # Don't clutter the log
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1) # High DPI
    except:
        logger.warning('Windows - Failed to enable High DPI awareness. Maybe not on Windows?')
    else:
        logger.info('Windows - High DPI awareness Enabled')

    try:
        # logger.info("Starting child process..")
        # tk_proc = Process(target=load_window, args=())
        # tk_proc.start()
        # tk_proc.join()
        load_window()
    except:
        pass
        # logger.critical("Failed to start child process!!!", exc_info=True)

if __name__ == "__main__":
    main()