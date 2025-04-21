
from tkinter import ttk

def apply_button_style():
    style = ttk.Style()

    # Optional: set theme for a modern look
    style.theme_use("clam")


    style.configure("Modern.TButton",
        font=('Lucida Sans', 10, 'bold'),
        padding=(12, 12),
        background="#1A5082",
        foreground="#FFFFFF",
        relief="raised",
        borderwidth=0,
        focusthickness=3,
        focuscolor="none"
    )

    style.map("Modern.TButton",
        background=[("active", "#357ABD")],
        foreground=[("active", "#FFFFFF")]
    )
