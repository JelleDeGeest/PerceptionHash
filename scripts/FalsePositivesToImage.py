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
            # chack if first character of the line is an F otherwise skip the line search
            if line[0] != "F":
                continue

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
file_path = 'assets/results/24_04_2024 - 14_36_23/false_postives.txt'
output_path = 'assets/results/24_04_2024 - 14_36_23'
hashing_methods = ["Phash_Vit"]
thresholds = ["0.78125"]
distortion = "blur-2"
database = "MetaTestset_1"
os.makedirs(os.path.join(output_path, "false_postives"), exist_ok=True)
for i, hashing_method in enumerate(hashing_methods):
    keywords = [database, distortion, hashing_method]
    dict_found = find_dict(file_path, keywords)
    os.makedirs(os.path.join(output_path, "false_postives", hashing_method), exist_ok=True)
    images = dict_found[thresholds[i]]
    for original, similar in images.items():
        # get original image
        input_image = os.path.join(settings["input_directories"][database], original+".jpg")
        # get similar images
        similar_image_folder = os.path.join(settings["distorted_directory"], database, distortion)
        matches = ast.literal_eval(similar)
        match_list = []
        for match in matches:
            found_filename = None
            for filename in os.listdir(similar_image_folder):
                # Split the filename around dashes and extract the number part
                parts = filename.split('-')
                if len(parts) > 1 and parts[1].isdigit():  # Check if the second part is a number
                    number = int(parts[1])
                    if number == match:
                        found_filename = filename
                        break

            if found_filename is not None:
                match_list.append(os.path.join(similar_image_folder, found_filename))
        
        if match_list != []:
            end_image = create_square_grid_image([input_image] + match_list, original_found=True)
            end_image.save(os.path.join(output_path, "false_postives", hashing_method, original+".jpg"))

                

