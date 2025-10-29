
def screenshot_to_code(url,fileName):
    import cv2
    import matplotlib.pyplot as plt
    import pytesseract

    from stringToScript import string_to_script
    
    pytesseract.pytesseract.tesseract_cmd = r"source\Tesseract-OCR\tesseract.exe"

    screenshot = cv2.imread(url)
    screenshot_rgb = cv2.cvtColor(screenshot,cv2.COLOR_BGR2RGB)

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

    string_to_script(string,fileName,execute=True)

screenshot_to_code("data\codpy.png","resultado")