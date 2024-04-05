from flask import Flask, send_file
import io
import pyautogui
import numpy as np
from PIL import Image

app = Flask(__name__)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

@app.route('/screenshot')
def screenshot():
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)  # Convert the screenshot to a NumPy array
    
    # Sort the pixels of the screenshot using bubble sort
    sorted_screenshot = np.apply_along_axis(bubble_sort, 2, screenshot)
    
    # Create an image from the sorted screenshot pixels
    sorted_image = Image.fromarray(np.uint8(sorted_screenshot))
    
    # Save the sorted image to a bytesIO object
    bytes_io = io.BytesIO()
    sorted_image.save(bytes_io, format='PNG')
    bytes_io.seek(0)
    
    # Return the sorted image as a file
    return send_file(bytes_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
