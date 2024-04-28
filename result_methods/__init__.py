from .General_accuracy import General_accuracy
from .Roc import Roc
from .Forced_mistake import Forced_mistake

RESULT_METHODS = {
    "general_accuracy": General_accuracy,
    "roc": Roc,
    "forced_mistake": Forced_mistake
}