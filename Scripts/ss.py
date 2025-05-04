import os
import time
import cv2
import numpy as np
import pyautogui
from datetime import datetime

# Configuration
SCREENSHOT_DIR = "screenshots"
SCROLL_PIXELS = 300  
SCROLL_DELAY = 1.5  
SCROLL_ATTEMPTS = 10
COMPARISON_THRESHOLD = 10
MAIN_DELAY = 2

def setup():
    """Create directories if needed"""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

def take_screenshot():
    """Take a screenshot and return as PIL Image"""
    return pyautogui.screenshot()

def compare_images(img1, img2, threshold=COMPARISON_THRESHOLD):
    """Check if two images are different using pixel difference"""
    diff = cv2.absdiff(np.array(img1), np.array(img2))
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, threshold_diff = cv2.threshold(gray_diff, threshold, 255, cv2.THRESH_BINARY)
    non_zero_pixels = cv2.countNonZero(threshold_diff)
    return non_zero_pixels > 0

def scroll_down(pixels=SCROLL_PIXELS):
    """Scroll down the screen with more reliable method"""
   
    try:
        pyautogui.scroll(-pixels)  # Negative for scrolling down
    except:
        # Alternative method - click in center and scroll
        x, y = pyautogui.size()
        pyautogui.moveTo(x//2, y//2)
        pyautogui.scroll(-pixels)

def save_screenshot(screenshot):
    """Save screenshot with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{SCREENSHOT_DIR}/screenshot_{timestamp}.png"
    screenshot.save(filename)
    print(f"Saved: {filename}")
    return filename

def main():
    setup()
    print("Monitoring for new content. Press Ctrl+C to stop.")
    
    prev_screenshot = take_screenshot()
    scroll_count = 0
    
    try:
        while True:
            time.sleep(MAIN_DELAY)
            new_screenshot = take_screenshot()
            
            if compare_images(prev_screenshot, new_screenshot):
                save_screenshot(new_screenshot)
                prev_screenshot = new_screenshot
                scroll_count = 0
            else:
                if scroll_count < SCROLL_ATTEMPTS:
                    print(f"Attempting scroll ({scroll_count + 1}/{SCROLL_ATTEMPTS})")
                    scroll_down()
                    scroll_count += 1
                    time.sleep(SCROLL_DELAY)  
                else:
                    print("Max scroll attempts reached. Waiting...")
                    scroll_count = 0  
                    
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()