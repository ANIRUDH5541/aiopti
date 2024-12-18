import pyautogui
import pytesseract
import spacy
import webbrowser
import re
from modules.voice_recognition import recognize_speech
from modules.text_to_speech import speak_text
from modules.screen_controll import set_brightness, change_volume, highlight_tool
from modules.ai_screen_assistant import explain_current_view  # Import the AI Screen Assistant function
from modules.youtube_control import YouTubeController
import speech_recognition as sr
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from modules.summarize import summarize_video_and_display  
from modules.popup_window import display_summary_popup
from modules.file_search import handle_file_search_command, close_file

driver_path = r"C:\WebDriver\chromedriver.exe"
youtube = YouTubeController(driver_path=driver_path)

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Setup recognizer for voice commands
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen_for_opti():
    """Continuously listen for the keyword 'opti' to activate the assistant."""
    with mic as source:
        print("Listening for 'opti'...")  # Can be used for debugging or logging
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"Heard: {command}")
                
                if "opti" in command:
                    print("Activating AI Assistant...")
                    speak_text("How can I assist you?")
                    main()  # Trigger the main function when 'opti' is heard
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Could not request results, check your network connection.")
                break

def extract_number(command):
    """Extract the first number from a command."""
    match = re.search(r"\b\d+\b", command)
    return int(match.group()) if match else None


def capture_and_analyze_screen():
    """Capture the screen and extract text using OCR."""
    screenshot = pyautogui.screenshot()  # Capture a screenshot of the screen
    screenshot.save("screenshot.png")

    # Convert the screenshot to text using pytesseract
    extracted_text = pytesseract.image_to_string(screenshot)

    # Process the text to understand it using NLP
    doc = nlp(extracted_text)

    return extracted_text, doc


def provide_feedback_on_screen_content(extracted_text):
    """Provide feedback or guide the user based on the screen content."""
    # Check for specific patterns in the extracted text
    if "error" in extracted_text.lower():
        speak_text("It seems there is an error on the screen. Would you like help resolving it?")
        highlight_tool("Error Region", ((100, 100), (400, 400)))  # Example coordinates
    elif "submit" in extracted_text.lower():
        speak_text("I see you're about to submit something. Please make sure you've filled in all the fields.")
        highlight_tool("Submit Button", ((500, 200), (700, 300)))  # Example coordinates
    elif "password" in extracted_text.lower() and "forgot" in extracted_text.lower():
        speak_text("It looks like you're trying to recover a password. Would you like assistance with that?")
        highlight_tool("Password Recovery", ((600, 400), (800, 500)))  # Example coordinates
    elif "tutorial" in extracted_text.lower():
        speak_text("You're watching a tutorial. Would you like me to summarize the next step?")
        highlight_tool("Tutorial Area", ((100, 500), (800, 600)))  # Example coordinates
    else:
        speak_text(f"Here's what I found: {extracted_text[:100]}...")


def search_google(query):
    """Open Google and search for the specified query."""
    speak_text(f"Searching Google for {query}.")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)

def summarize_text(text):
    """Summarizes the given text."""
    # Implementing a simple summarizer here for demonstration
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.summarizers.lsa import LsaSummarizer
    parser = PlaintextParser.from_string(text, PlaintextParser.from_string(text))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)
    return " ".join(str(sentence) for sentence in summary)

def handle_command(command):
    """Process the recognized voice command and take action."""
    command = command.lower()

    if "opti" in command:  # Start listening when 'opti' is said
        command = command.replace("opti", "").strip()  # Clean up the command

    if "youtube" in command:  # Automatically detect YouTube-related commands
        if "search youtube for" in command:
            query = command.replace("search youtube for", "").strip()
            if query:
                speak_text(f"Searching for {query} on YouTube...")
                video_titles = youtube.search_youtube(query)
                if video_titles:
                    speak_text("I found the following videos:")
                    for title in video_titles:
                        speak_text(title)
                    speak_text("Please say the name of the video you want to play.")
                    video_title = recognize_speech()
                    if video_title:
                        response = youtube.play_video_by_title(video_title)
                        speak_text(response)
                    else:
                        speak_text("I couldn't understand the video title. Try again.")
                else:
                    speak_text("No videos found for the search query.")
            else:
                speak_text("Please specify what to search on YouTube.")

        elif "set playback speed to" in command:
           print(f"Command: {command}")
           match = re.search(r"(\d+(\.\d+)?)", command)
           if match:
              speed = float(match.group(1))
              print(f"Detected speed: {speed}")
              response = youtube.adjust_playback_speed(speed)
              print(f"Playback speed response: {response}")
              speak_text(response)

        elif "set quality to" in command:
           print(f"Command: {command}")
           match = re.search(r"(\d+)", command)
           if match:
              quality = int(match.group(1))
              print(f"Detected quality: {quality}")
              response = youtube.adjust_quality(quality)
              print(f"Quality adjustment response: {response}")
              speak_text(response)

        elif "turn subtitles on" in command:
           print(f"Command: {command}")
           response = youtube.toggle_subtitles("on")
           print(f"Subtitle on response: {response}")
           speak_text(response)

        elif "turn subtitles off" in command:
           print(f"Command: {command}")
           response = youtube.toggle_subtitles("off")
           print(f"Subtitle off response: {response}")
           speak_text(response)

        elif "summarize video" in command:
           print(f"Command: {command}")
           speak_text("Summarizing the video content...")
           video_id = youtube.get_video_id()
           print(f"Video ID: {video_id}")
           if video_id:
              video_text = youtube.get_video_text()
              print(f"Video text: {video_text[:100]}...")
              if video_text:
                summary = summarize_text(video_text)
                display_summary_popup(summary)
                speak_text("Summary displayed in the popup.")
              else:
                speak_text("No subtitles or transcript found for this video.")
           else:
               speak_text("Unable to find the video ID.")
  

        elif "set fullscreen" in command or "fullscreen the video" in command:
            response = youtube.set_fullscreen()
            speak_text(response)

        elif "close youtube" in command:
            speak_text("Closing YouTube...")
            youtube.close()
                
    # Brightness commands
    elif "set brightness" in command:
        level = extract_number(command)
        if level is not None and 0 <= level <= 100:
            response = set_brightness(level)
            speak_text(f"Brightness is set to {level} percent.")
        else:
            speak_text("Please specify a brightness level between 0 and 100.")
    elif "increase brightness" in command:
        response = set_brightness(100)  # Max brightness
        speak_text("Brightness is set to 100 percent.")
    elif "decrease brightness" in command:
        response = set_brightness(20)  # Min brightness
        speak_text("Brightness is set to 20 percent.")

    # Volume commands
    elif "set volume" in command:
        level = extract_number(command)
        if level is not None and 0 <= level <= 100:
            response = change_volume(level)
            speak_text(f"Volume is set to {level} percent.")
        else:
            speak_text("Please specify a volume level between 0 and 100.")
    elif "increase volume" in command:
        response = change_volume(100)  # Max volume
        speak_text("Volume is set to 100 percent.")
    elif "decrease volume" in command:
        response = change_volume(20)  # Min volume
        speak_text("Volume is set to 20 percent.")
    elif "mute" in command:
        response = change_volume(0)  # Mute volume
        speak_text("Volume is muted.")
    elif "unmute" in command:
        response = change_volume(50)  # Set volume to 50%
        speak_text("Volume is set to 50 percent.")

    # Screen-related commands
    elif "explain screen" in command:
        speak_text("Analyzing the current screen content...")
        extracted_text, _ = capture_and_analyze_screen()  # Capture screen and extract text
        provide_feedback_on_screen_content(extracted_text)  # Provide feedback on screen content

    elif "search google" in command:
        speak_text("What would you like to search for on Google?")
        query = recognize_speech()
        if query:
            search_google(query)
        else:
            speak_text("I couldn't understand the search query. Try again.")

    elif "open" in command:  # General file open command
        print(f"Command: {command}")
        response = handle_file_search_command(command)
        print(response)
        speak_text(response)

    elif "close" in command:  # File close command
        print("Which file/application would you like to close?")
        file_name = input("Enter the file/application name to close: ")
        close_file(file_name)

    # Exit
    elif "exit" in command:
        speak_text("Goodbye!")
        return False

    # Unknown command fallback
    else:
        speak_text("Sorry, I don't recognize this command yet.")

    return True


def main():
    """Main loop for the AI assistant."""
    speak_text("Hello! How can I assist you today?")
    while True:
        command = recognize_speech()
        if command:
            if "exit" in command:
                speak_text("Goodbye!")
                break
            handle_command(command)
        else:
            speak_text("I didn't catch that. Could you please repeat?")


if __name__ == "__main__":
    main()
