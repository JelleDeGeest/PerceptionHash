import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import json
from tqdm import tqdm
from hash_methods import RESULT_THRESHOLDS, AMOUNT_OF_IMAGES
import time
from Utilities import extract_number


class Roc():
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
            for distortion_folder in os.listdir(folder_path):

                # check if the distortion folder is in the list of distortion techniques
                if distortion_folder is not None and distortion_folder not in self.distortion_techniques:
                    continue
                
                # check if the distortion folder is in the list of distortion techniques
                if distortion_folder not in results:
                    results[distortion_folder] = {}

                # create a task for each hash object
                for hash_object in self.hash_objects:
                    self.current_hash_object = hash_object
                    thresholds = RESULT_THRESHOLDS["roc_curve"][hash_object.__class__.__name__]
                    if hash_object.__class__.__name__ not in results[distortion_folder]:
                        results[distortion_folder][hash_object.__class__.__name__] = self.get_rates(thresholds, folder, os.path.join(folder_path, distortion_folder), distortion_folder)
                    else:  
                        results[distortion_folder][hash_object.__class__.__name__] = self.combine_results(results[distortion_folder][hash_object.__class__.__name__], self.get_rates(thresholds, folder, os.path.join(folder_path, distortion_folder), distortion_folder))
            



        # cache result in result folder
        with open(os.path.join(result_folder, "roc_curve.json"), 'w') as file:
            json.dump(self.convert(results), file)

        # generate graphs
        self.generate_graphs(results, result_folder)
        
        # generate auc
        self.generate_auc(results, result_folder)
            

    def get_rates(self, thresholds, folder, folder_path, distortion):
        # This method should return true positives, false positives, true negatives, and false negatives
        # based on the threshold. You'll need to modify this method to fit your hashing method and data structure.
        # This is a placeholder example.
        # tp, fp, tn, fn = 0, 0, 0, 0
        self.false_positives = {}
        current_score = {}
        for threshold in thresholds:
            current_score[threshold] = [0, 0, 0, 0]
        if AMOUNT_OF_IMAGES[self.current_hash_object.__class__.__name__] == -1:
            total = len(os.listdir(folder_path))
        else:
            total = AMOUNT_OF_IMAGES[self.current_hash_object.__class__.__name__]
        progress_bar = tqdm(total=total, leave=False)
        progress_bar.set_description(f"ROC Curve: {folder} with {distortion} with {self.current_hash_object.__class__.__name__}")
        imgs = {}
        should_be_found = folder in os.listdir(self.databases_path)
        file_list = sorted(os.listdir(folder_path), key=lambda file: extract_number(file, ".*" + "-", "-" + self.distortion_name_dict[distortion.split('-')[0]], ".*"))

        counter = AMOUNT_OF_IMAGES[self.current_hash_object.__class__.__name__]
        if not self.cache:
            
            for file in file_list:
                progress_bar.update(1)
                key = file.split("-")[0]
                if key not in imgs.keys():
                    imgs[key] = []
                imgs[key].append(int(extract_number(file)))
                if len(imgs.keys()) == 100:
                    for key, value in imgs.items():
                        imgs[key] = np.array(value)
                    similarities = self.current_hash_object.get_similar_images(imgs, thresholds, output_folder=self.result_folder )
                    current_score = self.get_accuracies(similarities, should_be_found, current_score)
                    imgs = {}
                if counter == 1:
                    break
                counter -= 1
            if(len(imgs.keys()) > 0):
                similarities = self.current_hash_object.get_similar_images(imgs, thresholds)
                current_score = self.get_accuracies(similarities, should_be_found, current_score)

        if self.cache:
            cache_path = self.cache_dict[folder][distortion]
            for file in file_list:
                progress_bar.update(1)
                key = file.split("-")[0]
                if key not in imgs.keys():
                    imgs[key] = []
                    
                imgs[key].append(int(extract_number(file, key + "-", "-" + self.distortion_name_dict[distortion.split('-')[0]], ".*")))
                if len(imgs[key]) == 100:
                    for key, value in imgs.items():
                        imgs[key] = np.array(value)
                    similarities = self.current_hash_object.get_similar_images(imgs, cache_path)
                    current_score = self.get_accuracies(imgs, similarities, thresholds, should_be_found, current_score)
                    imgs = {}
                if counter == 1:
                    break
                counter -= 1
            if len(imgs.keys()) > 0:
                for key, value in imgs.items():
                    imgs[key] = np.array(value)
                similarities = self.current_hash_object.get_similar_images(imgs, cache_path)
                current_score = self.get_accuracies(imgs, similarities, thresholds, should_be_found, current_score)


        with open(os.path.join(self.result_folder, "new_false_negatives.txt"), "a") as file:
            file.write(f"New false negatives found for {folder} with {distortion} with {self.current_hash_object.__class__.__name__} \n")
            file.write(json.dumps(self.current_hash_object.new_fp))
            file.write("\n")
        
        with open(os.path.join(self.result_folder, "false_postives.txt"), "a") as file:
            file.write(f"False positives found for {folder} with {distortion} with {self.current_hash_object.__class__.__name__} \n")
            file.write(json.dumps(self.false_positives))
            file.write("\n") 
        
        self.current_hash_object.new_fp = {}


        progress_bar.close()
        # Logic to calculate tp, fp, tn, fn goes here
        return current_score
    
    def get_accuracies(self, imgs, similarities, thresholds,  should_be_found, current_score):
        time1 = time.time()
        for db, nrs in imgs.items():
            for threshold in thresholds:
                # check if the originals are found
                for i, nr in enumerate(nrs):
                    # print( similarities[i, nr])
                    # print( threshold)
                    if similarities[i, nr] >= threshold:
                        current_score[threshold][1] -= 1
                        if should_be_found:
                            current_score[threshold][0] += 1
                        else:
                            current_score[threshold][1] += 1
                    else:
                        if should_be_found:
                            current_score[threshold][3] += 1
                        else:
                            current_score[threshold][2] += 1
                    # similarities[i, nr] = 0
                # check if the false positives are found
                current_score[threshold][1] += np.sum(similarities >= threshold)

        time2 = time.time()
        # print(f"Time taken for False Positives: {time2-time1} seconds")
        return current_score

        # for db_and_nr, similarity in similarities.items():
        #     for threshold, db_dict in similarity.items():
        #         if threshold not in self.false_positives.keys():
        #             self.false_positives[threshold] = {}
        #         if should_be_found:
        #             if len(db_dict.keys()) == 0:
        #                 current_score[threshold][3] += 1
        #             else:
        #                 if db_and_nr.split(":")[0] in db_dict.keys() and int(db_and_nr.split(":")[1]) in db_dict[db_and_nr.split(":")[0]]:
        #                     current_score[threshold][0] += 1
        #                     current_score[threshold][1] -= 1
        #                     og_found = True
        #                 current_score[threshold][1] += sum(len(value) for value in db_dict.values())
        #                 if (len(self.false_positives[threshold].keys())<11) and ((og_found and len(db_dict[db_and_nr.split(":")[0]]) > 1) or (not og_found and len(db_dict[db_and_nr.split(":")[0]]) > 0)):
        #                     self.false_positives[threshold][db_and_nr.split(":")[1]] = str(db_dict[db_and_nr.split(":")[0]])
        #         else:
        #             if len(db_dict.keys()) == 0:
        #                 current_score[threshold][2] += 1
        #             else:
        #                 current_score[threshold][1] += sum(len(value) for value in db_dict.values())
        #                 if (len(self.false_positives[threshold].keys()) < 11):
        #                     self.false_positives[threshold][db_and_nr.split(":")[1]] = str(db_dict)

        
        return current_score
    def generate_auc(self, results, result_folder):
        auc_results = {}
        for distortion, value1 in results.items():
            auc_results[distortion] = {}
            for hash_object, value2 in value1.items():
                hash_object_name = hash_object
                fpr_tpr_pairs = []
                
                # Collect FPR and TPR pairs
                for _, value3 in sorted(value2.items()):
                    tp, fp, tn, fn = value3
                    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
                    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
                    fpr_tpr_pairs.append((fpr, tpr))
                
                # Sort by FPR in ascending order
                sorted_pairs = sorted(fpr_tpr_pairs, key=lambda x: x[0])
                sorted_fpr = [pair[0] for pair in sorted_pairs]
                sorted_tpr = [pair[1] for pair in sorted_pairs]
                
                # Calculate AUC using sorted FPR and TPR
                auc = np.trapz(sorted_tpr, sorted_fpr)
                auc_results[distortion][hash_object_name] = auc
        with open(os.path.join(result_folder, "auc.json"), 'w') as file:
            json.dump(auc_results, file)

    def generate_graphs(self, results, result_folder):
        # generate roc folder
        os.makedirs(os.path.join(result_folder, "roc"))

        for distortion, value1 in results.items():
            roc_points = {}
            for hash_object, value2 in value1.items():
                hash_object_name = hash_object
                # get ROC points
                roc_points[hash_object_name] = {}
                roc_points[hash_object_name]["tpr"] = []
                roc_points[hash_object_name]["fpr"] = []
                for _, value3 in sorted(value2.items()):
                    tp, fp, tn, fn = value3
                    if (tp + fn) == 0:
                        roc_points[hash_object_name]["tpr"].append(0)
                    else:
                        roc_points[hash_object_name]["tpr"].append(tp / (tp + fn))
                    if (fp + tn) == 0:
                        roc_points[hash_object_name]["fpr"].append(0)
                    else:
                        roc_points[hash_object_name]["fpr"].append(fp / (fp + tn))
                
                # clear previous plots
                plt.clf()

                # Generetate graph
                plt.rcParams['font.family'] = "Times New Roman"
                plt.rcParams['pdf.fonttype'] = 42
                plt.rcParams['ps.fonttype'] = 42
                plt.plot(roc_points[hash_object_name]["fpr"], roc_points[hash_object_name]["tpr"], label=hash_object)
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title(f"ROC Curve {distortion} with {hash_object_name}")
                plt.legend(fontsize=20)
                plt.savefig(os.path.join(result_folder, "roc", f"roc_curve_{distortion}_{hash_object_name}.pdf"), format="pdf")

            if len(roc_points.keys()) > 1:
                plt.clf()
                plt.rcParams['font.family'] = "Times New Roman"
                plt.rcParams['pdf.fonttype'] = 42
                plt.rcParams['ps.fonttype'] = 42
                for hash_object_name in roc_points.keys():
                    # plt.plot(roc_points[hash_object_name]["fpr"], roc_points[hash_object_name]["tpr"], 'o-', label=hash_object_name)
                    plt.plot(roc_points[hash_object_name]["fpr"], roc_points[hash_object_name]["tpr"], label=hash_object_name)
                plt.xlabel('False Positive Rate',fontsize=16)
                plt.ylabel('True Positive Rate',fontsize=16)
                plt.title(f"ROC Curve {distortion}", fontsize=18)
                plt.legend(fontsize=20)
                # plt.show()
                plt.savefig(os.path.join(result_folder, "roc", f"roc_curve_{distortion}.pdf"), format="pdf")

            # generate grap featuring multiple hash objects
        


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

    def convert(self, data):
        if isinstance(data, dict):
            return {k: self.convert(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert(item) for item in data]
        elif isinstance(data, np.int32):
            return int(data)
        else:
            return data
