import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import os
from PIL import Image
from hash_methods import RESULT_THRESHOLDS, AMOUNT_OF_IMAGES
import json
from tqdm import tqdm

class General_accuracy():
    def __init__(self, hash_objects, folders_to_hash):
        self.hash_objects = hash_objects
        self.folders_to_hash = folders_to_hash
        with open("Settings.json") as file:
            settings = json.load(file)
        self.databases_path = os.path.join(settings["working_directory"], "databases")
        

    def execute(self, result_folder):
        total = len(self.folders_to_hash) * len(self.hash_objects)
        progress_bar = tqdm(total=total, leave=False)
        for folder, folder_path in self.folders_to_hash.items():
            for hash_object in self.hash_objects:
                progress_bar.set_description(f"General_accuracy: {folder} with {hash_object.__class__.__name__}")
                self.current_hash_object = hash_object
                thresholds = RESULT_THRESHOLDS["general_accuracy"][hash_object.__class__.__name__]
  

                # Initialize figure and axes outside the animation function
                self.fig, self.ax = plt.subplots(figsize=(10, 6))
                self.fig.subplots_adjust(right=0.72)
                for spine in self.ax.spines.values():
                    spine.set_visible(False)

                progress_bar_thresholds = tqdm(total=len(thresholds), desc=f"General_accuracy: {folder} with {hash_object.__class__.__name__}: Similarities", leave= False)
                def init():
                    self.ax.clear()
                    self.ax.set_title(f"Initializing...")
                    return self.fig
            
                def animate(i):
                    # Clear the axes for the new plot
                    self.ax.clear()
                    # Generate new data
                    data = self.get_data(thresholds[i], folder, folder_path)
                    progress_bar_thresholds.update(1)
                      # Plot the new data
                    self.create_horizontal_bar_chart(data, f"General Accuracy of {hash_object.__class__.__name__} at Similarity {thresholds[i]} on {folder}")
                
                # Create the animation
                ani = animation.FuncAnimation(self.fig, animate, frames=len(thresholds), init_func=init, repeat=False)
                # create folder for the hash object
                os.makedirs(os.path.join(result_folder, hash_object.__class__.__name__))
                path  = os.path.join(result_folder, hash_object.__class__.__name__, "general_accuracy.html")
                ani.save(filename=path, writer="html")
                progress_bar.update(1)

    def create_horizontal_bar_chart(self, data, plot_title):
        labels = list(data.keys())
        y_pos = np.arange(len(labels))
        green_data = [values[0] for values in data.values()]
        orange_data = [values[1] for values in data.values()]
        red_data = [values[2] for values in data.values()]
        colors = ['green', 'orange', 'red']

        self.ax.barh(y_pos, green_data, color=colors[0], edgecolor='black', label='Only Original')
        self.ax.barh(y_pos, orange_data, left=green_data, color=colors[1], edgecolor='black', label='Original + Extra')
        self.ax.barh(y_pos, red_data, left=[i+j for i, j in zip(green_data, orange_data)], color=colors[2], edgecolor='black', label='Original Not Found')

        self.ax.set_yticks(y_pos)
        self.ax.set_yticklabels(labels)
        self.ax.set_xlabel("Images")
        self.ax.set_title(plot_title)
        self.ax.legend(loc='center right', bbox_to_anchor=(1.4, 0.5), frameon=False, title='Resulting matches')

    def get_data(self, threshold, folder, folder_path):
        data = {}
        should_be_found = folder in os.listdir(self.databases_path)
        if AMOUNT_OF_IMAGES[self.current_hash_object.__class__.__name__] == -1:
            total_images = sum(len(os.listdir(os.path.join(folder_path, df))) for df in os.listdir(folder_path))
        else:
            total_images = AMOUNT_OF_IMAGES[self.current_hash_object.__class__.__name__] * len(os.listdir(folder_path))
        progress_bar = tqdm(total=total_images, desc=f"General_accuracy: {folder} with {self.current_hash_object.__class__.__name__} at similarity {threshold}", leave= False)            
        for distortion_folder in os.listdir(folder_path):
            counter = AMOUNT_OF_IMAGES[self.current_hash_object.__class__.__name__]
            current_score = [0, 0, 0]
            distortion_folder_path = os.path.join(folder_path, distortion_folder)
            # get the amount of images in the folder
            folder_count = len(os.listdir(distortion_folder_path))
            # Process images in batches of 100
            imgs = {}
            for file in os.listdir(distortion_folder_path):
                key = file.split("-")[0] + ":" + file.split("-")[1]
                imgs[key] = Image.open(os.path.join(distortion_folder_path, file))
                if len(imgs.keys()) == 1000:
                    similarities = self.current_hash_object.get_similar_images(imgs, threshold)
                    current_score = [x + y for x, y in zip(current_score, self.get_accuracy_triplet(similarities, should_be_found ))]
                    imgs = {}
                if counter == 0:
                    break
                counter -= 1
                progress_bar.update(1)

            if(len(imgs.keys()) > 0):
                similarities = self.current_hash_object.get_similar_images(imgs, threshold)
                current_score = [x + y for x, y in zip(current_score, self.get_accuracy_triplet(similarities, should_be_found ))]
            data[distortion_folder] = current_score
        progress_bar.close()
        return data
    
    def get_accuracy_triplet(self, similarities, should_be_found):
        data = [0, 0, 0]
        for key, value in similarities.items():
            if should_be_found:
                if key.split(":")[0] not in value.keys():
                    data[2] += 1
                elif int(key.split(":")[1]) not in value[key.split(":")[0]]:
                    data[2] += 1
                elif len(value[key.split(":")[0]]) > 1:
                    data[1] += 1
                else:
                    data[0] += 1
            else:
                if len(value.keys()) > 0:
                    data[2] += 1
                else:
                    data[0] += 1
        return data
    




    

