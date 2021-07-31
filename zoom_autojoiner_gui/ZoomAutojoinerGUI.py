from zoom_autojoiner_gui.views import MainWindow

if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1) # High DPI
    except:
        pass
    window = MainWindow()
    window.mainloop()