from .Perception_Hasher import Perception_Hasher
from perception.hashers import WaveletHash


class WaveletHash(Perception_Hasher):
    def __init__(self):
        super().__init__(WaveletHash(), "WaveletHash")
