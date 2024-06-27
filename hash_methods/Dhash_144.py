from .Perception_Hasher import Perception_Hasher
from perception.hashers import DHash


class Dhash_144(Perception_Hasher):
    def __init__(self):
        super().__init__(DHash(hash_size=12), "Dhash_144")
