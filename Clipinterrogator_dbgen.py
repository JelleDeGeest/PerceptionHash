from PIL import Image
import os
from clip_interrogator import Config, Interrogator

# Initialize the CLIP interrogator
# ci = Interrogator(Config(clip_model_name="ViT-L-14/openai", caption_model_name="blip2-flan-t5-xl"))

# Folder containing the PNG images
folder_path = 'test/'

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.png') or filename.endswith('.jpeg'):
        # Construct the full image path
        image_path = os.path.join(folder_path, filename)
        
        # Process the image using PIL and CLIP
        image = Image.open(image_path).convert('RGB')
        ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
        outcome = ci.interrogate(image)
        
        # Open the output file in write mode
        # with open('db.txt', 'a') as outfile:

        #     # Write filename and outcome to the output file
        #     outfile.write(f"{outcome}\n")
        #     outfile.close()
        
        # Optionally, print the outcome to the console
        print(f"{filename}: {outcome}")

# for i in range(541,50000):
#     # Construct the full image path
#     image_path = os.path.join(folder_path, "R" + str(i).zfill(6) + ".jpg")
    
#     # Process the image using PIL and CLIP
#     image = Image.open(image_path).convert('RGB')
#     outcome = ci.interrogate(image)
    
#     # Open the output file in write mode with utf-8 encoding
#     with open('db_clip_interrogator.txt', 'a', encoding='utf-8') as outfile:
#         # Write filename and outcome to the output file
#         outfile.write(f"{outcome}\n")
    
#     # Optionally, print the outcome to the console
#     print(f"{i}: {outcome}")