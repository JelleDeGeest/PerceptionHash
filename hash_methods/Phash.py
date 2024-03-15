from perception.hashers import PHash
import json
import numpy as np
from .HashMethod import HashMethod
import os
from tqdm import tqdm
from PIL import Image


class Phash(HashMethod):
    def __init__(self):
        # assume databases are pregenerated and stored in a local file
        self.databases = None
        thresholds = []
        for i in range(64,0,-1):
            thresholds.append(i/64)
        self.roc_thresholds = thresholds
        self.general_accuracy_thresholds = np.arange(0.5, 1, 0.05)
        self.name = "Phash"
    
    def get_similar_images(self, images, similarity_threshold):
        if self.databases is None:
            raise Exception("No database set for Phash. Use set_database() to set a database.")
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

    def set_database(self, database):
        self.databases = database

    def database_generation(self, images_path, database_path):
        hasher = PHash()
        hashes = []

        # Check if all files have same file extension
        file_extensions = set()
        for file in os.listdir(images_path):
            file_extensions.add(os.path.splitext(file)[1])
        if len(file_extensions) > 1:
            raise Exception("All files must have the same file extension")
        extension = file_extensions.pop()

        # Loop through all files in the folder and display progress bar
        for index in tqdm(range(len(os.listdir(images_path)))):
            file_path = os.path.join(images_path, str(index)+extension)
            # Open the image using PIL and calculate its pHash
            with Image.open(file_path) as img:
                img_hash = hasher.compute(img)
                hashes.append(str(img_hash))

        # Write the hashes to the output file in JSON format
        database_partition = 0  # Ensure you provide a filename here, e.g., "output.json"
        with open(os.path.join(database_path, str(database_partition)+".json"), 'w') as f:
            json.dump(hashes, f)

        print(f"Hashes written to {os.path.join(database_path, str(database_partition)+'.json')}")

        
