import os
import numpy as np
import json
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from perception.hashers import PHash
import matplotlib.font_manager as fm

# Load custom font
custom_font = fm.FontProperties(fname='UGentPannoText-SemiBold-1.ttf')

# Define paths
json_path = "assets\databases\ImSim\Phash_256/0.json"
image_folder = "D:/thesisdata/SimIm/1"

# Define a function to calculate similarity using PDQHash
def calculate_similarity_in_batches(new_hash, stored_hashes):
    distances = []
    hasher = PHash(hash_size=16)
    for stored_hash in stored_hashes:
        distances.append(hasher.compute_distance(new_hash, stored_hash))
    return np.array(distances)

# Load the database of stored hashes
with open(json_path, 'r') as f:
    database = json.load(f)

# Lists to store similarities
correct_matches = []
incorrect_matches = []

# Iterate over each image in the folder
for filename in os.listdir(image_folder):
    if filename.endswith(".jpg"):
        image_path = os.path.join(image_folder, filename)
        
        # Load and process the new image
        image = Image.open(image_path).convert('RGB')
        hasher = PHash(hash_size=16)
        new_hash = hasher.compute(image)
        
        # Calculate similarity
        similarities = calculate_similarity_in_batches(new_hash, database)
        
        image_name = os.path.splitext(filename)[0] 
        for i, similarity in enumerate(similarities):
            if i == int(image_name):
                correct_matches.append(similarity)
            else:
                incorrect_matches.append(similarity)

print(len(correct_matches))
print(len(incorrect_matches))

# Ensure the lists are flat (1D)
correct_matches = np.array(correct_matches).flatten()
incorrect_matches = np.array(incorrect_matches).flatten()

# Plot the similarity distributions as KDE plots
plt.figure(figsize=(12, 7))

# Plot for correct and incorrect matches on the same plot
sns.kdeplot(correct_matches, color='green', fill=True, label='Correct Matches', common_norm=False, clip=(0, 1))
sns.kdeplot(incorrect_matches, color='red', fill=True, label='Incorrect Matches', common_norm=False, clip=(0, 1))
# plt.title('Similarity Distribution for Correct and Incorrect Matches', fontsize=32, fontproperties=custom_font)
plt.xlabel('Similarity', fontsize=32, fontproperties=custom_font)
plt.ylabel('Density', fontsize=32, fontproperties=custom_font)

# Adjust the legend to avoid overlapping the graph lines
legend = plt.legend(loc='upper right', bbox_to_anchor=(1, 1))
for text in legend.get_texts(): 
    text.set_fontproperties(custom_font)
    text.set_fontsize(24)

# Change the font and size of axis numbers
plt.xticks(fontsize=40, fontproperties=custom_font)
plt.yticks(fontsize=40, fontproperties=custom_font)
plt.tick_params(axis='both', which='major', labelsize=24)

# Save plot
plt.savefig('SimImPHash.png')