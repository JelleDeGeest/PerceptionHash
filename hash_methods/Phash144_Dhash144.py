from .HashMethod import HashMethod
from .Dhash_144 import Dhash_144
from .Phash_144 import Phash_144
import os
import json
import copy
import time

class Phash144_Dhash144(HashMethod):
    def __init__(self):
        self.dhash = Dhash_144()
        self.phash = Phash_144()
        self.threshold= 0.8
        self.new_fp = {}

    def get_similar_images(self, images: dict, cache_path=None):
        phash_similarities = self.phash.get_similar_images(images, cache_path)
        dhash_similarities = self.dhash.get_similar_images(images, cache_path)
        mask = dhash_similarities < self.threshold
        phash_similarities[mask] = 0
        return phash_similarities
    
    def find_optimal_threshold(self, images: dict, cache_path=None):
        # time1 = time.time()
        phash_similarities = self.phash.get_similar_images(images, cache_path)
        dhash_similarities = self.dhash.get_similar_images(images, cache_path)
        # time2 = time.time()
        # print(f"Time taken for {images}: {time2-time1:.2f} seconds")
        return[phash_similarities, dhash_similarities]
        

    def set_database(self, database):
        self.dhash.set_database(database)
        self.phash.set_database(database)
    
    def database_generation(self, images_path, database_path):
        print("No database needed for Phash_Vit. Database generation is done by the individual hash methods.")
        pass

    def combine_dictionaries(self, phash_dict, vit_dict):
        combined = {}
        # Iterate through the keys in the first dictionary
        for key in phash_dict:
            if key in vit_dict:
                combined[key] = {}
                # Iterate through the sub-keys (thresholds)
                for threshold in phash_dict[key]:
                    combined[key][threshold] = {}
                    # Iterate through the db_names
                    for db_name in phash_dict[key][threshold]:
                        if db_name in vit_dict[key][self.threshold]:
                            # Use set intersection to find common elements
                            set1 = set(phash_dict[key][threshold][db_name])
                            set2 = set(vit_dict[key][self.threshold][db_name])
                            common_elements = list(set1 & set2)
                            # Store common elements, or an empty list if none
                            if len(common_elements) > 0:
                                combined[key][threshold][db_name] = common_elements
        return combined

    def find_new_FP(self, phash_dict, vit_dict):
        new_fps = {}
        for key, value in phash_dict.items():
            for threshold, value2 in value.items():
                if key.split(":")[0] in value2.keys():
                    if int(key.split(":")[1]) in value2[key.split(":")[0]]:
                        if threshold not in new_fps.keys():
                            new_fps[threshold] = [key]
                        else:
                            new_fps[threshold].append(key)

        new_fps_2 = {}
        for key, value in vit_dict.items():
            for threshold, value2 in value.items():
                if key.split(":")[0] in value2.keys():
                    if int(key.split(":")[1]) in value2[key.split(":")[0]]:
                        if threshold not in new_fps_2.keys():
                            new_fps_2[threshold] = [key]
                        else:
                            new_fps_2[threshold].append(key)

        # check for keys that are in 1 but not in 2
        for key, value in new_fps.items():
            temp = new_fps_2[self.threshold]
            set1 = set(value)
            set2 = set(temp)
            common_elements = list(set1 - set2)
            if len(common_elements) > 0:
                if key not in self.new_fp.keys():
                    self.new_fp[key] = common_elements
                else:
                    self.new_fp[key] += common_elements

        