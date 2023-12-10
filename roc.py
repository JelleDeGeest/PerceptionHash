import torch
import torch.nn.functional as F
import os
from PIL import Image
from clip_interrogator import Config, Interrogator
import time
import numpy as np
from Utilities import *
import matplotlib.pyplot as plt
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
def get_score(original_picture, results, dictionary):
    original_picture_present = False
    if len(results) == 0:
        dictionary["FN"] += 1
        return
    if original_picture in results:
        dictionary["TP"] += 1
        original_picture_present = True
    if original_picture_present:
        dictionary["FP"] += len(results) - 1
    else:
        dictionary["FP"] += len(results) 




    # for i in results:
    #     if i == original_picture:
    #         dictionary["TP"] += 1
    #     else:
    #         dictionary["FP"] += 1

def calculate_roc_point(scores):
    TP = scores["TP"]
    FP = scores["FP"]
    TN = scores["TN"]
    FN = scores["FN"]

    # Calculate True Positive Rate (TPR) and False Positive Rate (FPR)
    TPR = TP / (TP + FN) if (TP + FN) != 0 else 0
    FPR = FP / (FP + TN) if (FP + TN) != 0 else 0

    return (FPR, TPR)  # Return the point (FPR, TPR) on the ROC curve

# Initialize the Interrogator with GPU support if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
interrogator = Interrogator(Config(clip_model_name="ViT-L-14/openai", device=device))

# Load and move the stored feature vectors to GPU if available
stored_feature_vectors = [vec.to(device) for vec in torch.load('feature_vectors.pt')]

# Folder containing the folders with the images
folder_path = os.path.join("assets", "distorted")

# Graph points
roc_points = []

for similiarity_threshold in np.arange(0.0, 1.0, 0.1):
    print(f"Similarity threshold: {similiarity_threshold}")
    scores = { "FN": 0, "FP": 0, "TN": 0, "TP": 0 }
    for folder in os.listdir(folder_path):
        path = os.path.join(folder_path, folder)
        print("Reading folder: " + path)
        for file in os.listdir(path):
            image_path = os.path.join(path, file)
            image = Image.open(image_path).convert("RGB")
            new_image_features = interrogator.image_to_features(image).to(device)
            similarities = calculate_similarity_in_batches(new_image_features, stored_feature_vectors, batch_size=2048, similarity_threshold=similiarity_threshold)
            get_score(int(file[1:7]), similarities, scores)
    
    roc_points.append(calculate_roc_point(scores))
    print(calculate_roc_point(scores))

    # Write the scores dictionary to file
    with open('scores.txt', 'a') as file:
        file.write(f"Scores: {scores}\n\n")

# Write the ROC points to file
with open('scores.txt', 'a') as file:
    file.write(f"ROC points: {roc_points}\n\n")

FPR_values, TPR_values = zip(*roc_points)

# Plot the ROC curve
plt.figure(figsize=(6, 6))
plt.plot(FPR_values, TPR_values, marker='o', linestyle='-')
plt.title('ROC Curve')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.grid(True)
plt.show()
