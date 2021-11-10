from flask import Flask, request, redirect, send_file
from flask_cors import CORS
from tera import *
from image_process import *
import cv2
import numpy as np
import os
import json
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

RESULT_DIR = os.path.join(os.getcwd(), "results")


@app.route('/uploader', methods=['POST'])
def upload_file():
    data = {'names': [], 'texts': [], 'steps': []}
    if request.method == 'POST':

        id = str(uuid.uuid1())

        f = request.files['files']

        # convert string data to numpy array
        np_img = np.fromstring(f.read(), np.uint8)
        # convert numpy array to image
        image = cv2.imdecode(np_img, cv2.IMREAD_UNCHANGED)

        name = "input-" + id +".jpg"
        data['names'].append(name)
        data['texts'].append("")
        data['steps'].append("Step 0: Input image")
        cv2.imwrite(os.path.join(RESULT_DIR, name), image)

        # Step 1: process image

        resize_ratio = 500 / image.shape[0]

        original = image.copy()
        image = opencv_resize(image, resize_ratio)

        # Chuyển ảnh sang Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Dùng GaussianBlur 5x5 để giảm nhiễu
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Nhận diện các vùng trắng
        rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        dilated = cv2.dilate(blurred, rectKernel)

        # Hiển thị các Object trong hình dạng cạnh viền (nền đen)

        edged = cv2.Canny(dilated, 100, 200, apertureSize=3)

        # Detect tất cả các cạnh viền của vật thể
        contours, _ = cv2.findContours(
            edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Giữ lại 10 đường viền rõ nét
        largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        get_receipt_contour(largest_contours)

        receipt_contour = get_receipt_contour(largest_contours)

        scanned = wrap_perspective(
            original.copy(), contour_to_rect(receipt_contour, resize_ratio))

        result = bw_scanner(scanned)

        if len(result) > 0:
            name = "receipt-" + id +".jpg"
            data['names'].append(name)
            data['texts'].append("")
            data['steps'].append("Step 1: Detect receipt")
            cv2.imwrite(os.path.join(RESULT_DIR, name), result)

            # step 2: detect text

            # Text box các thông tin
            image=result
            boxes = cv2.cvtColor(result.copy(),cv2.COLOR_GRAY2RGB)
            d = pytesseract.image_to_data(boxes, output_type= pytesseract.Output.DICT)
            n_boxes = len(d['level'])

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

            name = "boxes-" + id + ".jpg"
            data['names'].append(name)
            data['steps'].append("Step 2: Detect box && text")
            cv2.imwrite(os.path.join(RESULT_DIR, name), boxes)

            # Nhận dạng thông tin
            extracted_text = pytesseract.image_to_string(image)
            amounts = find_amounts(extracted_text)
            print(amounts)
            data['texts'].append(repr(extracted_text).replace("\\n", "<br/>").replace("'", "").replace("\\x0c", ""))

            if len(amounts) > 0:
                data['names'].append("")
                data['steps'].append("Step 3: Calculate amount of bill")
                data['texts'].append("<h1>total: "+str(max(amounts)) + "</h1>")

        return json.dumps(data, indent=4)


@app.route('/displays/<filename>', methods=['GET'])
def display_img(filename):
    return send_file(RESULT_DIR + "/" + filename)


if __name__ == '__main__':
    app.run(debug=True)
