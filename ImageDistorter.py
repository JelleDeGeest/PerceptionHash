import argparse
import os
from PIL import Image, ImageFilter



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
        self.output_path = os.path.join("assets", "distorted", self.output)
        if os.path.exists(self.output_path):
            raise FileExistsError(f"The file {self.output_path} already exists.")

        if self.method == "rotation":
            self.rotate()
        elif self.method == "scale":
            self.scale()
        elif self.method == "blur":
            self.blur()
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

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A framework to test/evaluate different (perceptual)hashing methods")

    parser.add_argument('-m', '--method', type=str, choices=["rotation", "scale", "blur"], default="rotation", help="Distortion method to be used on the images")
    parser.add_argument('-a', '--amount', type=int, default=-1, help="Amount of images to be edited for the test")
    parser.add_argument('-i', '--input', type=str, default="none", help="The folder containing the original images")
    parser.add_argument('-o', '--output', type=str, default="none", help="The folder to store the edited images in")
    
    args = parser.parse_args()
    
    image_distorter = ImageDistorter(args.method, args.amount, args.input, args.output)
