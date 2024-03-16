from .General_accuracy import General_accuracy
from .Roc import Roc

RESULT_METHODS = {
    "general_accuracy": General_accuracy,
    "roc": Roc
}