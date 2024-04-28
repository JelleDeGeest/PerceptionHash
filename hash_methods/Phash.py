from .Perception_Hasher import Perception_Hasher
from perception.hashers import PHash


class Phash(Perception_Hasher):
    def __init__(self):
        super().__init__(PHash(), "Phash")
