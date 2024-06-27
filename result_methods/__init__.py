from .General_accuracy import General_accuracy
from .Roc import Roc
from .Forced_mistake import Forced_mistake
from .Optimal_threshold import Optimal_threshold

RESULT_METHODS = {
    "general_accuracy": General_accuracy,
    "roc": Roc,
    "forced_mistake": Forced_mistake,
    "optimal_threshold": Optimal_threshold,
}