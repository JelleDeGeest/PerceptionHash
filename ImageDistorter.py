import argparse
import os
from PIL import Image, ImageFilter, ImageEnhance
import math



class ImageDistorter():
    def __init__(self, method, amount, input, output):
        self.method = method
        self.amount = amount
        self.input = input
        self.output = output
        self.distort()
    
    def distort(self):
        
        #check if input folder contains files
        self.input_path = os.path.join("assets", self.input)
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"The folder {self.input_path} does not exist.")
        if not os.listdir(self.input_path):
            raise FileNotFoundError(f"The folder {self.input_path} is empty.")

        #check if output folder exists
        self.output_path = os.path.join("assets", "distorted/test", self.output)
        if os.path.exists(self.output_path):
            raise FileExistsError(f"The file {self.output_path} already exists.")

        if self.method == "rotation":
            self.rotate()
        elif self.method == "scale":
            self.scale()
        elif self.method == "blur":
            self.blur()
        elif self.method == "mirror":
            self.mirror()
        elif self.method == "distort_color":
            self.distort_color()
        elif self.method == "compression":
            self.compression()
        elif self.method == "crop_rotation":
            self.crop_rotation()
        else:
            raise NotImplementedError("The method {} is not implemented yet".format(self.method))

        
    def rotate(self):

        degrees = input("Degrees to rotate the image: ")
        if not degrees.isdigit():
            raise ValueError("The input is not a number")
        degrees = int(degrees)
        if degrees < 0 or degrees > 360:
            raise ValueError("The input is not a valid degree")
        
        #create output folder
        os.mkdir(self.output_path)

        for file in os.listdir(self.input_path):
            if self.amount == 0:
                break
            file_name, file_extension = os.path.splitext(file)
            with Image.open(os.path.join(self.input_path,file)) as img:
                
                rotated_img = img.rotate(degrees)
                rotated_img.save(os.path.join(self.output_path, f"{file_name}_rotated_{degrees}degrees{file_extension}"))
            
            self.amount -= 1

    def scale(self):

        factor = input("Scaling factor (e.g., 150 for 150%): ")
        try:
            factor = int(factor)
        except ValueError:
            raise ValueError("The input is not a valid number")
        if factor < 0 or factor > 200:
            raise ValueError("The input is not a valid number")
        
        factor = factor / 100

        # Create output folder
        os.makedirs(self.output_path, exist_ok=True)

        for file in os.listdir(self.input_path):
            if self.amount == 0:
                break
            file_name, file_extension = os.path.splitext(file)
            with Image.open(os.path.join(self.input_path, file)) as img:
                new_size = (int(img.width * factor), int(img.height * factor))
                scaled_img = img.resize(new_size)
                scaled_img.save(os.path.join(self.output_path, f"{file_name}_scaled_{factor}{file_extension}"))

            self.amount -= 1

    def blur(self):
        radius = input("Blur radius (e.g., 2 for mild blur): ")
        try:
            radius = float(radius)
        except ValueError:
            raise ValueError("The input is not a valid number")

        # Create output folder
        os.makedirs(self.output_path, exist_ok=True)

        for file in os.listdir(self.input_path):
            if self.amount == 0:
                break
            file_name, file_extension = os.path.splitext(file)
            with Image.open(os.path.join(self.input_path, file)) as img:
                blurred_img = img.filter(ImageFilter.GaussianBlur(radius))
                blurred_img.save(os.path.join(self.output_path, f"{file_name}_blurred_{radius}{file_extension}"))

            self.amount -= 1
    def mirror(self):
        # Create output folder
        os.makedirs(self.output_path, exist_ok=True)

        for file in os.listdir(self.input_path):
            if self.amount == 0:
                break
            file_name, file_extension = os.path.splitext(file)
            with Image.open(os.path.join(self.input_path, file)) as img:
                mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                mirrored_img.save(os.path.join(self.output_path, f"{file_name}_mirrored{file_extension}"))

            self.amount -= 1
    
    def distort_color(self):
        factor = input("Color distortion factor (e.g., 1.5 for 150%) between 0-1: ")
        try:
            factor = float(factor)
        except ValueError:
            raise ValueError("The input is not a valid number")
        # Create output folder
        os.makedirs(self.output_path, exist_ok=True)

        for file in os.listdir(self.input_path):
            if self.amount == 0:
                break
            file_name, file_extension = os.path.splitext(file)
            with Image.open(os.path.join(self.input_path, file)) as img:
                distorted_img = ImageEnhance.Color(img).enhance(factor)
                # Distort the color of the image
                distorted_img.save(os.path.join(self.output_path, f"{file_name}_distorted_color{file_extension}"))
    def compression(self):
        quality = input("Compression quality (e.g., 50 for 50%): ")
        try:
            quality = int(quality)
        except ValueError:
            raise ValueError("The input is not a valid number")
        if quality < 0 or quality > 100:
            raise ValueError("The input is not a valid number")

        # Create output folder
        os.makedirs(self.output_path, exist_ok=True)

        for file in os.listdir(self.input_path):
            if self.amount == 0:
                break
            file_name, file_extension = os.path.splitext(file)
            with Image.open(os.path.join(self.input_path, file)) as img:
                img.save(os.path.join(self.output_path, f"{file_name}_compressed_{quality}{file_extension}"), quality=quality)

            self.amount -= 1
    
    def crop_rotation(self):
        def crop_to_content( img, original_size, degrees):
            # Image dimensions and radians
            width, height = original_size
            radians = math.radians(degrees)

            # Calculate the width and height of the rotated image
            cos_angle = abs(math.cos(radians))
            sin_angle = abs(math.sin(radians))
            new_width = int(height * sin_angle + width * cos_angle)
            new_height = int(height * cos_angle + width * sin_angle)

            # Calculate the width and height of the crop box
            original_diag = math.sqrt(width ** 2 + height ** 2)
            scale_factor = min(new_width, new_height) / original_diag
            crop_width = int(width * scale_factor)
            crop_height = int(height * scale_factor)

            # Calculate the position of the crop box
            x0 = (new_width - crop_width) // 2
            y0 = (new_height - crop_height) // 2
            x1 = x0 + crop_width
            y1 = y0 + crop_height

            # Crop the image
            cropped_img = img.crop((x0, y0, x1, y1))
            return cropped_img
        
        degrees = input("Degrees to rotate the image: ")
        if not degrees.isdigit():
            raise ValueError("The input is not a number")
        degrees = int(degrees)
        if degrees < 0 or degrees > 360:
            raise ValueError("The input is not a valid degree")

        # Create output folder if it doesn't exist
        os.makedirs(self.output_path, exist_ok=True)

        for file in os.listdir(self.input_path):
            if self.amount == 0:
                break
            file_name, file_extension = os.path.splitext(file)
            with Image.open(os.path.join(self.input_path, file)) as img:
                # Rotate image with expand=True to avoid clipping
                rotated_img = img.rotate(degrees, expand=True)

                # Mathematical cropping to remove black borders
                rotated_img = crop_to_content(rotated_img, img.size, degrees)

                rotated_img.save(os.path.join(self.output_path, f"{file_name}_croprotated_{degrees}degrees{file_extension}"))
            
            self.amount -= 1


    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A framework to modifiy images for the test")

    parser.add_argument('-m', '--method', type=str, choices=["rotation", "scale", "blur", "mirror", "distort_color","crop_rotation", "compression"], default="rotation", help="Distortion method to be used on the images")
    parser.add_argument('-a', '--amount', type=int, default=-1, help="Amount of images to be edited for the test")
    parser.add_argument('-i', '--input', type=str, default="none", help="The folder containing the original images")
    parser.add_argument('-o', '--output', type=str, default="none", help="The folder to store the edited images in")
    
    args = parser.parse_args()
    
    image_distorter = ImageDistorter(args.method, args.amount, args.input, args.output)
