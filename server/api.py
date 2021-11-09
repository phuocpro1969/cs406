from flask import Flask, request, redirect, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
from tera import *
from PIL import Image
import cv2
import numpy as np
import os
import json
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

RESULT_DIR = os.path.join(os.getcwd(), "server", "results")


@app.route('/uploader', methods=['POST'])
def upload_file():
    data = {'names': [], 'texts': []}
    if request.method == 'POST':
        f = request.files['files']
        # convert string data to numpy array
        np_img = np.fromstring(f.read(), np.uint8)
        # convert numpy array to image
        image = cv2.imdecode(np_img, cv2.IMREAD_GRAYSCALE)

        # Bước 1: Text box các thông tin
        d = pytesseract.image_to_data(image, output_type=Output.DICT)
        n_boxes = len(d['level'])
        boxes = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
        for i in range(n_boxes):
            (x, y, w, h) = (
                d['left'][i],
                d['top'][i],
                d['width'][i],
                d['height'][i]
            )
            boxes = cv2.rectangle(
                boxes,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        name = "boxes-" + str(uuid.uuid1())+".jpg"
        data['names'].append(name)
        cv2.imwrite(os.path.join(RESULT_DIR, name), boxes)

        # Bước 2: Nhận dạng thông tin
        extracted_text = pytesseract.image_to_string(image)
        data['texts'].append(extracted_text)

        return json.dumps(data, indent=4)


@app.route('/displays/<filename>', methods=['GET'])
def display_img(filename):
    return send_file(RESULT_DIR + "/" + filename)


if __name__ == '__main__':
    app.run(debug=True)
