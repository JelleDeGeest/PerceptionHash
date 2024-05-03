from PIL import Image, ImageDraw, ImageFont
import math
import os
from tqdm import tqdm
import json
import re

FULL_DB_PATH = "D:/thesisdata/Included"
NOT_IN_DB_PATH = "D:/thesisdata/Not-included"

def concatenate_images(image_path1, image_path2, output_path):
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    image1_width, image1_height = image1.size
    image2_width, image2_height = image2.size

    new_image = Image.new('RGB', (image1_width + image2_width, max(image1_height, image2_height)))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_width, 0))

    new_image.save(output_path)

def create_square_grid_image(image_paths, original_found=True, spacing=10, border_width=5, text_size=40):
    if original_found:
        second_color = 'green'
    else:
        second_color = 'red'

    # Load images
    images = [Image.open(path) for path in image_paths]

    # Determine grid size (number of rows and columns)
    grid_size = math.ceil(math.sqrt(len(images)))

    # Calculate the total size of the grid
    row_max_height = [0] * grid_size
    col_max_width = [0] * grid_size
    for i, image in enumerate(images):
        row, col = divmod(i, grid_size)
        row_max_height[row] = max(row_max_height[row], image.size[1])
        col_max_width[col] = max(col_max_width[col], image.size[0])

    total_width = sum(col_max_width) + spacing * (grid_size - 1)
    total_height = sum(row_max_height) + spacing * (grid_size - 1)

    # Create a new image to hold the grid
    grid_image = Image.new('RGB', (total_width, total_height), 'black')

    # Initialize ImageDraw
    draw = ImageDraw.Draw(grid_image)

    # Define font
    try:
        font = ImageFont.truetype("arial.ttf", text_size)
    except IOError:
        font = ImageFont.load_default()

    # Function to draw text with background
    def draw_text_with_background(draw, text, position, font, text_color, bg_color, text_size):
        text_width, text_height = draw.textlength(text, font=font), text_size
        bg_position = (position[0], position[1], position[0] + text_width + 10, position[1] + text_height + 10)
        draw.rectangle(bg_position, fill=bg_color)
        draw.text((position[0] + 5, position[1] + 5), text, fill=text_color, font=font)

    # Paste images into the grid, draw borders, and add text
    current_x, current_y = 0, 0
    for i, image in enumerate(images):
        if i % grid_size == 0 and i != 0:  # New row
            current_x = 0
            current_y += row_max_height[i // grid_size - 1] + spacing
        grid_image.paste(image, (current_x, current_y))

        # Draw border and text for the first image
        if i == 0:
            draw.rectangle(
                [current_x, current_y, current_x + image.size[0], current_y + image.size[1]], 
                outline='blue', width=border_width
            )
            draw_text_with_background(draw, "Image", (current_x + 5, current_y + image.size[1] - text_size - 15), font, 'blue', 'black', text_size)

        # Draw border and text for the second image
        if i == 1:
            draw.rectangle(
                [current_x, current_y, current_x + image.size[0], current_y + image.size[1]], 
                outline=second_color, width=border_width
            )
            draw_text_with_background(draw, "Original", (current_x + 5, current_y + image.size[1] - text_size - 15), font, second_color, 'black', text_size)

        current_x += col_max_width[i % grid_size] + spacing

    return grid_image

def int_to_filename(number, base_name="R", extension=".jpg", total_length=6, subdir=True):
    # Convert the number to a string and pad it with zeros to the desired total length
    padded_number = str(number).zfill(total_length)
    multiple = (number // 50000) + 1
    # Construct the filename
    if subdir:
        filename = f"{multiple}/{base_name}{padded_number}{extension}"
    else:
        filename = f"{base_name}{padded_number}{extension}"
    return filename

def is_sequential_naming(folder_path):
    with os.scandir(folder_path) as entries:
        # Creating a generator expression to count files without loading all names into memory
        num_files = sum(1 for _ in entries)

    # Resetting entries iterator by reopening scandir
    with os.scandir(folder_path) as entries:
        # Check for the existence of each expected filename
        expected_files_found = 0
        for entry in entries:
            if entry.is_file():
                name, ext = os.path.splitext(entry.name)
                if name.isdigit() and 0 <= int(name) < num_files:
                    expected_files_found += 1
                else:
                    # Found a file not matching the naming convention
                    return False

    # If the count of sequentially named files matches the total number, the structure is correct
    return expected_files_found == num_files

def rename_images_in_input_folder(folder_path, input_folder_name):
    print("Checking if the input folder follows the desired naming structure...")
    if is_sequential_naming(folder_path):
        print("Folder follows the desired naming structure. No changes made.")
        return
    print("Folder does not follow the desired naming structure. Renaming files...")

    # because the indexes are changing we need to delete existing databases
    with open("Settings.json") as file:
        settings = json.load(file)

    database_path = os.path.join(settings["working_directory"], "databases" ,input_folder_name)

    if os.path.exists(database_path):
        print(f"Database folder for {input_folder_name} already exists, deleting it.")
        os.rmdir(database_path)
    
    with os.scandir(folder_path) as entries:
        files = [(entry.name, entry.path) for entry in entries if entry.is_file()]

    for i, (_, path) in enumerate(tqdm(files, desc="Renaming images")):
        extension = os.path.splitext(path)[1]
        new_file_name = f"{i}{extension}"
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(path, new_file_path)

    print(f"Renamed {len(files)} files.")

def extract_number(filename, prefix="", sufix="", extension=".jpg" ):
    match = re.search(rf"{prefix}(\d+){sufix}{extension}", filename)
    if match:
        return int(match.group(1))
    raise ValueError(f"Filename {filename} does not match the expected pattern: {prefix}<number>{sufix}{extension}")
