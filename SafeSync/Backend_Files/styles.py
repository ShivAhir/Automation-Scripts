
from tkinter import ttk


def apply_styles():
    style = ttk.Style()
    # Optional: set theme for a modern look
    style.theme_use("clam")
    style.configure("Modern.TButton",
                    font=('Lucida Sans', 10, 'bold'),
                    padding=(12, 12),
                    relief="raised",
                    borderwidth=0,
                    focusthickness=3,
                    focuscolor="none"
                    )
    style.map("Modern.TButton",
              background=[("active", "#357ABD"), ("!active", "#1A5082")],
              foreground=[("active", "#FFFFFF"), ("!active", "#FFFFFF")])

    style.configure("TEntry", foreground="#000000",
                    relief='flat')

    style.map("TEntry",
              fieldbackground=[("focus", "#EDF5FB"), ("!focus", "#FFFFFF")],
              bordercolor=[("focus", "#EDF5FB"), ("!focus", "#FFFFFF")],)
