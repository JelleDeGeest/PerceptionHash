from perception.hashers import PHash
import json
import numpy as np
import os
from tqdm import tqdm
from PIL import Image

hasher = PHash()
image = Image.open("D:/thesisdata\Included/1/2.jpg")
hash = hasher.compute(image)
print(hash)
