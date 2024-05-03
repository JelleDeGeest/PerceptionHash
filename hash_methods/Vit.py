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
import time


class Vit(HashMethod):
    def __init__(self):
        self.databases = None
        with open("Settings.json") as file:
            settings = json.load(file)
        self.database_path = os.path.join(settings["working_directory"], "databases")
        self.ci = None
        self.databases_loaded = None
        self.new_fp = {}
        self.cache = None
        self.cache_path = None

    def load_ci(self):
        if self.ci is None:
            self.ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))

    def get_similar_images(self, images: dict, cache_path=None):
        time1 = time.time()
        
        # check if a database has been set
        if cache_path is None:
            self.load_ci()
        if self.databases is None:
            raise Exception("No database set for Vit. Use set_database() to set a database.")
        
        # Load the databases if they haven't been loaded yet
        if self.databases_loaded is None:
            self.databases_loaded = {}
            for database in self.databases:
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                # device = torch.device("cpu")
                self.databases_loaded[database] = torch.load(os.path.join(self.database_path, database, "Vit", "0.pt"), map_location=device)
                self.databases_loaded[database] = torch.cat(self.databases_loaded[database], dim=0)
                self.databases_loaded[database] = torch.nn.functional.normalize(self.databases_loaded[database], p=2, dim=1)


        # Load cache if it hasn't been loaded yet
        if cache_path is not None and cache_path != self.cache_path:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.cache = torch.load(os.path.join(cache_path, "ViT.pt"), map_location=device)
            self.cache = torch.cat(self.cache , dim=0)
            self.cache = torch.nn.functional.normalize(self.cache, p=2, dim=1)
            self.cache_path = cache_path


        if cache_path is not None:
            for key, value in images.items():
                image_hashes = self.cache[value.min():(value.max()+1)]

                # Compute cosine similarity
                cosine_sim = torch.mm(image_hashes, self.databases_loaded[self.databases[0]].t())  # Shape (100, 50000)

                # Tensor to cpu and numpy array
                cosine_sim = cosine_sim.cpu()

                # Convert to NumPy array
                similarities = cosine_sim.numpy()


        # # Calculate similarity
        # for key in images.keys():
        #     if cache_path is not None:
        #         image_hash = self.cache[images[key]]
        #     else:
        #         image_hash = self.ci.image_to_features(images[key])
        #     similarities = {}
        #     for threshold in similarity_thresholds:
        #         similarities[threshold] = {}
        #     for db_name, db_tensor in self.databases_loaded.items():
        #         temp = self.calculate_similarity_in_batches(image_hash, db_tensor,  similarity_thresholds, 2048)
        #         for threshold, value in temp.items():
        #             if len(value) > 0:
        #                 similarities[threshold][db_name] = value
        #     images[key] = similarities
        time2 = time.time()
        print(f"Time taken for Similarity: {time2-time1} seconds")

        return similarities.astype(np.float64)
        

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

        files = sorted(os.listdir(images_path), key=lambda file: extract_number(file, ".*" + "-", "-" + ".*", ""))

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
        

