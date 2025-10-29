
def string_to_script(string,fileName,execute=False):
    with open(f"..\data\{fileName}.py", "w", encoding="utf-8") as f:
        f.write(string)

    if execute==True:
        with open(f"..\data\{fileName}.py", "r") as f:
            code = f.read()
            exec(code)

