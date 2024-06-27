import json
import os
from hash_methods import HASH_METHODS
from tqdm import tqdm
import concurrent.futures

def generate_cache(method):
    print(f"Generating cache for {method}")
    # Load settings from JSON file
    settings = json.load(open('settings.json'))

    # Define paths for the distorted images and the cache
    distorted_folder = settings["distorted_directory"]
    cache_folder = "assets/cache/"

    # Initialize hash objects (only for 'pdqhash' in this case)
    hash_objects = [value() for key, value in HASH_METHODS.items() if key == method]
    if method == "vit":
        for hash_object in hash_objects:
            hash_object.load_ci()
    # hash_objects = [value() for key, value in HASH_METHODS.items()]
    print(f"Hash objects: {hash_objects}")

    def process_distortion(directory, distortion):
        # Build full paths for distorted and cache directories
        distorted_path = os.path.join(distorted_folder, directory, distortion)
        cache_path = os.path.join(cache_folder, directory, distortion)

        # Check if cache folder exists, if not create it
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        # Generate cache for each hash object
        for hash_object in hash_objects:
            hash_object.cache_generation(distorted_path, cache_path, -1)
            print(f"Generated database for {hash_object.__class__.__name__} for {directory} {distortion}")

    def process_directory(directory):
        print(f"Processing directory {directory}")
        # List all distortions in the directory
        distortions = os.listdir(os.path.join(distorted_folder, directory))
        print(f"Distortions: {distortions}")
        # Use ThreadPoolExecutor to process each distortion in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda distortion: process_distortion(directory, distortion), distortions)

    # Process each directory using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Get a list of directories in the distorted folder
        directories = os.listdir(distorted_folder)
        # Display progress with tqdm as directories are processed
        list(tqdm(executor.map(process_directory, directories), total=len(directories)))

    print("All directories have been processed.")

generate_cache("phash_144")
generate_cache("dhash_256")
generate_cache("dhash_144")