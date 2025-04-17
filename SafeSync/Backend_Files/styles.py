# Define styles for the window and widgets
WINDOW_STYLE = {
    "bg": "#F0F8FF"  # Alice Blue background
}

LABEL_STYLE = {
    "bg": "#F0F8FF",  # Match the window background
    "fg": "#333333",  # Dark gray text
    "font": ("Helvetica", 14, "bold")  # Modern font with bold text
}

TEXT_WIDGET_STYLE = {
    "bg": "#FFFFFF",  # White background for text widgets
    "fg": "#000000",  # Black text
    "font": ("Courier New", 12),  # Monospace font for text
    "wrap": "word",  # Wrap text at word boundaries
    "relief": "solid",  # Add a border around the text widget
    "bd": 1  # Border width
}

BUTTON_STYLE = {
    "bg": "#87CEEB",  # Sky Blue background
    "fg": "#FFFFFF",  # White text
    "font": ("Arial", 12, "bold"),  # Bold text
    "activebackground": "#4682B4",  # Steel Blue when hovered
    "activeforeground": "#FFFFFF",  # White text when hovered
    "relief": "raised",  # Raised button style
    "bd": 2  # Border width
}

EXIT_BUTTON_STYLE = {
    "bg": "#FF6347",  # Tomato Red background
    "fg": "#FFFFFF",  # White text
    "font": ("Arial", 12, "bold"),
    "activebackground": "#CD5C5C",  # Indian Red when hovered
    "activeforeground": "#FFFFFF",
    "relief": "raised",
    "bd": 2
}
