import json
import os
import math
from PIL import Image, ImageDraw, ImageFont
from Utilities import create_square_grid_image

def read_false_positives(file_path):
    """Read false positives data from a file."""
    false_positives = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("New false negatives found for"):
                parts = line.strip().split()
                dataset = parts[5]
                distortion = parts[7]
                method = parts[9]
                next_line = next(file).strip()
                false_positives[(dataset, distortion, method)] = json.loads(next_line)
    return false_positives

def get_image_paths(base_dir, dataset, distortion, image_id, original_id):
    """Retrieve the image paths corresponding to the image IDs."""
    image_path = os.path.join(base_dir, dataset, distortion, f"{image_id}.jpg")
    original_path = os.path.join(base_dir, dataset, "originals", f"{original_id}.jpg")
    return [image_path, original_path]

def process_false_positives(base_image_dir, false_positive_file, output_dir):
    """Process all false positives and save the distorted and matched images separately."""
    false_positives = read_false_positives(false_positive_file)
    print(false_positives)

    counter = 0
    for (dataset, distortion, method), pairs in false_positives.items():
        for image_id, original_id in pairs.items():
            if distortion == "blur-2":
                filename = f"{dataset}-{image_id.split(':')[1]}-blurred-2.jpg"
            else:
                filename = f"{dataset}-{image_id.split(':')[1]}-color-distorted0_5.jpg"
            distorted_path = os.path.join(base_image_dir, dataset, distortion, filename)

            matched_path = os.path.join("D:/thesisdata/included", "1", f"{original_id.split(':')[1]}.jpg")

            # Load images
            distorted_image = Image.open(distorted_path)
            matched_image = Image.open(matched_path)

            # Save distorted image
            distorted_output_path = os.path.join(output_dir, f"{counter}-{distortion}-distorted.jpg")
            distorted_image.save(distorted_output_path)
            print(f"Saved distorted image to {distorted_output_path}")

            # Save matched image
            matched_output_path = os.path.join(output_dir, f"{counter}-{distortion}-matched.jpg")
            matched_image.save(matched_output_path)
            print(f"Saved matched image to {matched_output_path}")

            counter += 1
            if counter == 400:
                exit()

# Example usage
base_image_dir = 'D:/thesisdata\distorted'
false_positive_file = 'assets/results/01_06_2024 - 23_01_38/new_false_positives.txt'
output_dir = 'assets/fp_examples/vithash'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process false positives and generate collages
process_false_positives(base_image_dir, false_positive_file, output_dir)
