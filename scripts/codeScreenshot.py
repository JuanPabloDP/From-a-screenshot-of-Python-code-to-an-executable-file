import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pytesseract
from pytesseract import Output

from stringToScript.py import string_to_script

pytesseract.pytesseract.tesseract_cmd = r"..\source\Tesseract-OCR\tesseract.exe"

code = cv2.imread("..\data\codpy.png")

data = pytesseract.image_to_data(code, output_type=pytesseract.Output.DATAFRAME)

data = data.dropna(subset=['text'])
data = data[data['text'].str.strip() != '']

lines = (data
    .sort_values(['block_num', 'par_num', 'line_num', 'left'])
    .groupby(['page_num', 'block_num', 'par_num', 'line_num'], as_index=False)
    .agg({
        'left': 'min',
        'text': lambda x: ' '.join(x)
    })
)

counts, bins, _ = plt.hist(lines["left"])
plt.close()

clases = []
for i in range(len(bins)-1):
    if counts[i] > 0:
        clases.append((bins[i], bins[i+1]))

def obtener_indentacion(numero):
    for i, (start, end) in enumerate(clases):
        if start <= numero < end:
            return i
    return len(clases) - 1

lines["Indentacion"] = lines["left"].apply(obtener_indentacion)

string = ""

for i in range(len(lines)):
    if lines.iloc[i]["line_num"] == 1:
        aux = "\n"
    else:
        aux = ""
    aux += lines.iloc[i]["Indentacion"] * "\t" + lines.iloc[i]["text"] + "\n"
    string += aux

string_to_script(string,"resultado",execute=True)