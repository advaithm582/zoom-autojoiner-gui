from tkinter import messagebox


OBJECT_ORIENTED = False


main_window = menu_bar = meeting_list_frame = None

def set_objects(main_window_=None, menu_bar_=None, meeting_list_frame_=None):
    """set_objects

    Set the objects from the Extensions API.

    Args:
        main_window (tk.Tk): The TK Main window.
        menu_bar (tk.Menu): The TK menubar
        meeting_list_frame (tk.Frame): The TK Frame.
    """
    global main_window, menu_bar, meeting_list_frame
    main_window = main_window_
    menu_bar = menu_bar_
    meeting_list_frame = meeting_list_frame_

def main():
    # messagebox.showinfo("EXTENSIONFATHER IS RUNNING", ("Extensionfather is "
    #     "running properly, as intended."))
    
    menu_bar.make_list_to_menu([
        ["Extensions", [
                ["Extensionfather", None, None, None]
            ]
        ]
    ])