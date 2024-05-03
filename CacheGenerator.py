import json
import os
from hash_methods import HASH_METHODS
from tqdm import tqdm

settings = json.load(open('settings.json'))

distorted_folder = settings["distorted_directory"]
chache_folder = "assets/cache/"

hash_objects = []
for key, value in HASH_METHODS.items():
    if key != "phash_vit" and key != "phash_dhash":
        hash_objects.append(value())

for directory in tqdm(os.listdir(distorted_folder)):
    for distortion in os.listdir(os.path.join(distorted_folder, directory)):
        # if distortion != "blur-2":
        #     continue
        for hash_object in hash_objects:
            # check if caceh folder exists, if not create it
            if not os.path.exists(chache_folder + directory + "/" + distortion):
                os.makedirs(chache_folder + directory + "/" + distortion)
            hash_object.cache_generation(distorted_folder + "/" + directory + "/" + distortion, chache_folder + directory + "/" + distortion, -1)
            print("Generated database for " + hash_object.__class__.__name__ + " for " + directory + " " + distortion)

