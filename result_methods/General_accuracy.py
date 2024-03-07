import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import os
from PIL import Image

class General_accuracy():
    def __init__(self, hash_objects):
        self.hash_objects = hash_objects

        self.execute()

    def execute(self):
        self.current_hash_object = self.hash_objects[0]
        thresholds = self.current_hash_object.get_general_accuracy_thresholds()

        # Initialize figure and axes outside the animation function
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.subplots_adjust(right=0.72)
        for spine in self.ax.spines.values():
            spine.set_visible(False)

        def animate(i):
            # Clear the axes for the new plot
            self.ax.clear()
            # Generate new data
            data = self.get_data(thresholds[i])
            data = {"original": [100-10*i, 0, 10*i], "phash": [50-5*i,50, 0+5*i], "vit": [30-2*i, 30+2*i, 40]}
            # Plot the new data
            self.create_horizontal_bar_chart(data, f"General Accuracy at similarity {i*10}%")

        # Create the animation
        ani = animation.FuncAnimation(self.fig, animate, frames=range(len(thresholds)), repeat=False)
        ani.save(filename="tmp/html_example.html", writer="html")

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

    def get_data(self, threshold):
        for distortion, folder_path in self.current_hash_object.get_folders_to_test().items():
            print(distortion)
            imgs = []
            for file in os.listdir(folder_path):
                
                imgs.append(Image.open(os.path.join(folder_path, file)))
                if len(imgs) == 100:
                    similarities = self.current_hash_object.get_similar_images(imgs, threshold)
                    print(similarities)
                    imgs = []

            
        pass

    

