import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import json
from tqdm import tqdm
from hash_methods import RESULT_THRESHOLDS, AMOUNT_OF_IMAGES


class ROC_Curve():
    def __init__(self, hash_objects, folders_to_hash):
        self.hash_objects = hash_objects
        self.folders_to_hash = folders_to_hash
        with open("Settings.json") as file:
            settings = json.load(file)
        self.databases_path = os.path.join(settings["working_directory"], "databases")

    def execute(self, result_folder):
        total = sum(len(os.listdir(folder_path)) for folder_path in self.folders_to_hash.values())
        progress_bar_distortion = tqdm(total=total, leave=False)
        for folder, folder_path in self.folders_to_hash.items():
            for distortion_folder in os.listdir(folder_path):
                progress_bar_distortion.set_description(f"ROC Curve: {folder} with {distortion_folder}")
                results = {}
                progress_bar_hash_objects = tqdm(total=len(self.hash_objects), leave= False)
                for hash_object in self.hash_objects:
                    self.current_hash_object = hash_object
                    progress_bar_hash_objects.set_description(f"ROC Curve: {folder} with {distortion_folder} with {hash_object.__class__.__name__}")
                    thresholds = RESULT_THRESHOLDS["roc_curve"][hash_object.__class__.__name__]
                    results[hash_object.__class__.__name__] = {}
                    progress_bar_thresholds = tqdm(total=len(thresholds), leave= False)
                    for threshold in thresholds:
                        progress_bar_thresholds.set_description(f"ROC Curve: {folder} with {distortion_folder} with {hash_object.__class__.__name__} at similarity {threshold}")
                        results[hash_object.__class__.__name__][threshold] = self.get_rates(threshold, folder, os.path.join(folder_path, distortion_folder))
                        progress_bar_thresholds.update(1)
                    progress_bar_hash_objects.update(1)
                progress_bar_distortion.update(1)
        # cache result in result folder
        with open(os.path.join(result_folder, "roc_curve.json"), 'w') as file:
            json.dump(results, file)
        # generate graphs
        self.generate_graphs(results, result_folder)

    def get_rates(self, threshold, folder, folder_path, distortion):
        # This method should return true positives, false positives, true negatives, and false negatives
        # based on the threshold. You'll need to modify this method to fit your hashing method and data structure.
        # This is a placeholder example.
        tp, fp, tn, fn = 0, 0, 0, 0
        total = len(os.listdir(os.folder_path))
        progress_bar = 


        
        # Logic to calculate tp, fp, tn, fn goes here
        return [tp, fp, tn, fn]
    
    def get_accuracies(self,similarities, should_be_found):
        pass

    def generate_graphs(self, results, result_folder):
        pass
