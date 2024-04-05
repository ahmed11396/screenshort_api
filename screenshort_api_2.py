from flask import Flask, send_file
import io
import pyautogui
import threading
import time
from PIL import Image

app = Flask(__name__)

# Function to take a screenshot and save it to a bytesIO object
def take_screenshot(monitor_info):
    x, y, width, height = monitor_info['left'], monitor_info['top'], monitor_info['width'], monitor_info['height']
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    bytes_io = io.BytesIO()
    screenshot.save(bytes_io, format='PNG')
    bytes_io.seek(0)
    return bytes_io

# Function to continuously take screenshots every 5 seconds
def take_screenshots():
    while True:
        for monitor_index, monitor_info in enumerate(pyautogui.getAllMonitors()):
            bytes_io = take_screenshot(monitor_info)
            screenshots[monitor_index] = bytes_io
        time.sleep(5)

# Dictionary to store the latest screenshot for each monitor
screenshots = {}

# Start the thread to take screenshots
screenshot_thread = threading.Thread(target=take_screenshots)
screenshot_thread.daemon = True
screenshot_thread.start()

@app.route('/screenshot/<int:monitor>')
def get_screenshot(monitor):
    if monitor in screenshots:
        return send_file(screenshots[monitor], mimetype='image/png')
    else:
        return 'Monitor not found'

if __name__ == '__main__':
    app.run(debug=True)
