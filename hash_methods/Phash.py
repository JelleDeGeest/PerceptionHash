from perception.hashers import PHash
import json
import numpy as np
from hash_method import HashMethod


class Phash(HashMethod):
    def __init__(self, databases):
        # assume databases are pregenerated and stored in a local file
        self.databases = databases

        thresholds = []
        for i in range(64,0,-1):
            thresholds.append(i/64)
        self.roc_thresholds = thresholds
        self.general_accuracy_thresholds = np.arange(0.5, 1, 0.05)
    
    def get_similar_images(self, images, similarity_threshold):
        with open(self.databases, 'r') as file:
            db = json.load(file)
        hasher = PHash()
        db_matrix = self.hashes_to_matrix(db, hasher)
        similarities = []
        for image in images:
            image_hash = hasher.compute(image)
            similarities.append(self.find_similar_images(image_hash, db_matrix, similarity_threshold, hasher))
        return similarities
    
    def hashes_to_matrix(self, hashes, hasher):
        # Convert hash strings to binary matrix
        bin_hashes = [hasher.string_to_vector(hash_str, hash_format="base64") for hash_str in hashes]
        matrix = np.array([[int(bit) for bit in hash_str] for hash_str in bin_hashes], dtype=np.int8)
        return matrix
    
    def find_similar_images(self,new_image_hash, db_matrix, threshold, hasher):
        new_image_vector = hasher.string_to_vector(new_image_hash, hash_format="base64")
        distances = np.sum(np.abs(db_matrix - new_image_vector), axis=1) / 64
        similar_indices = np.where(distances <= threshold)[0]
        return similar_indices
    
    def get_roc_thresholds(self):
        return self.get_roc_thresholds
    
    def get_general_accuracy_thresholds(self):
        return self.general_accuracy_thresholds
