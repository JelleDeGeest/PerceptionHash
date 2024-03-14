import argparse
import os
from PIL import Image, ImageFilter, ImageEnhance
import math
import json
from tqdm import tqdm
from Utilities import rename_images_in_input_folder


class ImageDistorter():
    def __init__(self, method, amount, input_dirname, input_dir, output):
        self.method = method
        self.amount = amount
        self.input_dirname = input_dirname
        self.input_path = input_dir
        self.output = output
        
        self.methods = {
            "rotation": self.rotate,
            "scale": self.scale,
            "blur": self.blur,
            "mirror": self.mirror,
            "distort_color": self.distort_color,
            "compression": self.compression,
            "crop_rotation": self.crop_rotation,
        }

        rename_images_in_input_folder(self.input_path)
        self.distort()


    def distort(self):
        #check if input folder contains files
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"The input folder {self.input_path}, defined in settings.json, does not exist.")
        if not os.listdir(self.input_path):
            raise FileNotFoundError(f"The folder {self.input_path}, defined in settings.json, is empty.")

        #check if output folder exists
        if not os.path.exists(self.output):
            raise FileNotFoundError(f"The file output folder {self.output}, defined in settigns.json, does not exists.")
        
        #check if output folder already exists otherwise create it
        self.output_path = os.path.join(self.output, self.input_dirname)
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        if self.method == "all":
            for method_function in self.methods.values():
                method_function()
        elif self.method in self.methods:
            self.methods[self.method]()
        else:
            raise NotImplementedError(f"The method {self.method} is not implemented yet")
        
    def get_specific_output_path(self, method):
        specific_output_path = os.path.join(self.output_path, method)
        if os.path.exists(specific_output_path):
            print(f"The output folder {specific_output_path} already exists.\n If you want to regenerate the images, please delete the folder.")
            return None
        else:
            os.makedirs(specific_output_path)
            return specific_output_path
        
    def rotate(self):
        # Read out settings to check which degrees to rotate
        with open("Settings.json") as file:
            settings = json.load(file)
        degrees = settings["distortion_settings"]["rotate"]

        for degree in degrees:
            # check if the specific output folder already exists
            specific_output_path = self.get_specific_output_path(f"rotate-{degree}")
            if specific_output_path is None:
                continue
            amount = self.amount

            # loop through the images and rotate them
            for file in tqdm(os.listdir(self.input_path),desc=f"Rotating images by {degree} degrees"):
                if amount == 0:
                    break
                file_name, file_extension = os.path.splitext(file)
                with Image.open(os.path.join(self.input_path,file)) as img:
                    
                    rotated_img = img.rotate(degree)
                    rotated_img.save(os.path.join(specific_output_path, f"{self.input_dirname}-{file_name}-rotated-{degree}{file_extension}"))
                
                amount -= 1

    def scale(self):

        with open("Settings.json") as file:
            settings = json.load(file)
        factors = settings["distortion_settings"]["scale"]


        for factor in factors:
            specific_output_path = self.get_specific_output_path(f"scale-{str(factor).replace('.','_')}")
            if specific_output_path is None:
                continue
            amount = self.amount

            for file in tqdm(os.listdir(self.input_path), desc=f"Scaling images by factor {factor}"):
                if amount == 0:
                    break
                file_name, file_extension = os.path.splitext(file)
                with Image.open(os.path.join(self.input_path, file)) as img:
                    new_size = (int(img.width * factor), int(img.height * factor))
                    scaled_img = img.resize(new_size)
                    scaled_img.save(os.path.join(specific_output_path, f"{self.input_dirname}-{file_name}-scaled_{str(factor).replace('.','_')}{file_extension}"))

                amount -= 1


    def blur(self):
        # Read out settings to check which radius to blur
        with open("Settings.json") as file:
            settings = json.load(file)
        radii = settings["distortion_settings"]["blur"]
       

        for radius in radii:
            
            specific_output_path = self.get_specific_output_path(f"blur-{radius}")
            if specific_output_path is None:
                continue
            amount = self.amount

            for file in tqdm(os.listdir(self.input_path), desc=f"Blurring images with radius {radius}"):
                if amount == 0:
                    break
                file_name, file_extension = os.path.splitext(file)
                with Image.open(os.path.join(self.input_path, file)) as img:
                    blurred_img = img.filter(ImageFilter.GaussianBlur(radius))
                    blurred_img.save(os.path.join(specific_output_path, f"{self.input_dirname}-{file_name}-blurred-{radius}{file_extension}"))

                amount -= 1

    def mirror(self):
        # Create output folder
        specific_output_path = self.get_specific_output_path("mirror")
        if specific_output_path is None:
            return
        amount = self.amount
        
        for file in tqdm(os.listdir(self.input_path), desc="Mirroring images"):
            if amount == 0:
                break
            file_name, file_extension = os.path.splitext(file)
            with Image.open(os.path.join(self.input_path, file)) as img:
                mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                mirrored_img.save(os.path.join(specific_output_path, f"{self.input_dirname}-{file_name}-mirrored{file_extension}"))

            amount -= 1

    def distort_color(self):
        with open("Settings.json") as file:
            settings = json.load(file)
        factors = settings["distortion_settings"]["color_distortion"]


        for factor in factors:
            specific_output_path = self.get_specific_output_path(f"color_distortion-{str(factor).replace('.','_')}")
            if specific_output_path is None:
                continue
            amount = self.amount

            for file in tqdm(os.listdir(self.input_path),desc=f"Distorting colors with factor {factor}"):
                if amount == 0:
                    break
                file_name, file_extension = os.path.splitext(file)
                with Image.open(os.path.join(self.input_path, file)) as img:
                    distorted_img = ImageEnhance.Color(img).enhance(factor)
                    distorted_img.save(os.path.join(specific_output_path, f"{self.input_dirname}-{file_name}-color-distorted{str(factor).replace('.','_')}{file_extension}"))

                amount -= 1

    def compression(self):
        with open("Settings.json") as file:
            settings = json.load(file)
        qualities = settings["distortion_settings"]["compression"]

        for quality in qualities:
            specific_output_path = self.get_specific_output_path(f"compression-{quality}")
            if specific_output_path is None:
                continue
            amount = self.amount

            for file in tqdm(os.listdir(self.input_path), desc=f"Compressing images with quality {quality}"):
                if amount == 0:
                    break
                file_name, file_extension = os.path.splitext(file)
                with Image.open(os.path.join(self.input_path, file)) as img:
                    img.save(os.path.join(specific_output_path, f"{self.input_dirname}-{file_name}-compressed-{quality}{file_extension}"), quality=quality)

                amount -= 1

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
        
        with open("Settings.json") as file:
            settings = json.load(file)
        degrees = settings["distortion_settings"]["crop_rotation"]

        for degree in degrees:
            specific_output_path = self.get_specific_output_path(f"crop_rotation-{degree}")
            if specific_output_path is None:
                continue
            amount = self.amount

            for file in tqdm(os.listdir(self.input_path), desc=f"Cropping and rotating images by {degree} degrees"):
                if amount == 0:
                    break
                file_name, file_extension = os.path.splitext(file)
                with Image.open(os.path.join(self.input_path, file)) as img:
                    # Rotate image with expand=True to avoid clipping
                    rotated_img = img.rotate(degree, expand=True)

                    # Mathematical cropping to remove black borders
                    rotated_img = crop_to_content(rotated_img, img.size, degree)

                    rotated_img.save(os.path.join(specific_output_path, f"{self.input_dirname}-{file_name}-croprotated-{degree}degrees{file_extension}"))
                
                amount -= 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A framework to modifiy images for the test")
    
    # read in Settings.json to get the input folders
    with open("Settings.json") as file:
        settings = json.load(file)

    parser.add_argument('-m', '--method', type=str, choices=["rotation", "scale", "blur", "mirror", "distort_color","crop_rotation", "compression", "all"], default="all", help="Distortion method to be used on the images")
    parser.add_argument('-a', '--amount', type=int, default=-1, help="Amount of images to be edited for the test")
    parser.add_argument('-i', '--input', type=str, choices=settings["input_directories"].keys(), help="The folder containing the original images, you can add input folders in Settings.json")
    
    args = parser.parse_args()
    # check if the input folder is given
    if args.input is None:
        parser.error("You need to select an input folder with the -i option. Use -h for help.")
    
    image_distorter = ImageDistorter(args.method, args.amount, args.input, settings["input_directories"][args.input], settings["distorted_directory"])
