import os
import shutil

# Define the main folder containing the images
main_folder = 'D:\\thesisdata/SimIm'
# Define the subfolders for `0` and `1`
subfolder_0 = os.path.join(main_folder, '0')
subfolder_1 = os.path.join(main_folder, '1')

# Create subfolders if they don't exist
os.makedirs(subfolder_0, exist_ok=True)
os.makedirs(subfolder_1, exist_ok=True)

# Iterate over each file in the main folder
for filename in os.listdir(main_folder):
    if filename.endswith('-0.jpg'):
        # Move to subfolder 0
        shutil.move(os.path.join(main_folder, filename), os.path.join(subfolder_0, filename.split('-')[0] + '.jpg'))
    elif filename.endswith('-1.jpg'):
        # Move to subfolder 1
        shutil.move(os.path.join(main_folder, filename), os.path.join(subfolder_1, filename.split('-')[0] + '.jpg'))

print("Images have been moved to their respective subfolders.")