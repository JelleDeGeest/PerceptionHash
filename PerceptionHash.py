import argparse
from clip_interrogator import clip_interrogator

class PerceptionHash:
    def __init__(self, method, amount, transformation, folder):
        self.method = method
        self.amount = amount
        self.transformation = transformation
        self.folder = folder

    def execute(self):
        print(f"You are testings: {self.method} by generating {self.amount} images that were edited by {self.transformation}")
        
        if self.method == "clip-interrogator":
            clip_interrogator(self.amount, self.transformation)
        # You can add more methods here in the future
        else:
            print("Method not implemented.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A framework to test/evaluate different (perceptual)hashing methods")

    parser.add_argument('-m', '--method', type=str, choices=["clip-interrogator", "none"], default="clip-interrogator", help="Method of perceptual hashing to be used")
    parser.add_argument('-a', '--amount', type=int, default=10, help="Amount of images to be edited for the test")
    parser.add_argument('-t', '--transformation', type=str, default="none", help="The type of transformation to be applied to the images")
    parser.add_argument('-f', '--folder', type=str, default="none", help="The folder where images are stored that need to be matched to the original images")
    
    args = parser.parse_args()
    
    perception_hash = PerceptionHash(args.method, args.amount, args.transformation, args.folder)
    perception_hash.execute()
