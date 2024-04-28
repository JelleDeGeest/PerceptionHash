from .HashMethod import HashMethod
from .Dhash import Dhash
from .Phash import Phash
import os
import json
import copy

class Phash_Dhash(HashMethod):
    def __init__(self):
        self.dhash = Dhash()
        self.phash = Phash()
        self.threshold= 0.8
        self.new_fp = {}

    def get_similar_images(self, images: dict, similarity_thresholds, cache_path=None):
        image_copy = copy.deepcopy(images)
        phash_images = self.phash.get_similar_images(images, similarity_thresholds, cache_path)
        dhash_images = self.dhash.get_similar_images(image_copy,[self.threshold], cache_path)
        # print(vit_images["MetaTestset_1:0"])
        # print(phash_images["MetaTestset_1:0"])
        images = self.combine_dictionaries(phash_images, dhash_images)
        self.find_new_FP(phash_images, dhash_images)

        return images

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

        