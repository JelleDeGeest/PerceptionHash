import json
import numpy as np
from .HashMethod import HashMethod
import os
from tqdm import tqdm
from PIL import Image
from Utilities import extract_number
import time

class Perception_Hasher(HashMethod):
    def __init__(self, hasher, name ):
        # assume databases are pregenerated and stored in a local file
        self.hasher = hasher
        self.name = name
        self.databases = None
        with open("Settings.json") as file:
            settings = json.load(file)
        self.database_path = os.path.join(settings["working_directory"], "databases")
        self.databases_loaded = None
        self.new_fp = {}
        self.cache = None
        self.cache_path = None
    
    def get_similar_images(self, images: dict, cache_path=None):
        
        # time1 = time.time()
        similarities = None
        # Check if a database has been set
        if self.databases is None:
            raise Exception(f"No database set for {self.name}. Use set_database() to set a database.")
        
        hasher = self.hasher
        if cache_path is not None and cache_path != self.cache_path:
            with open(os.path.join(cache_path, f"{self.name}.json")) as f:
                temp = json.load(f)
                self.cache_path = cache_path
                self.cache = self.hashes_to_matrix(temp, self.hasher)

        # Load the databases if they haven't been loaded yet
        if self.databases_loaded is None:
            self.databases_loaded = {}
            for database in self.databases:
                with open(os.path.join(self.database_path, database, self.name, "0.json"), 'r') as file:
                    db = json.load(file)
                self.databases_loaded[database] = self.hashes_to_matrix(db, hasher)

        if cache_path is not None:
            for key, value in images.items():
                hashes = self.cache[value.min():(value.max()+1)]
                similarities = 1 - self.find_similar_images(hashes, self.databases_loaded[self.databases[0]])
            
            # hashes =  self.cache[]

        # else:
        #     for key in images.keys():
        #         image_hash = hasher.compute(images[key])
        #         similarities = {}
        #         for threshold in similarity_thresholds:
        #             similarities[threshold] = {}
        #         for db_name, db_matrix in self.databases_loaded.items():
        #             temp = self.find_similar_images(image_hash, db_matrix, similarity_thresholds, hasher)
        #             for threshold, value in temp.items():
        #                 if len(value) > 0:
        #                     similarities[threshold][db_name] = value
        #         images[key] = similarities
        
        # time2 = time.time()
        # print(f"Time taken for Similarity: {time2-time1} seconds")

        return similarities.astype(np.float64)
    
    def find_optimal_threshold(self, images: dict, cache_path=None):
        return[self.get_similar_images(images, cache_path)]

    def hashes_to_matrix(self, hashes, hasher):
        # Convert hash strings to binary matrix
        bin_hashes = [hasher.string_to_vector(hash_str, hash_format="base64") for hash_str in hashes]
        matrix = np.array([[int(bit) for bit in hash_str] for hash_str in bin_hashes], dtype=np.int8)
        return matrix
    
    def find_similar_images(self, hash_matrix, db_matrix):
        pairwise_abs_diff = np.abs(hash_matrix[:, np.newaxis, :] - db_matrix)
        if self.name in ["PDQhash", "Phash_256", "Dhash_256"]:
            distances = np.sum(pairwise_abs_diff, axis=2) / 256
        elif self.name in ["Dhash_144", "Phash_144"]:
            distances = np.sum(pairwise_abs_diff, axis=2) / 144
        else:
            distances = np.sum(pairwise_abs_diff, axis=2) / 64
        return distances

    def set_database(self, database):
        self.databases = database

    def database_generation(self, images_path, database_path):
        hasher = self.hasher
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
            # Open the image using PIL and calculate its hash
            with Image.open(file_path) as img:
                img_hash = hasher.compute(img)
                hashes.append(str(img_hash))

        # Write the hashes to the output file in JSON format
        database_partition = 0  # Ensure you provide a filename here, e.g., "output.json"
        with open(os.path.join(database_path, str(database_partition)+".json"), 'w') as f:
            json.dump(hashes, f)

        print(f"Hashes written to {os.path.join(database_path, str(database_partition)+'.json')}")
    
    def cache_generation(self, images_path, output_path, lenght=-1):
        # check if cache already exists
        if os.path.exists(output_path + f"/{self.name}.json"):
            print(f"Cache already exists for {output_path + '/' +self.name + '.json'}")
            return


        hasher = self.hasher
        hashes = []

        # Check if all files have same file extension
        file_extensions = set()
        for file in os.listdir(images_path):
            file_extensions.add(os.path.splitext(file)[1])
        if len(file_extensions) > 1:
            raise Exception("All files must have the same file extension")
        extension = file_extensions.pop()

        files = sorted(os.listdir(images_path), key=lambda file: extract_number(file, ".*" + "-", "-" + ".*", ""))
        

        # Loop through each file in alphabetical order
        for filename in tqdm(files):
            if filename.endswith(extension):  # Ensure we're only working with files of a specific type
                file_path = os.path.join(images_path, filename)
                # Open the image and calculate its hash
                with Image.open(file_path) as img:
                    img_hash = hasher.compute(img)
                    hashes.append(str(img_hash))
                if len(hashes) == lenght:
                   break

        # Write the hashes to the output file in JSON format
        with open(output_path + f"/{self.name}.json", 'w') as f:
            json.dump(hashes, f)
