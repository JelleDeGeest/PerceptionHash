import ast
import re
import os
from Utilities import create_square_grid_image
import json


def find_dict(file_path, keywords):
    # Construct a regular expression that matches lines containing all keywords
    # The following pattern constructs a regex that looks for each keyword, regardless of order
    regex_pattern = r'(?=.*\b{}\b)'.format(r'\b)(?=.*\b'.join(map(re.escape, keywords))) + r'.*'

    # Initialize a variable to store the dictionary
    found_dict = None

    # Open the file and read line by line
    with open(file_path, 'r') as file:
        while True:
            line = file.readline().strip()  # Read a line and strip any leading/trailing whitespace
            if not line:
                break  # Stop if end of file
            if re.search(regex_pattern, line):
                # Read the next line for the dictionary
                dict_line = file.readline().strip()
                try:
                    # Convert the string representation of a dictionary to a dictionary
                    found_dict = ast.literal_eval(dict_line)
                except ValueError as e:
                    print(f"Error reading dictionary: {e}")
                break  # Optional: break if you only need the first occurrence

    # Output the found dictionary
    if found_dict is not None:
        return found_dict
    else:
        return None
# read in settings file
with open("Settings.json") as file:
    settings = json.load(file)
file_path = 'assets/results/10K blur-2/new_false_positives.txt'
output_path = 'assets/results/10K blur-2'
hashing_methods = ["Phash_Vit", "Phash_Dhash"]
thresholds = ["0.84375", "0.84375"]
distortion = "blur-2"
os.makedirs(os.path.join(output_path, "new_false_negatives"), exist_ok=True)
for i, hashing_method in enumerate(hashing_methods):
    keywords = ["MetaTestset_1", distortion, hashing_method]
    dict_found = find_dict(file_path, keywords)
    os.makedirs(os.path.join(output_path, "new_false_negatives", hashing_method), exist_ok=True)
    images = dict_found[thresholds[i]]
    for image in images:
        # get original image
        input_image = os.path.join(settings["input_directories"][image.split(":")[0]], image.split(":")[1]+".jpg")
        # get similar image
        similar_image_folder = os.path.join(settings["distorted_directory"], image.split(":")[0], distortion)
        found_filename = None
        for filename in os.listdir(similar_image_folder):
            # Split the filename around dashes and extract the number part
            parts = filename.split('-')
            if len(parts) > 1 and parts[1].isdigit():  # Check if the second part is a number
                number = parts[1]
                if number == image.split(":")[1]:
                    found_filename = filename
                    break
        
        # save image to new_false_negatives folder
        if found_filename is not None:
            end_image = create_square_grid_image([input_image,os.path.join(similar_image_folder, found_filename)], original_found=False)
            end_image.save(os.path.join(output_path, "new_false_negatives", hashing_method, image.split(":")[1]+".jpg"))

                


