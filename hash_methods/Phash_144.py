from .Perception_Hasher import Perception_Hasher
from perception.hashers import PHash


class Phash_144(Perception_Hasher):
    def __init__(self):
        super().__init__(PHash(hash_size=12), "Phash_144")
