from clip_interrogator import Config, Interrogator, LabelTable
import torch
import torch.nn.functional as F
import numpy as np

def calculate_similarity_in_batches(new_features, stored_features, similarity_thresholds, batch_size=100):
    batch_similarities = []
    for i in range(0, len(stored_features), batch_size):
        batch = stored_features[i:i + batch_size]
        batch_tensor = torch.stack(batch)  # Create a batch tensor
        batch_similarity = F.cosine_similarity(new_features.unsqueeze(0), batch_tensor, dim=-1)
        batch_similarities.append(batch_similarity.cpu().numpy())  # Append batch result

    # Concatenate all batch results into a single NumPy array
    all_similarities = np.concatenate(batch_similarities)
    # get 5 biggest indexes of all_similarities
    top_5 = []
    for i in range(5):
        index = np.argmax(all_similarities)
        top_5.append(index)
        all_similarities[index] = 0
    return top_5
ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
table = LabelTable(["Formula 1 car"], "test", ci)
vector = table.embeds[0]
# transform vector to tensor
vector = torch.tensor(vector)
# move to gpu
vector = vector.to('cuda')
db_path = "D:\Coding\PerceptionHash/assets/databases/MetaTestset_1/Vit/0.pt" 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
database = torch.load(db_path, map_location=device)
print(calculate_similarity_in_batches(vector, database, [0.3,0.4,0.5,0.6,0.7,0.8,0.9], 2048))