import tkinter as tk
from tkinter import ttk


def show_loading_ui(root, title=None, msg=None, type=None):
    loading_window = tk.Toplevel(root)
    loading_window.configure(bg="#3E3E3E")
    loading_window.withdraw()
    loading_window.title(f"{title}")

    loading_window.iconbitmap("assets\Icon\SafeSync.ico")
    if type == None:
        loading_window.geometry("300x120")
    else:
        loading_window.geometry("330x100")
    loading_window.transient(root)
    loading_window.grab_set()

    loading_window.attributes('-topmost', True)

    # to center the loading window inside the root window
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    # to determine the position for the loading window
    loading_x = root_x + (root_width // 2) - (300 // 2)
    loading_y = root_y + (root_height // 2) - (100 // 2)

    loading_window.geometry(f"+{loading_x}+{loading_y}")
    loading_window.deiconify()
    if title == "Error":
        tk.Label(loading_window, text=f"{msg}",
                 font=("Lucida Sans", 10, 'bold'), fg="#ffffe0", wraplength=225).pack(pady=(40, 20))

    else:
        tk.Label(loading_window, text=f"{msg}",
                 font=("Lucida Sans", 10), fg="#ffffff", wraplength=225).pack(pady=20)

    if type == None:
        progress_bar = ttk.Progressbar(
            loading_window, mode="indeterminate", length=250)
        progress_bar.pack(pady=10)
        progress_bar.start(10)
        return loading_window, progress_bar
    else:
        return loading_window
