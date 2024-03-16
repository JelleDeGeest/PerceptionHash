from .Phash import Phash
from .Vit import Vit


HASH_METHODS = {
    "phash": Phash,
    "vit": Vit
}

thresholds = {}
thresholds["general_accuracy"] = {
    "Phash": [0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.0],
    "Vit": [0.9]
}
thresholds["roc_curve"] = {
    "Phash": [0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.0],
    "Vit": [0.9]
}
RESULT_THRESHOLDS = thresholds

AMOUNT_OF_IMAGES = {
    "Phash": 1000,
    "Vit": 100
}


