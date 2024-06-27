import torch
import torch.nn.functional as F
from clip_interrogator import Config, Interrogator
from PIL import Image

# Configuration
ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
ci.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_image_features(image_path, ci):
    """Load an image and get its feature vector using the provided CLIP Interrogator."""
    input_image = Image.open(image_path).convert("RGB")
    features = ci.image_to_features(input_image).to(ci.device)
    return features

def calculate_cosine_similarity(feature_a, feature_b):
    """Calculate the cosine similarity between two feature vectors."""
    similarity = F.cosine_similarity(feature_a, feature_b, dim=-1).item()
    return similarity

# Paths to the images
image_path_a = "assets/temp/Similar_image_example_a.png"
image_path_b = "assets/temp/Similar_image_example_b.png"
image_path_c = "assets/temp/Similar_image_example_c.png"
image_path_d = "assets/temp/Similar_image_example_d.png"

# Get feature vectors for each image
features_a = get_image_features(image_path_a, ci)
features_b = get_image_features(image_path_b, ci)
features_c = get_image_features(image_path_c, ci)
features_d = get_image_features(image_path_d, ci)

# Calculate similarities
similarity_ab = calculate_cosine_similarity(features_a, features_b)
similarity_ac = calculate_cosine_similarity(features_a, features_c)
similarity_ad = calculate_cosine_similarity(features_a, features_d)

# Print the similarities
print(f"Similarity between image A and image B: {similarity_ab:.4f}")
print(f"Similarity between image A and image C: {similarity_ac:.4f}")
print(f"Similarity between image A and image D: {similarity_ad:.4f}")
