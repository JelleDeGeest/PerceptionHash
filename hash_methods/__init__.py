from .Phash import Phash
from .Vit import Vit
from .Phash_Vit import Phash_Vit
from .WaveletHash import WaveletHash
from .Dhash import Dhash
from .Phash_Dhash import Phash_Dhash
import numpy as np

HASH_METHODS = {
    "phash": Phash,
    "vit": Vit,
    "phash_vit": Phash_Vit,
    # "wavelethash": WaveletHash,
    "dhash": Dhash,
    "phash_dhash": Phash_Dhash
}

thresholds = {}

thresholds["general_accuracy"] = {
    "Phash": np.append(np.linspace(0.4,0.8,8,endpoint=False), np.linspace(0.8,1.0, 11)),
    "Vit": [0.9],
    "Phash_Vit": np.append(np.linspace(0.4,0.8,8,endpoint=False), np.linspace(0.8,1.0, 11)),
    "WaveletHash": np.append(np.linspace(0.4,0.8,8,endpoint=False), np.linspace(0.8,1.0, 11)),
    "Dhash": np.append(np.linspace(0.4,0.8,8,endpoint=False), np.linspace(0.8,1.0, 11)),
    "Phash_Dhash": np.append(np.linspace(0.4,0.8,8,endpoint=False), np.linspace(0.8,1.0, 11))
}
thresholds["roc_curve"] = {
    "Phash": [],
    "Vit": np.concatenate((np.linspace(0.8,0.9,9, endpoint=False), np.linspace(0.9,1.0,20))),
    "Phash_Vit": [],
    "WaveletHash": [],
    "Dhash": [],
    "Phash_Dhash": []
}
thresholds["forced_mistake"] = {
    "Phash": [],
    "Vit": np.linspace(0,1.0,100),
    "Phash_Vit": [],
    "WaveletHash": [],
    "Dhash": [],
    "Phash_Dhash": []

}
for i in range(64,0,-1):
    thresholds["roc_curve"]['Phash'].append(i/64)
    thresholds["forced_mistake"]['Phash'].append(i/64)
    thresholds["roc_curve"]['Phash_Vit'].append(i/64)
    thresholds["forced_mistake"]['Phash_Vit'].append(i/64)
    thresholds["roc_curve"]['WaveletHash'].append(i/64)
    thresholds["forced_mistake"]['WaveletHash'].append(i/64)
    thresholds["roc_curve"]['Dhash'].append(i/64)
    thresholds["forced_mistake"]['Dhash'].append(i/64)
    thresholds["roc_curve"]['Phash_Dhash'].append(i/64)
    thresholds["forced_mistake"]['Phash_Dhash'].append(i/64)


RESULT_THRESHOLDS = thresholds

AMOUNT_OF_IMAGES = {
    "Phash": 1000,
    "Vit": 10000,
    "Phash_Vit": 300,
    "WaveletHash": 10000,
    "Dhash": 10000,
    "Phash_Dhash": 300
}


