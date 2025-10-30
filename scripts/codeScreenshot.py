import cv2
import matplotlib.pyplot as plt
import pytesseract
import numpy

from stringToScript import string_to_script
    
pytesseract.pytesseract.tesseract_cmd = r"..\source\Tesseract-OCR\tesseract.exe"
    
def screenshot_to_code(url,fileName,p1=2,p2=5,p3=2,p4=5,p5=2):
    screenshot = cv2.imread(url)
    screenshot_rgb = cv2.cvtColor(screenshot,cv2.COLOR_BGR2RGB)
    
    # tratamiento
    
    screenshot_rgb = cv2.bitwise_not(screenshot_rgb)

    for _ in range(p1):
        kernel = numpy.ones((2,2), numpy.uint8)
        screenshot_rgb = cv2.dilate(screenshot_rgb, kernel, iterations=5)

    for _ in range(p2):
        screenshot_rgb = cv2.GaussianBlur(screenshot_rgb, (15, 15), 0)

    for _ in range(p3):
        kernel = numpy.ones((10, 10), numpy.uint8)
        screenshot_rgb = cv2.erode(screenshot_rgb, kernel)
        
        
    screenshot_rgb = cv2.bitwise_not(screenshot_rgb)

    for _ in range(p4):
        kernel = numpy.ones((5, 5), numpy.uint8)
        screenshot_rgb = cv2.erode(screenshot_rgb, kernel)
        kernel = numpy.ones((2,2), numpy.uint8)
        screenshot_rgb = cv2.dilate(screenshot_rgb, kernel, iterations=2)

    for _ in range(p5):
        kernel = numpy.ones((5,5), numpy.uint8)
        screenshot_rgb = cv2.dilate(screenshot_rgb, kernel, iterations=3)

    plt.imshow(screenshot_rgb)
    plt.axis("off")
    plt.show()

    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DATAFRAME)

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
        
    def normalize_quotes(text):
        replacements = {
            '‘': "'",
            '’': "'",
            '‚': "'",
            '‛': "'",

            '“': "'",
            '”': "'",
            '„': "'",
            '‟': "'",
            
            '"': "'",
            '"': "'",
            '"': "'",
            '"': "'",
        }

        for fancy, normal in replacements.items():
            text = text.replace(fancy, normal)
        return text

    string_to_script(normalize_quotes(string),fileName,execute=True)

screenshot_to_code("..\data\codpy.png","resultado")