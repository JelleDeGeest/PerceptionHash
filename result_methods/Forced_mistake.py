import json
import os
import random
from PIL import Image
from hash_methods import RESULT_THRESHOLDS
import numpy as np
from Utilities import *

class Forced_mistake():
    def __init__(self, hash_objects, folders_to_hash, temp, temp2):
        self.hash_objects = hash_objects
        self.folders_to_hash = folders_to_hash
        with open("Settings.json") as file:
            settings = json.load(file)
        self.databases_path = os.path.join(settings["working_directory"], "databases")
        self.input_directories = settings["input_directories"]
        self.amount_of_mistakes = settings["amount_of_forced_mistakes"]
        self.forced_mistakes = {}
        self.random_files = {}
    
    def execute(self, result_folder):
        for folder, folder_path in self.folders_to_hash.items():
            for hash_object in self.hash_objects:
                self.forced_mistakes[hash_object.__class__.__name__] = {}
                self.current_hash_object = hash_object
                self.create_forced_mistake(folder, folder_path, result_folder)

        self.json_dump(result_folder)
    
    def convert_numpy(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert arrays to lists
        elif isinstance(obj, np.generic):
            return obj.item()  # Convert numpy numbers to Python scalars
        elif isinstance(obj, dict):
            return {k: self.convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_numpy(x) for x in obj]
        elif isinstance(obj, tuple):
            return tuple(self.convert_numpy(x) for x in obj)
        else:
            return obj

    def json_dump(self, result_folder):
        # Convert all numpy objects to native Python types
        for key in self.forced_mistakes.keys():
            self.forced_mistakes[key] = self.convert_numpy(self.forced_mistakes[key])

        # Now, `converted_forced_mistakes` is fully compatible with json.dump
        with open(os.path.join(result_folder, "forced_mistakes.json"), 'w') as file:
            json.dump(self.forced_mistakes, file)


    def create_forced_mistake(self, folder, folder_path, result_folder):
        for distortion_folder in os.listdir(folder_path):
            amount_of_mistakes = min(self.amount_of_mistakes, len(os.listdir(folder_path)))
            self.random_files[distortion_folder] = self.random_files[distortion_folder] if distortion_folder in self.random_files else random.sample(os.listdir(os.path.join(folder_path, distortion_folder)), amount_of_mistakes)
            random_files = self.random_files[distortion_folder]
            imgs = {}
            for file in random_files:
                key = file.split("-")[0] + ":" + file.split("-")[1]
                imgs[key] = Image.open(os.path.join(folder_path, distortion_folder, file))
            thresholds = RESULT_THRESHOLDS["forced_mistake"][self.current_hash_object.__class__.__name__]
            similarities = self.current_hash_object.get_similar_images(imgs, thresholds)
            self.generate_results(similarities, folder, distortion_folder, folder_path, result_folder)
    
    def generate_results(self, similarities, folder, distortion, folder_path, result_folder):
        os.makedirs(os.path.join(result_folder, "forced_mistakes"), exist_ok=True)
        for db_and_nr, similarity in similarities.items():
            for threshold, db_dict in sorted(similarity.items(), reverse=True):
                if sum(len(value) for value in db_dict.values()) < 2:
                    continue
                else:
                    self.forced_mistakes[self.current_hash_object.__class__.__name__][db_and_nr.split(":")[0] + "-"+ db_and_nr.split(":")[1]   + "-" + distortion] = (threshold, db_dict)
                    original_found = db_and_nr.split(":")[0] in db_dict.keys() and int(db_and_nr.split(":")[1]) in db_dict[db_and_nr.split(":")[0]]
                    for file in os.listdir(os.path.join(folder_path, distortion)):
                        if int(file.split("-")[1]) == int(db_and_nr.split(":")[1]):
                            string = file
                            break
                    images = [os.path.join(folder_path, distortion, string)]
                    images.append(os.path.join(self.input_directories[folder], db_and_nr.split(":")[1] + ".jpg"))
                    for key, value in db_dict.items():
                        for number in value:
                            if key == db_and_nr.split(":")[0] and number == int(db_and_nr.split(":")[1]):
                                continue
                            images.append(os.path.join(self.input_directories[key], str(number) + ".jpg"))
                    image = create_square_grid_image(images, original_found)
                    image.save(os.path.join(result_folder, "forced_mistakes", db_and_nr.split(":")[0] + "-"+ db_and_nr.split(":")[1] + "-" + distortion + "-" + self.current_hash_object.__class__.__name__ + ".jpg"))
                    break
            



    
    

