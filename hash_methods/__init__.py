from .Phash import Phash
from .Vit import Vit
from .Phash_Vit import Phash_Vit
from .Dhash import Dhash
from .Phash_Dhash import Phash_Dhash
from .PDQ_Hash import PDQhash
from .Phash_256 import Phash_256
from .Dhash_256 import Dhash_256
from .Phash_144 import Phash_144
from .Dhash_144 import Dhash_144
from .Dhash_Vit import Dhash_Vit
from .Dhash144_Vit import Dhash144_Vit
from .Phash144_Vit import Phash144_Vit
from .Phash144_Dhash144 import Phash144_Dhash144
import numpy as np
import itertools

def combinations(*args):
    return tuple(itertools.product(*args))


HASH_METHODS = {
    "phash": Phash,
    "vit": Vit,
    "phash_vit": Phash_Vit,
    "pdqhash": PDQhash,
    "dhash": Dhash,
    "phash_dhash": Phash_Dhash,
    "phash_256": Phash_256,
    "dhash_256": Dhash_256,
    "phash_144": Phash_144,
    "dhash_144": Dhash_144,
    "dhash_vit": Dhash_Vit,
    "dhash144_vit": Dhash144_Vit,
    "phash144_vit": Phash144_Vit,
    "phash144_dhash144": Phash144_Dhash144
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




# thresholds["optimal_threshold"] = {
#     # "Phash": [element for element in thresholds["roc_curve"]['Phash'] if element > 0.6],
#     "Phash": [0, 0.3, 0.5, 0.6, 0.7, 0.8] + list(np.linspace(0.9,1.0,11, endpoint=True)),
#     "PDQhash": [element for element in thresholds["roc_curve"]['Phash'] if element > 0.6],
#     "Vit": [0, 0.3] + list(np.linspace(0.6,1.0,10, endpoint=True)),
#     # "Vit": np.linspace(0,0.7,8, endpoint=True),
#     "Phash_Vit": "",
#     "Dhash": [0, 0.3, 0.5, 0.6, 0.7, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.925] + list(np.linspace(0.94,1.0,7, endpoint=True)),
#     "Phash_Dhash": "",
#     "Phash_256": [element for element in thresholds["roc_curve"]['Phash'] if element > 0.6],
#     "Dhash_256": [element for element in thresholds["roc_curve"]['Phash'] if element > 0.6],
#     "Phash_144": [0, 0.3,0.6, 0.7, 0.8] + list(np.linspace(0.85,0.95,11, endpoint=True)) + [1.0],
#     "Dhash_144": [0, 0.3,0.6, 0.7, 0.8] + list(np.linspace(0.9,1.0,11, endpoint=True)),
    


# }
# thresholds["optimal_threshold"]["Phash_Vit"] = combinations(thresholds["optimal_threshold"]["Phash"], thresholds["optimal_threshold"]["Vit"])
# thresholds["optimal_threshold"]["Phash_Dhash"] = combinations(thresholds["optimal_threshold"]["Phash"], thresholds["optimal_threshold"]["Dhash"])
# thresholds["optimal_threshold"]["Dhash_Vit"] = combinations(thresholds["optimal_threshold"]["Dhash"], thresholds["optimal_threshold"]["Vit"])
# thresholds["optimal_threshold"]["Dhash144_Vit"] = combinations(thresholds["optimal_threshold"]["Dhash_144"], thresholds["optimal_threshold"]["Vit"])
# thresholds["optimal_threshold"]["Phash144_Vit"] = combinations(thresholds["optimal_threshold"]["Phash_144"], thresholds["optimal_threshold"]["Vit"])
# thresholds["optimal_threshold"]["Phash144_Dhash144"] = combinations(thresholds["optimal_threshold"]["Phash_144"], thresholds["optimal_threshold"]["Dhash_144"])


thresholds["optimal_threshold"] = {
    "Phash": [0.922],
    "PDQhash": [0.812],
    "Vit": [0.945],
    "Dhash": [0.969],
    "Phash_256": [0.875],
    "Dhash_256": [0.922],
    "Phash_144": [0.906],
    "Dhash_144": [0.938],
    


}
thresholds["optimal_threshold"]["Phash_Vit"] = [(0.910,0.3)]
thresholds["optimal_threshold"]["Phash_Dhash"] = [(0.922,0.812)]
thresholds["optimal_threshold"]["Dhash_Vit"] = [(0.925,0.822)]
thresholds["optimal_threshold"]["Dhash144_Vit"] = [(0.920,0.778)]
thresholds["optimal_threshold"]["Phash144_Vit"] = [(0.910,0)]
thresholds["optimal_threshold"]["Phash144_Dhash144"] = [(0.910,0.700)]

print( thresholds["optimal_threshold"]["Dhash144_Vit"])

RESULT_THRESHOLDS = thresholds

AMOUNT_OF_IMAGES = {
    "Phash": 50000,
    "Vit": 50000,
    "Phash_Vit": 50000,
    "Dhash": 50000,
    "Phash_Dhash": 50000,
    "PDQhash": 50000,
    "Phash_256": 50000,
    "Dhash_256": 50000,
    "Phash_144": 50000,
    "Dhash_144": 50000,
    "Dhash_Vit": 50000,
    "Dhash144_Vit": 50000,
    "Phash144_Vit": 50000,
    "Phash144_Dhash144": 50000 
}

# AMOUNT_OF_IMAGES = {
#     "Phash": 100,
#     "Vit": 100,
#     "Phash_Vit": 100,
#     "WaveletHash": 100,
#     "Dhash": 100,
#     "Phash_Dhash": 100,
#     "PDQhash": 100,
#     "Phash_256": 100,
#     "Dhash_256": 100,
#     "Phash_144": 100,
#     "Dhash_144": 100,
#     "Dhash_Vit": 100,
#     "Dhash144_Vit": 100,
#     "Phash144_Vit": 100,
#     "Phash144_Dhash144": 100 
# }

AMOUNT_OF_THREADS = {
    "Phash": None,
    "Vit": 8,
    "Phash_Vit": None,
    "Dhash": None,
    "Phash_Dhash": None,
    "PDQhash": None,
    "Phash_256": None,
    "Dhash_256": None,
    "Phash_144": None,
    "Dhash_144": None,
    "Dhash_Vit": None,
    "Dhash144_Vit": None,
    "Phash144_Vit": None,
    "Phash144_Dhash144": None,
}


