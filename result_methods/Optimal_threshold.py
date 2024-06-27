import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import json
from tqdm import tqdm
from hash_methods import RESULT_THRESHOLDS, AMOUNT_OF_IMAGES, AMOUNT_OF_THREADS
import time
from Utilities import extract_number
import concurrent.futures
import copy



class Optimal_threshold():
    def __init__(self, hash_objects, folders_to_hash, cache, distortion_techniques):
        self.hash_objects = hash_objects
        self.folders_to_hash = folders_to_hash
        self.distortion_techniques = distortion_techniques
        with open("Settings.json") as file:
            settings = json.load(file)
        self.distortion_name_dict = settings["distortion_name_dict"]
        self.databases_path = os.path.join(settings["working_directory"], "databases")
        self.cache = cache
        if self.cache:
            self.cache_name_dict = settings["cache_name_dict"]
            self.load_cache(os.path.join(settings["working_directory"], "cache"))

    def execute(self, result_folder):
        self.result_folder = result_folder
        total = sum(len(os.listdir(folder_path)) for folder_path in self.folders_to_hash.values())
        results = {}
        for folder, folder_path in self.folders_to_hash.items():
            for hash_object in self.hash_objects:
                threads = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=AMOUNT_OF_THREADS[hash_object.__class__.__name__]) as executor:
                    for distortion_folder in os.listdir(folder_path):
                        # check if the distortion folder is in the list of distortion techniques
                        if len(self.distortion_techniques) != 0 and distortion_folder not in self.distortion_techniques:
                            continue
                        
                        # check if the distortion folder is in the list of distortion techniques
                        if distortion_folder not in results:
                            results[distortion_folder] = {}

                        # self.current_hash_object = hash_object
                        thresholds = RESULT_THRESHOLDS["optimal_threshold"][hash_object.__class__.__name__]
                        threads.append([distortion_folder,hash_object.__class__.__name__, executor.submit(self.get_rates, thresholds, folder, os.path.join(folder_path, distortion_folder), distortion_folder, copy.deepcopy(hash_object))])
                        print(f"Thread created for {folder} with {distortion_folder} with {hash_object.__class__.__name__}")
                 
                    for thread in threads:
                        rates = thread[2].result()
                        if thread[1] not in results[thread[0]]:
                            results[thread[0]][thread[1]] = rates
                        else:  
                            results[thread[0]][thread[1]] = self.combine_results(results[thread[0]][thread[1]], rates)

        # cache result in result folder
        converted_results = self.convert_for_json(results)
        with open(os.path.join(result_folder, "optimal_thresholds_values.json"), 'w') as file:
            json.dump(converted_results, file)

        # calculate accuracy_scores
        self.calculate_accuracy_scores(results, result_folder)

    def calculate_accuracy_scores(self, results, result_folder):
        accuracy_scores = {}
        for distortion, values in results.items():
            accuracy_scores[distortion] = {}
            for hash_object, values2 in values.items():
                accuracy_scores[distortion][hash_object] = {}
                for threshold, values3 in values2.items():
                    accuracy_scores[distortion][hash_object][threshold] = {}
                    tp = values3[0]
                    fp = values3[1]
                    tn = values3[2]
                    fn = values3[3]
                    # calculate metrics but make sure there are no 0 divisions
                    accuracy = (tp + tn) / (tp + fp + tn + fn) if tp + fp + tn + fn != 0 else 0
                    precision = tp / (tp + fp) if tp + fp != 0 else 0
                    recall = tp / (tp + fn) if tp + fn != 0 else 0
                    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall != 0 else 0
                
                    accuracy_scores[distortion][hash_object][threshold] = {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}
        
        with open(os.path.join(result_folder, "optimal_thresholds_metrics.json"), 'w') as file:
            json.dump(self.convert_for_json(accuracy_scores), file)

        best_thresholds = {}
        for distortion, values in accuracy_scores.items():
            best_thresholds[distortion] = {}
            for hash_object, values2 in values.items():
                best_thresholds[distortion][hash_object] = {}
                for metric in ["accuracy", "precision", "recall", "f1"]:
                    best_thresholds[distortion][hash_object][metric] = []
                    max_value = -float("inf")
                    for threshold, values3 in values2.items():
                        current_value = values3[metric]
                        if current_value > max_value:
                            max_value = current_value
                            best_thresholds[distortion][hash_object][metric] = [(threshold, current_value)]
                        elif current_value == max_value:
                            best_thresholds[distortion][hash_object][metric].append((threshold, current_value))

        
        with open(os.path.join(result_folder, "optimal_thresholds.json"), 'w') as file:
            json.dump(self.convert_for_json(best_thresholds), file)

            
        

                    
            

    def get_rates(self, thresholds, folder, folder_path, distortion, current_hash_object):
        # This method should return true positives, false positives, true negatives, and false negatives
        # based on the threshold. You'll need to modify this method to fit your hashing method and data structure.
        # This is a placeholder example.
        # tp, fp, tn, fn = 0, 0, 0, 0
        self.false_positives = {}
        current_hash_object.new_fp = {}
        current_hash_object.new_fn = {}
        
        current_score = {}
        for threshold in thresholds:
            current_score[threshold] = [0, 0, 0, 0]
        if AMOUNT_OF_IMAGES[current_hash_object.__class__.__name__] == -1:
            total = len(os.listdir(folder_path))
        else:
            total = AMOUNT_OF_IMAGES[current_hash_object.__class__.__name__]
        # progress_bar = tqdm(total=total, leave=False)
        # progress_bar.set_description(f"ROC Curve: {folder} with {distortion} with {current_hash_object.__class__.__name__}")
        imgs = {}
        should_be_found = folder in os.listdir(self.databases_path)
        file_list = sorted(os.listdir(folder_path), key=lambda file: extract_number(file, ".*" + "-", "-" + self.distortion_name_dict[distortion.split('-')[0]], ".*"))

        counter = AMOUNT_OF_IMAGES[current_hash_object.__class__.__name__]
        if not self.cache:
            
            for file in file_list:
                # progress_bar.update(1)
                key = file.split("-")[0]
                if key not in imgs.keys():
                    imgs[key] = []
                imgs[key].append(int(extract_number(file)))
                if len(imgs.keys()) == 100:
                    for key, value in imgs.items():
                        imgs[key] = np.array(value)
                    similarities = current_hash_object.find_optimal_threshold(imgs, thresholds, output_folder=self.result_folder )
                    current_score = self.get_accuracies(similarities, should_be_found, current_score, current_hash_object)
                    imgs = {}
                if counter == 1:
                    break
                counter -= 1
            if(len(imgs.keys()) > 0):
                similarities = current_hash_object.find_optimal_threshold(imgs, thresholds)
                current_score = self.get_accuracies(similarities, should_be_found, current_score, current_hash_object)

        if self.cache:
            cache_path = self.cache_dict[folder][distortion]
            for file in tqdm(file_list, desc=f"{folder} with {distortion}"):
                # print(file_list)
                # print(distortion)
                # progress_bar.update(1)
                key = file.split("-")[0]
                if key not in imgs.keys():
                    imgs[key] = []
                    
                imgs[key].append(int(extract_number(file, key + "-", "-" + self.distortion_name_dict[distortion.split('-')[0]], ".*")))
                if len(imgs[key]) == 100:
                    for key, value in imgs.items():
                        imgs[key] = np.array(value)
                    similarities = current_hash_object.find_optimal_threshold(imgs, cache_path)
                    current_score = self.get_accuracies(imgs, similarities, thresholds, should_be_found, current_score, current_hash_object)
                    imgs = {}
                if counter == 1:
                    break
                counter -= 1
            if len(imgs.keys()) > 0:
                for key, value in imgs.items():
                    imgs[key] = np.array(value)
                similarities = current_hash_object.find_optimal_threshold(imgs, cache_path)
                current_score = self.get_accuracies(imgs, similarities, thresholds, should_be_found, current_score, current_hash_object)


        with open(os.path.join(self.result_folder, "new_false_positives.txt"), "a") as file:
            file.write(f"New false negatives found for {folder} with {distortion} with {current_hash_object.__class__.__name__} \n")
            file.write(json.dumps(current_hash_object.new_fp))
            file.write("\n")

        with open(os.path.join(self.result_folder, "new_false_negatives.txt"), "a") as file:
            file.write(f"New false negatives found for {folder} with {distortion} with {current_hash_object.__class__.__name__} \n")
            file.write(json.dumps(current_hash_object.new_fn))
            file.write("\n")
        
        # with open(os.path.join(self.result_folder, "false_postives.txt"), "a") as file:
        #     file.write(f"False positives found for {folder} with {distortion} with {current_hash_object.__class__.__name__} \n")
        #     file.write(json.dumps(self.false_positives))
        #     file.write("\n") 


        # progress_bar.close()
        # Logic to calculate tp, fp, tn, fn goes here
        return current_score
    
    def get_accuracies(self, imgs, similarities, thresholds,  should_be_found, current_score, current_hash_object):
        if should_be_found:
            temp = "MetaTestset_1"
        else:
            temp = "MetaTestset_2"
        # print(thresholds)
        # print(imgs)
        # exit()
        # print(similarities)
        # print(imgs)
        # time1 = time.time()
        # print the size similarities takes in memory
        for db, nrs in imgs.items():
            for threshold in thresholds:
                # check if the originals are found
                # current_mask = similarities >= threshold
                current_mask = None
                # check if threshold is a tuple
                if not isinstance(threshold, tuple):
                    current_mask = similarities[0] >= threshold
                else:
                    for i, temp in enumerate(threshold):
                        if i == 0:
                            current_mask = similarities[i] >= temp
                        else:
                            current_mask = np.logical_and(current_mask, similarities[i] >= temp)

                
                for i, nr in enumerate(nrs):
                    # print( similarities[i, nr])
                    # print( threshold)
                    if should_be_found:
                        # check if the original is found
                        if current_mask[i, nr]:
                            current_score[threshold][1] -= 1 
                            current_score[threshold][0] += 1
                        else:
                            current_score[threshold][3] += 1
                            current_hash_object.new_fn[f"{temp}:{imgs[db][i]}"] = f"{temp}:{imgs[db][i]}"
                    else:
                        # check if no match is found in the entire row
                        if not np.any(current_mask[i]):
                            current_score[threshold][2] += 1

                # check if the false positives are found

                current_score[threshold][1] += int(np.sum(current_mask))

                coords = list(np.argwhere(current_mask))
                for coord1, coord2 in coords:
                    if imgs[db][coord1] != coord2:
                        current_hash_object.new_fp[f"{temp}:{imgs[db][coord1]}"] = f"{temp}:{coord2}"


        # time2 = time.time()
        # print(f"Time taken for getting accuracies: {time2-time1}")
        return current_score

    def load_cache(self, cache_folder):
        self.cache_dict = {}
        for folder in os.listdir(cache_folder):
            self.cache_dict[folder] = {}
            for distortion in os.listdir(os.path.join(cache_folder, folder)):
                for hash_object in self.hash_objects:
                        self.cache_dict[folder][distortion] = cache_folder + "/" + folder + "/" + distortion



    def combine_results(self, result1, result2):
        result = {}
        for key in result1.keys():
            result[key] = [result1[key][0] + result2[key][0], result1[key][1] + result2[key][1], result1[key][2] + result2[key][2], result1[key][3] + result2[key][3]]
        return result

    def convert_for_json(self, data):
        if isinstance(data, dict):
            return {str(k): self.convert_for_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_for_json(item) for item in data]
        elif isinstance(data, np.int32):
            return int(data)
        else:
            return data