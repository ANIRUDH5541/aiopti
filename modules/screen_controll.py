import cv2
import numpy as np

def highlight_tool(window_name, region):
    """Highlight a specific region on the screen."""
    screen = np.zeros((1080, 1920, 3), dtype=np.uint8)  # Simulated screen
    cv2.rectangle(screen, region[0], region[1], (0, 255, 0), 2)  # Draw rectangle around the region
    cv2.imshow(window_name, screen)
    cv2.waitKey(3000)  # Show the highlighted region for 3 seconds
    cv2.destroyAllWindows()

if __name__ == "__main__":
    highlight_tool("Tool Highlighter", ((100, 100), (400, 400)))
