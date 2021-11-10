import numpy as np
import cv2
import matplotlib.pyplot as plt
import pytesseract
import re


def find_amounts(text):
    amounts = re.findall(r'\d+\.\d{2}\b', text)
    floats = [float(amount) for amount in amounts]
    unique = list(dict.fromkeys(floats))
    return unique


if __name__ == '__main__':
    file_name = "results/step1.jpg"
    image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

    # Bước 1: Text box các thông tin
    d = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    n_boxes = len(d['level'])
    boxes = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top']
                        [i], d['width'][i], d['height'][i])
        boxes = cv2.rectangle(boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("boxes", boxes)
    cv2.waitKey(0)

    # Bước 2: Nhận dạng thông tin
    extracted_text = pytesseract.image_to_string(image)
    print(extracted_text)

    # Bước 3: Trích xuất thông tin bằng regular expression

    # Trích xuất tổng tiền hoá đơn

    amounts = find_amounts(extracted_text)
    print(amounts)
    if len(amounts) > 0:
        print(max(amounts))