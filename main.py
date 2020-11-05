import json
import os
import pathlib
import sys
from json import JSONEncoder

import numpy as np
from PIL import Image


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def main():
    print("Generating font output")

    font = {}

    path = str(pathlib.Path(__file__).parent.absolute()) + "/font/"
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            in_img = Image.open(path + filename)
            in_array = np.array(in_img)
            in_array_boolean = in_array[:, :, 0] > 0
            in_array_inverted = np.invert(in_array_boolean)
            
            separated = filename.split(".")
            font[separated[0]] = in_array_inverted
        else:
            print(f"Skipping non-image file: {filename}")
            continue

    with open("font.json", "w") as write_file:
        json.dump(font, write_file, cls=NumpyArrayEncoder)

    print("Finished creating font in font.json")


if __name__ == "__main__":
    main()
