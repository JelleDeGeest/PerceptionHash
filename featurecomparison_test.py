import torch
import torch.nn.functional as F
import os
from PIL import Image
from clip_interrogator import Config, Interrogator
import time
import numpy as np
from Utilities import *

# Function to process in batches
def calculate_similarity_in_batches(new_features, stored_features, batch_size=100, similarity_threshold=0.9):
    batch_similarities = []
    for i in range(0, len(stored_features), batch_size):
        batch = stored_features[i:i + batch_size]
        batch_tensor = torch.stack(batch)  # Create a batch tensor
        batch_similarity = F.cosine_similarity(new_features.unsqueeze(0), batch_tensor, dim=-1)
        batch_similarities.append(batch_similarity.cpu().numpy())  # Append batch result

    # Concatenate all batch results into a single NumPy array
    all_similarities = np.concatenate(batch_similarities)

    return np.where(all_similarities > similarity_threshold)[0]
    # return np.where(all_similarities > similarity_threshold)

# returns correct, false_negatives, false_postives
def get_score(original_picture, results):
    if original_picture in results and len(results) == 1:
        return 1, 0, 0
    elif original_picture in results and len(results) > 1:
        # return 1, 0, len(results) - 1
        return 0, 0, 1
    elif original_picture not in results:
        # return 0, 1, len(results)
        return 0, 1, 0

# Initialize the Interrogator with GPU support if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
interrogator = Interrogator(Config(clip_model_name="ViT-L-14/openai", device=device))

# Load and move the stored feature vectors to GPU if available
stored_feature_vectors = [vec.to(device) for vec in torch.load('feature_vectors.pt')]

# Folder containing the folders with the images
folder_path = os.path.join("assets", "distorted")

for folder in os.listdir(folder_path):
    correct, false_negatives, false_positives = 0, 0, 0
    path = os.path.join(folder_path, folder)
    print("Reading folder: " + path)
    for file in os.listdir(path):
        image_path = os.path.join(path, file)
        image = Image.open(image_path).convert("RGB")
        new_image_features = interrogator.image_to_features(image).to(device)
        similarities = calculate_similarity_in_batches(new_image_features, stored_feature_vectors, batch_size=2048)
        score = get_score(int(file[1:7]), similarities)
        correct, false_negatives, false_positives = correct + score[0], false_negatives + score[1], false_positives + score[2]
        # if score != (1, 0, 0):
        #     print(f"Wrong match for {file} is {str(similarities)}")
        if score != (1, 0, 0) and len(similarities) > 0:
            image_list = [image_path]
            for i in similarities:
                image_list.append(os.path.join(FULL_DB_PATH, int_to_filename(i)))
            contains_original = False
            if int(file[1:7]) in similarities:
                contains_original = True
            filename = file.split("_")[0]
            create_square_grid_image(image_list, contains_original, spacing=10, border_width=5, text_size=40).save(os.path.join("assets", "wrong_matches", f"{folder}_{filename}.jpg"))

    print("------------------------------------------------------------------------------------------")
    print(f"Results for folder {folder}:")
    print(f"Only orginal: {correct}, Original + extra: {false_negatives}, Original not found: {false_positives}")
    print("------------------------------------------------------------------------------------------")