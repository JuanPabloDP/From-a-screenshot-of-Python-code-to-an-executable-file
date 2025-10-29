import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt

code = cv2.imread("..\data\codpy.png")

plt.imshow(code)
plt.axis("off")
plt.show()

pytesseract.pytesseract.tesseract_cmd = r"..\source\Tesseract-OCR\tesseract.exe"

list_result = pytesseract.image_to_string(code)
print(list_result)