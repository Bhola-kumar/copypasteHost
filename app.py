# app.py

from flask import Flask, jsonify
from flask_cors import CORS
import pyautogui as pg
import pyperclip
import time
import pyperclip
from PIL import ImageGrab, Image
import pytesseract as pyt
import cv2
import numpy as np
# import keyboard

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/execute', methods=['POST'])
def execute():
    try:
        # keyboard.wait('ctrl+alt+v')
        code = pyperclip.paste()

        if not code:
            return jsonify({"error": "Clipboard is empty"}), 400
        elif not isinstance(code, str):
            return jsonify({"error": "Clipboard content is not text"}), 400

        def print_code(code):
            count = 0
            for line in code.splitlines():
                if line.startswith('#'):
                    continue
                else:
                    count += 1
                    pg.write('# ')
                    if '#' in line:
                        line = line[:line.index('#')]
                    pg.write(line.rstrip())
                    pg.press('space')
                    pg.press('enter')
            
            for _ in range(count):
                pg.hotkey('ctrl', 'altleft', 'up')
                # pg.press('up')
                # pg.hotkey('ctrl','/')
            # pg.press('delete', presses=2)
            pg.hotkey('ctrl','/')
            return count
        

        # t = 0.3
        t=7
        time.sleep(t)  
        
        count = print_code(code)
        return jsonify({"lines_processed": count}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/copy', methods=['POST'])
def copy():
    try:
        # pg.hotkey('win', 'shift', 's')
        # print("Select the area to capture the text...")
        # time.sleep(8)
        screenshot = ImageGrab.grabclipboard()
        if isinstance(screenshot, Image.Image):
            open_cv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            pyt.pytesseract.tesseract_cmd = "C:\\Users\\bhola\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
            extracted_text = pyt.image_to_string(open_cv_image)
            pyperclip.copy(extracted_text)
            # print("Text copied to clipboard successfully.")
            return jsonify({"message": "Text copied to clipboard successfully", "text_copied": extracted_text}), 200

        else:
            # print("No image found in clipboard.")
            return jsonify({"error": "No image found in clipboard"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    # pass
