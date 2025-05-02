import tkinter as tk


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None

        # Bind hover events
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        # Create a tooltip window
        x = self.widget.winfo_rootx() + event.x + 20
        y = self.widget.winfo_rooty() + event.y + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.overrideredirect(True)  # Remove window decorations
        self.tooltip.geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#357ABD",
                         foreground="white", font=("Lucida Console", 10))
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
