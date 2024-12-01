import pyttsx3
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def speak_text(text):
    """Convert text to speech and play it."""
    logging.info(f"Speaking: {text}")
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust speed if needed
    engine.setProperty('volume', 0.9)  # Set volume
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak_text("Hello! I am opti. How can I help you?")
