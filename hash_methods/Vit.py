from .HashMethod import HashMethod
import os
import json
from clip_interrogator import Config, Interrogator
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from tqdm import tqdm
from Utilities import extract_number


class Vit(HashMethod):
    def __init__(self):
        self.databases = None
        with open("Settings.json") as file:
            settings = json.load(file)
        self.database_path = os.path.join(settings["working_directory"], "databases")
        self.ci = None
        self.databases_loaded = None
        self.new_fp = {}

    def load_ci(self):
        if self.ci is None:
            self.ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))

    def get_similar_images(self, images: dict, similarity_thresholds, cache_path=None):
        self.load_ci()
        if self.databases is None:
            raise Exception("No database set for Vit. Use set_database() to set a database.")
        if self.databases_loaded is None:
            self.databases_loaded = {}
            for database in self.databases:
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                self.databases_loaded[database] = torch.load(os.path.join(self.database_path, database, "Vit", "0.pt"), map_location=device)
        if cache_path is not None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            hashes = torch.load(os.path.join(cache_path, "ViT.pt"), map_location=device)


        for key in images.keys():
            if cache_path is not None:
                image_hash = hashes[images[key]]
            else:
                image_hash = self.ci.image_to_features(images[key])
            similarities = {}
            for threshold in similarity_thresholds:
                similarities[threshold] = {}
            for db_name, db_tensor in self.databases_loaded.items():
                temp = self.calculate_similarity_in_batches(image_hash, db_tensor,  similarity_thresholds, 2048)
                for threshold, value in temp.items():
                    if len(value) > 0:
                        similarities[threshold][db_name] = value
            images[key] = similarities

        return images
        

    def set_database(self, database):
        self.databases = database
    
    def calculate_similarity_in_batches(self, new_features, stored_features, similarity_thresholds, batch_size=100):
        batch_similarities = []
        for i in range(0, len(stored_features), batch_size):
            batch = stored_features[i:i + batch_size]
            batch_tensor = torch.stack(batch)  # Create a batch tensor
            batch_similarity = F.cosine_similarity(new_features.unsqueeze(0), batch_tensor, dim=-1)
            batch_similarities.append(batch_similarity.cpu().numpy())  # Append batch result

        # Concatenate all batch results into a single NumPy array
        all_similarities = np.concatenate(batch_similarities)
        sim_dict = {}
        for threshold in similarity_thresholds:
            sim_dict[threshold] = np.where(all_similarities > threshold)[0]

        return sim_dict

    def database_generation(self, images_path, database_path):
        self.load_ci()

        # Check if all files have same file extension
        file_extensions = set()
        for file in os.listdir(images_path):
            file_extensions.add(os.path.splitext(file)[1])
        if len(file_extensions) > 1:
            raise Exception("All files must have the same file extension")
        extension = file_extensions.pop()

        feature_vectors = []
        
        for index in tqdm(range(len(os.listdir(images_path)))):
            file_path = os.path.join(images_path, str(index)+extension)
            with Image.open(file_path).convert("RGB") as image:
                features = self.ci.image_to_features(image)
                feature_vectors.append(features.cpu())
        
        database_partition = 0
        torch.save(feature_vectors, os.path.join(database_path, str(database_partition)+".pt"))

        print(f"Hashes written to {os.path.join(database_path, str(database_partition)+'.pt')}")
    
    def cache_generation(self, images_path, output_path, lenght=-1):
        self.load_ci()

        file_extensions = set()
        for file in os.listdir(images_path):
            file_extensions.add(os.path.splitext(file)[1])
        if len(file_extensions) > 1:
            raise Exception("All files must have the same file extension")
        extension = file_extensions.pop()

        feature_vectors = []

        files = sorted(os.listdir(images_path),key=extract_number)

        for filename in tqdm(files):
            if filename.endswith(extension):  # Check if the file has the right extension
                file_path = os.path.join(images_path, filename)
                with Image.open(file_path).convert("RGB") as image:
                    features = self.ci.image_to_features(image)
                    feature_vectors.append(features.cpu())
                if len(feature_vectors) == lenght:
                    break
        
        torch.save(feature_vectors, os.path.join(output_path, str("ViT")+".pt"))
        # print(f"Hashes written to {os.path.join(output_path, str("ViT")+'.pt')}")
        

