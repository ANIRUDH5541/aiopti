import tkinter as tk
from tkinter import messagebox

def display_summary_popup(summary):
    """Display the summary in a popup window with copy functionality."""
    def copy_to_clipboard():
        root.clipboard_clear()
        root.clipboard_append(summary)
        root.update()
        messagebox.showinfo("Copied", "Summary copied to clipboard!")

    root = tk.Tk()
    root.title("Video Summary")
    root.geometry("500x400")

    text_box = tk.Text(root, wrap="word")
    text_box.insert("1.0", summary)
    text_box.config(state="disabled")
    text_box.pack(expand=True, fill="both")

    copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
    copy_button.pack(pady=10)

    root.mainloop()
