# summarize.py
import tkinter as tk
import pyperclip  # To copy text to the clipboard
from modules.text_to_speech import speak_text


def display_summary_overlay(summary_text):
    """Display the summarized text next to the YouTube video with a copy button."""
    # Create the main window for the overlay
    overlay_window = tk.Tk()
    overlay_window.title("Video Summary")
    
    # Set the window to be always on top
    overlay_window.attributes("-topmost", True)
    overlay_window.geometry("300x200+100+100")  # Adjust the position and size as needed

    # Create a label to display the summary text
    summary_label = tk.Label(overlay_window, text=summary_text, wraplength=250, justify="left")
    summary_label.pack(padx=10, pady=10)

    # Create a button to copy the text to the clipboard
    def copy_to_clipboard():
        pyperclip.copy(summary_text)
        copy_button.config(text="Copied!")

    copy_button = tk.Button(overlay_window, text="Copy Text", command=copy_to_clipboard)
    copy_button.pack(pady=10)

    # Start the Tkinter event loop
    overlay_window.mainloop()

def summarize_video_and_display(command, youtube, summarize_text):
    """Summarizes the video and displays the summary overlay."""
    if "summarize video" in command:  # Triggered command
        speak_text("Summarizing the video content...")
        video_text = youtube.get_video_text()  # Example function to extract video transcript
        
        if video_text:
            # Summarize the text
            summary = summarize_text(video_text)
            speak_text(f"Here's the summary: {summary}")
            
            # Display the summary overlay beside the video
            display_summary_overlay(summary)
        else:
            speak_text("Sorry, I couldn't find any subtitles or transcript for this video.")
