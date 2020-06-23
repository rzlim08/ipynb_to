import json
import argparse
import re


class Parser:
    def __init__(self):
        self.lines = []
        self.caller = None

    def add_line(self, line):
        self.lines.append(line)

    def match_caller(self, source):
        for line in source:
            if re.match(self.caller, line):
                self.lines.append(source)
                break

    def printlines(self, f):
        for cell in self.lines:
            for line in cell:
                if re.match(self.caller, line) is None:
                    f.write(line)
            f.write("\n")

class ImportParser(Parser):
    def __init__(self):
        super().__init__()
        self.caller = re.compile(r"# *import[\\n]?")


class ExportParser(Parser):
    def __init__(self):
        super().__init__()
        self.caller = re.compile(r"# *export[\\n]?")


class MainParser(Parser):
    def __init__(self):
        super().__init__()
        self.caller = re.compile(r"# *__main__")

    def printlines(self, f):
        f.write("if __name__ == '__main__': \n")
        for cell in self.lines:
            for line in cell:
                if re.match(self.caller, line) is None:
                    f.write("    ")
                    f.write(line)
            f.write("\n")


def export_py(imports, export, main, name):
    with open(name, "w+") as f:
        imports.printlines(f)
        export.printlines(f)
        main.printlines(f)


def parse_json(nb_path):
    # Read notebook
    with open(nb_path) as f:
        nb = json.load(f)
    
    # Parse nb source
    main = MainParser()
    imports = ImportParser()
    export = ExportParser()
    for cell in nb["cells"]:
        if cell["source"]:
            imports.match_caller(cell["source"])
            export.match_caller(cell["source"])
            main.match_caller(cell["source"])
    output = nb_path.replace("ipynb", "py")
    print("Exporting as {}".format(output))
    export_py(imports, export, main, output)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
          description="A program that takes in a jupyter notebook and outputs a python file"
        ) 
    parser.add_argument("notebook_path")
    args = parser.parse_args()
    parse_json(args.notebook_path)
