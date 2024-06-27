from .Perception_Hasher import Perception_Hasher
from perception.hashers import DHash


class Dhash_256(Perception_Hasher):
    def __init__(self):
        super().__init__(DHash(hash_size=16), "Dhash_256")
