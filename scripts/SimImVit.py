import os
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from clip_interrogator import Config, Interrogator
import matplotlib.font_manager as fm

# Load custom font
custom_font = fm.FontProperties(fname='UGentPannoText-SemiBold-1.ttf')

# Configuration
ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
ci.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the database of stored features
db_path = "assets/databases/ImSim/Vit/0.pt"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
database = torch.load(db_path, map_location=device)

# Define the image folder
image_folder = "D:/thesisdata/SimIm/1"

# Define a function to calculate similarity in batches
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

# Lists to store similarities
correct_matches = []
incorrect_matches = []

# Iterate over each image in the folder
for filename in os.listdir(image_folder):
    if filename.endswith(".jpg"):
        image_path = os.path.join(image_folder, filename)
        
        # Preprocess the input image and extract its feature vector
        image = Image.open(image_path).convert('RGB')
        vector = ci.image_to_features(image)
        
        # Calculate similarity
        similarities = calculate_similarity_in_batches(vector, database, batch_size=100)
            
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
legend = plt.legend(loc='upper left', bbox_to_anchor=(0, 1))
for text in legend.get_texts(): 
    text.set_fontproperties(custom_font)
    text.set_fontsize(24)

# Change the font and size of axis numbers
plt.xticks(fontsize=40, fontproperties=custom_font)
plt.yticks(fontsize=40, fontproperties=custom_font)
plt.tick_params(axis='both', which='major', labelsize=24)

# Save plot
plt.savefig('SimImVit.png')