from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from tera import *
import cv2
import numpy as np

app = Flask(__name__)

global img

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      #convert string data to numpy array
      np_img = np.fromstring(f.read(), np.uint8)
      # convert numpy array to image
      image = cv2.imdecode(np_img, cv2.IMREAD_GRAYSCALE)

      # Bước 1: Text box các thông tin
      d = pytesseract.image_to_data(image, output_type=Output.DICT)
      n_boxes = len(d['level'])
      boxes = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
      for i in range(n_boxes):
         (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
         boxes = cv2.rectangle(boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)

      cv2.imshow('image', boxes)
      cv2.waitKey(0)

      # Bước 2: Nhận dạng thông tin
      extracted_text = pytesseract.image_to_string(image)
      print(extracted_text)

      return 'file uploaded successfully'

if __name__ == '__main__':
   app.run(debug = True)