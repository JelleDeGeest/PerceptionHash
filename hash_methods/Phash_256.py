from .Perception_Hasher import Perception_Hasher
from perception.hashers import PHash


class Phash_256(Perception_Hasher):
    def __init__(self):
        super().__init__(PHash(hash_size=16), "Phash_256")
