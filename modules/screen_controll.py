import cv2
import numpy as np
import screen_brightness_control as sbc
import ctypes
import os
# modules/screen_controll.py

# modules/screen_controll.py

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def change_volume(level):
    """
    Change the system volume to the specified level (0 to 100).
    """
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)

        # Normalize level to range 0.0 - 1.0
        normalized_level = level / 100.0
        volume.SetMasterVolumeLevelScalar(normalized_level, None)

        return f"Volume is set to {level} percent."
    except Exception as e:
        return f"Failed to set volume. Error: {e}"

# If you have set_brightness or highlight_tool functions, ensure they're also in this file.



def highlight_tool(window_name, region):
    """Highlight a specific region on the screen."""
    screen = np.zeros((1080, 1920, 3), dtype=np.uint8)  # Simulated screen
    cv2.rectangle(screen, region[0], region[1], (0, 255, 0), 2)  # Draw rectangle around the region
    cv2.imshow(window_name, screen)
    cv2.waitKey(3000)  # Show the highlighted region for 3 seconds
    cv2.destroyAllWindows()

def set_brightness(level):
    """Set screen brightness to a specific level (0-100)."""
    try:
        sbc.set_brightness(level)
        return f"Brightness set to {level} percent."
    except Exception as e:
        return f"Failed to set brightness. Error: {e}"

if __name__ == "__main__":
    highlight_tool("Tool Highlighter", ((100, 100), (400, 400)))
