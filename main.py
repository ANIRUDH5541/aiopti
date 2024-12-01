import pyautogui
import pytesseract
import spacy
from modules.voice_recognition import recognize_speech
from modules.text_to_speech import speak_text
import webbrowser
from modules.ai_screen_assistant import explain_current_view  # Import the AI Screen Assistant function
from modules.screen_controll import highlight_tool  # Import highlight_tool function

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

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
    elif "submit" in extracted_text.lower():
        speak_text("I see you're about to submit something. Please make sure you've filled in all the fields.")
    elif "password" in extracted_text.lower() and "forgot" in extracted_text.lower():
        speak_text("It looks like you're trying to recover a password. Would you like assistance with that?")
    elif "tutorial" in extracted_text.lower():
        speak_text("You're watching a tutorial. Would you like me to summarize the next step?")
    else:
        speak_text(f"Here's what I found: {extracted_text[:100]}...")

def handle_command(command):
    """Process the recognized voice command and take action."""
    command = command.lower()

    if "open youtube" in command:
        speak_text("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command:
        speak_text("What would you like to search for on Google?")
        query = recognize_speech()
        if query:
            search_google(query)
        else:
            speak_text("I couldn't understand the search query. Try again.")
    elif "explain screen" in command:
        speak_text("Analyzing the current screen content...")
        extracted_text, _ = capture_and_analyze_screen()  # Capture screen and extract text
        provide_feedback_on_screen_content(extracted_text)  # Provide feedback on screen content
    elif "exit" or "bye" in command:
        speak_text("Goodbye!")
        return False
    else:
        speak_text("Sorry, I don't recognize this command yet.")
    
    return True

def search_google(query):
    """Open Google and search for the specified query."""
    speak_text(f"Searching Google for {query}.")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)

def main():
    """Main loop for the AI assistant."""
    speak_text("Hello! How can I assist you today?")
    while True:
        command = recognize_speech()
        if command:
            if not handle_command(command):
                break
        else:
            speak_text("I didn't catch that. Could you please repeat?")

def provide_feedback_on_screen_content(extracted_text):
    """Provide feedback or guide the user based on the screen content."""
    
    # Check for specific patterns in the extracted text
    if "error" in extracted_text.lower():
        speak_text("It seems there is an error on the screen. Would you like help resolving it?")
        # Highlight the error region if possible (Example coordinates: (x1, y1, x2, y2))
        highlight_tool("Error Region", ((100, 100), (400, 400)))
    elif "submit" in extracted_text.lower():
        speak_text("I see you're about to submit something. Please make sure you've filled in all the fields.")
        # Highlight the submit button region
        highlight_tool("Submit Button", ((500, 200), (700, 300)))  # Example coordinates
    elif "password" in extracted_text.lower() and "forgot" in extracted_text.lower():
        speak_text("It looks like you're trying to recover a password. Would you like assistance with that?")
        # Highlight password recovery tool (coordinates as an example)
        highlight_tool("Password Recovery", ((600, 400), (800, 500)))
    elif "tutorial" in extracted_text.lower():
        speak_text("You're watching a tutorial. Would you like me to summarize the next step?")
        # Highlight tutorial video region
        highlight_tool("Tutorial Area", ((100, 500), (800, 600)))
    else:
        speak_text(f"Here's what I found: {extracted_text[:100]}...")

if __name__ == "__main__":
    main()
