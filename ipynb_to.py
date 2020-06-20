import json
import argparse


def parse_json(nb_path):
    # Read notebook
    with open(nb_path) as f:
        nb = json.load(f)
    
    # Parse nb source
    imports = []
    export = []
    for cell in nb["cells"]:
        if cell["source"]: 
            if "#imports" in cell["source"] or "#imports\n" in cell["source"]:
                imports.append(cell["source"])
            if "#export\n" in cell["source"] or "#export" in cell["source"]:
                export.append(cell["source"])
    output = nb_path.replace("ipynb", "py")
    print("Exporting as {}".format(output))
    with open(output, "w+") as f:
        for cell in imports:
            for line in cell:
                if not line.startswith("#import"):
                    f.write(line)
            f.write("\n")
        f.write("\n")
        for cell in export:
            for line in cell:
                if not line.startswith("#export"):
                    f.write(line)
            f.write("\n") 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
          description = "A program that takes in a jupyter notebook and outputs a python file"
        ) 
    parser.add_argument("notebook_path")
    args = parser.parse_args()
    parse_json(args.notebook_path)
    
