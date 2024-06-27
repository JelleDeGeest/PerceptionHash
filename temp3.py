import os
from PIL import Image

def count_small_images(folder1, folder2, min_dimension=896):
    def check_image_size(image_path):
        with Image.open(image_path) as img:
            width, height = img.size
            return width < min_dimension or height < min_dimension

    def process_folder(folder):
        count = 0
        for filename in os.listdir(folder):
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                image_path = os.path.join(folder, filename)
                if check_image_size(image_path):
                    count += 1
        return count

    count1 = process_folder(folder1)
    count2 = process_folder(folder2)

    return count1 + count2


folder1 = "D:\\thesisdata\\Included\\1"
folder2 = "D:\\thesisdata\\Included\\2"

# Get the count of images with at least one dimension smaller than 896
total_small_images = count_small_images(folder1, folder2)

print(f"Total images with at least one dimension smaller than 896: {total_small_images}")