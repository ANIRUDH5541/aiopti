import speech_recognition as sr
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def recognize_speech():
    """Capture audio and return text using Google Speech API."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logging.info("Listening for a command...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            logging.info(f"Recognized command: {command}")
            return command
        except sr.UnknownValueError:
            logging.error("Could not understand the audio. Please try again.")
            return None
        except sr.RequestError as e:
            logging.error(f"Speech recognition error: {e}")
            return None
        except sr.WaitTimeoutError:
            logging.error("Listening timed out.")
            return None

if __name__ == "__main__":
    command = recognize_speech()
    if command:
        print(f"Command received: {command}")
