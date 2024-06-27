from clip_interrogator import Config, Interrogator
import torch
import torch.nn.functional as F
import numpy as np
import shutil
from PIL import Image
from torchvision import transforms
import os

def calculate_similarity_in_batches(new_features, stored_features, batch_size=100):
    batch_similarities = []
    for i in range(0, len(stored_features), batch_size):
        batch = stored_features[i:i + batch_size]
        batch_tensor = torch.stack(batch)  # Create a batch tensor
        batch_similarity = F.cosine_similarity(new_features.unsqueeze(0), batch_tensor, dim=-1)
        batch_similarities.append(batch_similarity.cpu().numpy())  # Append batch result

    # Concatenate all batch results into a single NumPy array
    all_similarities = np.concatenate(batch_similarities)
    
    return all_similarities

def get_top_similar_images(new_features, database, image_folder, output_folder, X=5):
    all_similarities = calculate_similarity_in_batches(new_features, database, batch_size=100)
    all_similarities = [similarity[0] for similarity in all_similarities]
    # Get the indices of the top X similarities
    top_X_indices = np.argsort(all_similarities)[-X:][::-1]
    for idx in top_X_indices:
        similarity = all_similarities[idx]
        file_name = f"{idx}.jpg"  # Correctly convert index to filename
        source_path = f"{image_folder}/{file_name}"
        target_path = f"{output_folder}/{file_name}"
        shutil.copy2(source_path, target_path)
        print(f"Copied {file_name} to {output_folder} with similarity {similarity:.4f}")

# Configuration
ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
ci.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# List of input images
input_images = [
    'assets/quick_mistakes/test1.jpg',
    'assets/quick_mistakes/test2.jpg',
    'assets/quick_mistakes/test3.jpg'
]

# Load the database of stored features
db_path = "D:/Coding/PerceptionHash/assets/databases/MetaTestset_1/Vit/0.pt"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
database = torch.load(db_path, map_location=device)

# Image folder and target directory
image_folder = "D:/thesisdata/Included/1"
base_target_dir = 'assets/multimodal'

# Process each input image
for input_image_path in input_images:
    # Preprocess the input image
    vector = ci.image_to_features(Image.open(input_image_path).convert('RGB'))
    
    # Create a folder for this input image in the target directory
    image_name = os.path.splitext(os.path.basename(input_image_path))[0]
    target_dir = os.path.join(base_target_dir, image_name)
    os.makedirs(target_dir, exist_ok=True)
    
    # Get the top 5 most similar images for this input image
    get_top_similar_images(vector, database, image_folder, target_dir, X=3)
