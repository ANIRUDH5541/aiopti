from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time


class YouTubeController:
    def __init__(self, driver_path=None):
        """Initialize the YouTubeController with necessary configurations."""
        self.driver_path = driver_path
        self.driver = None

    def open_youtube(self):
        """Open YouTube in a new browser window."""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")

        # Use the driver path if provided
        if self.driver_path:
            service = Service(self.driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            self.driver = webdriver.Chrome(options=chrome_options)

        self.driver.get("https://www.youtube.com")
        time.sleep(3)  # Allow time for the page to load

    def search_youtube(self, query):
        """Search for a video on YouTube."""
        if not self.driver:
            self.open_youtube()
        
        try:
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)  # Wait for results to load

            # Retrieve video titles for feedback
            videos = self.driver.find_elements(By.ID, "video-title")
            video_titles = [video.get_attribute("title") for video in videos[:5]]
            return video_titles
        except Exception as e:
            return f"Error during search: {e}"

    def play_video_by_title(self, title):
        """Play a video by its title."""
        try:
            videos = self.driver.find_elements(By.ID, "video-title")
            for video in videos:
                if title.lower() in video.get_attribute("title").lower():
                    video.click()
                    time.sleep(1)  # Allow the video to start
                    return f"Playing video titled '{title}'"
            return f"Video titled '{title}' not found."
        except Exception as e:
            return f"Error while trying to play video: {e}"

    def adjust_playback_speed(self, speed):
        """Adjust the playback speed of the video."""
        try:
            settings_button = self.driver.find_element(By.CLASS_NAME, "ytp-settings-button")
            settings_button.click()
            time.sleep(1)
            speed_button = self.driver.find_element(By.XPATH, "//div[text()='Playback speed']")
            speed_button.click()
            time.sleep(1)
            speed_option = self.driver.find_element(By.XPATH, f"//span[text()='{speed}']")
            speed_option.click()
            return f"Playback speed set to {speed}."
        except Exception as e:
            return f"Failed to adjust playback speed: {e}"


    def adjust_quality(self, quality):
        """Adjust the video quality."""
        try:
            settings_button = self.driver.find_element(By.CLASS_NAME, "ytp-settings-button")
            settings_button.click()
            time.sleep(1)
            quality_button = self.driver.find_element(By.XPATH, "//div[text()='Quality']")
            quality_button.click()
            time.sleep(1)
            quality_option = self.driver.find_element(By.XPATH, f"//span[contains(text(), '{quality}p')]")
            quality_option.click()
            return f"Quality set to {quality}p."
        except Exception as e:
            return f"Failed to adjust video quality: {e}"

    def toggle_subtitles(self, state):
        """Turn subtitles on or off."""
        try:
            settings_button = self.driver.find_element(By.CLASS_NAME, "ytp-settings-button")
            settings_button.click()
            time.sleep(1)
            subtitles_button = self.driver.find_element(By.XPATH, "//div[text()='Subtitles/CC']")
            subtitles_button.click()
            time.sleep(1)
            if state == "on":
                on_option = self.driver.find_element(By.XPATH, "//span[text()='English']")
                on_option.click()
            elif state == "off":
                off_option = self.driver.find_element(By.XPATH, "//span[text()='Off']")
                off_option.click()
            return f"Subtitles turned {state}."
        except Exception as e:
            return f"Failed to toggle subtitles: {e}"

    def set_fullscreen(self):
        """Set the video to fullscreen."""
        try:
            fullscreen_button = self.driver.find_element(By.CLASS_NAME, "ytp-fullscreen-button")
            fullscreen_button.click()
            return "Video set to fullscreen."
        except Exception as e:
            return f"Error while setting fullscreen: {e}"

    def exit_fullscreen(self):
        """Exit fullscreen mode."""
        try:
            fullscreen_button = self.driver.find_element(By.CLASS_NAME, "ytp-fullscreen-button")
            fullscreen_button.click()
            return "Exited fullscreen mode."
        except Exception as e:
            return f"Error while exiting fullscreen: {e}"

    def close(self):
        """Close the browser session."""
        if self.driver:
            self.driver.quit()
            self.driver = None
