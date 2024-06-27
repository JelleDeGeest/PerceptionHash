from .Perception_Hasher import Perception_Hasher
from perception.hashers import PDQHash


class PDQhash(Perception_Hasher):
    def __init__(self):
        super().__init__(PDQHash(), "PDQhash")