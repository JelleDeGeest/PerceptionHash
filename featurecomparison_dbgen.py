import os
from clip_interrogator import Config, Interrogator
from PIL import Image
import torch
from Utilities import *
import time

# Initialize the Interrogator
interrogator = Interrogator(Config(clip_model_name="ViT-L-14/openai"))

# Folder containing the images
# folder_path = os.path.join("assets", "meta_testset")
folder_path = FULL_DB_PATH

# List to store feature vectors
feature_vectors = []

start_time = time.time()
# Process each file in the folder
for count, file in enumerate(os.listdir(folder_path), start=1):
    if count == 1000:
        break
    if count % 100 == 0:
        print(f"Processing image number: {count}")

    image_path = os.path.join(folder_path, file)
    image = Image.open(image_path).convert("RGB")

    # Get features and append to the list
    features = interrogator.image_to_features(image)
    feature_vectors.append(features.cpu())  # Move tensor to CPU

end_time = time.time()
# Save all feature vectors to a single file
torch.save(feature_vectors, 'feature_vectors_1000.pt')

print("All feature vectors saved. in " + str(end_time - start_time) + " seconds")
