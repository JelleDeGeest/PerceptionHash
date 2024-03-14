from abc import ABC, abstractmethod

class HashMethod(ABC):
    @abstractmethod
    def get_similar_images(self, databases: list) -> list:
        pass
