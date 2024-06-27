from perception.hashers import PHash, PDQHash, DHash
import numpy as np
import shutil
import json
from PIL import Image
import os

def get_most_similar_images(json_path, image_path, image_folder, output_folder, X=5):
    # Load vector from json file
    with open(json_path, 'r') as f:
        db = json.load(f)

    # Load and process the new image
    image = Image.open(image_path).convert('RGB')
    hasher = PDQHash()
    new_hash = hasher.compute(image)
    
    # Calculate distances to all database entries
    distances = []
    for entry in db:
        distances.append(hasher.compute_distance(new_hash, entry))

    # Return the indices of the X smallest distances
    top_X_indices = np.argsort(distances)[:X]

    # Copy the most similar images to the target directory and print their distances
    for idx in top_X_indices:
        distance = distances[idx]
        file_name = f"{idx}.jpg"  # Assuming db entries contain image names without extension
        source_path = f"{image_folder}/{file_name}"
        target_path = f"{output_folder}/{file_name}"
        shutil.copy2(source_path, target_path)
        print(f"Copied {file_name} to {output_folder} with distance {distance:.4f}")

# Define paths
json_path = "assets/databases/MetaTestset_1/PDQhash/0.json"
image_folder = "D:/thesisdata/Included/1"
base_target_dir = 'assets/quick_mistakes'

# List of input images
input_images = [
    'assets/quick_mistakes/test1.jpg',
    'assets/quick_mistakes/test2.jpg',
    'assets/quick_mistakes/test3.jpg'
]

# Process each input image
for image_path in input_images:
    # Create a folder for this input image in the target directory
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    target_dir = os.path.join(base_target_dir, image_name)
    os.makedirs(target_dir, exist_ok=True)
    
    # Get the top X most similar images for this input image
    get_most_similar_images(json_path, image_path, image_folder, target_dir, X=3)
