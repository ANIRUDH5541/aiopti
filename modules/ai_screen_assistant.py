import pyttsx3
import pytesseract
import pyautogui
import time
import spacy
from PIL import ImageGrab
from spacy.lang.en.stop_words import STOP_WORDS

# Initialize Spacy model for NLP
nlp = spacy.load("en_core_web_sm")

# Initialize Tesseract path (Make sure Tesseract is installed and path is correctly set)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture the screen
def capture_screen():
    screenshot = ImageGrab.grab()  # Captures the entire screen
    return screenshot

# Function to extract text from the captured screen
def extract_text(region):
    # Convert the screenshot to grayscale
    gray = region.convert("L")
    text = pytesseract.image_to_string(gray)
    return text

# Function to summarize extracted text using Spacy
def summarize_text(text):
    """Summarize the extracted text using basic NLP."""
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    important_sentences = [
        sent for sent in sentences if len(sent.split()) > 5 and not set(sent.split()).issubset(STOP_WORDS)
    ]
    summary = " ".join(important_sentences[:3])  # Take the first 3 important sentences
    return summary if summary else "No significant content detected."

def extract_entities(text):
    """Extract entities using spaCy's Named Entity Recognition (NER)."""
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    return entities


# Function to explain the current screen content
def explain_current_view():
    """Capture the screen, extract text, and provide a summary."""
    print("Analyzing current screen...")
    region = capture_screen()  # Screenshot of the screen
    text = extract_text(region)  # Extract text from the screenshot
    if text.strip():
        print(f"Extracted text:\n{text}")
        summary = summarize_text(text)
        print(f"\nSummary of the screen content:\n{summary}")
        
        # Extract and display entities
        entities = extract_entities(text)
        print(f"\nEntities detected: {entities}")
        speak(f"The screen shows: {summary}. I also found these key elements: {', '.join(entities)}.")
    else:
        print("No text detected on the screen.")
        speak("I could not detect any text on the screen.")

# Function to handle voice commands and trigger actions
def listen_for_commands():
    """Listen for user voice commands."""
    while True:
        # Assuming you're using a voice recognition tool like SpeechRecognition for listening
        command = listen_to_command()  # This should be your function that listens for the command
        
        if 'explain screen' in command:
            explain_current_view()
        elif 'exit' in command:
            print("Exiting the program.")
            speak("Goodbye.")
            break
        else:
            print(f"Command '{command}' not recognized.")
            speak("Sorry, I did not understand that command.")

# Dummy function to simulate voice command listening (replace with actual speech recognition)
def listen_to_command():
    """Simulate listening to a voice command."""
    # Simulating user saying "explain screen"
    time.sleep(2)  # Simulate delay between commands
    return "explain screen"

if __name__ == "__main__":
    print("AI Screen Assistant is running...")
    listen_for_commands()
