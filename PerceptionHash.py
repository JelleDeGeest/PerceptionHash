import argparse
from hash_methods import HASH_METHODS
from result_methods import Roc, General_accuracy
import os


class PerceptionHash:
    def __init__(self, source, distorted_folders, distortion_techniques, hashing_techniques, graphs, databases):
        self.source = source
        self.distorted_folders = distorted_folders
        self.distortion_techniques = distortion_techniques
        self.hashing_techniques = hashing_techniques
        self.graphs = graphs
        self.databases = databases

        self.execute()

    def execute(self):
        print("------Executing PerceptionHash------")
        print("Source: " + self.source)
        print("Distorted folders: " + str(self.distorted_folders))
        print("Distortion techniques: " + str(self.distortion_techniques))
        print("Hashing techniques: " + str(self.hashing_techniques))
        print("Graphs: " + str(self.graphs))

        self.distorted_images_folders = self.distort_images()
        print(self.distorted_images_folders)
        self.hash_objects = self.get_hash_objects()
        self.generate_graphs()
        self.generate_report()


    def distort_images(self):
        if self.source == "load":
            pass
        else:
            # TODO: Implement image distortion
            pass
        distorted_folders = {}
        for folder in self.distorted_folders:
            for technique in self.distortion_techniques:
                distorted_folders[technique] = os.path.join("assets", "distorted", folder, technique)
        return distorted_folders
    

    def get_hash_objects(self):
        hash_objects = []
        for technique in self.hashing_techniques:
            hash_objects.append(HASH_METHODS[technique]())
        return hash_objects

    def generate_graphs(self):
        for graph in self.graphs:
            if graph == "roc":
                Roc(self.hash_objects)
            elif graph == "general_accuracy":
                General_accuracy(self.hash_objects)
            else:
                print("Graph not recognized")

    def generate_report(self):
        # generate html report
        pass

        

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="A framework to test/evaluate different (perceptual)hashing methods")

#     parser.add_argument('-m', '--method', type=str, choices=["clip-interrogator", "none"], default="clip-interrogator", help="Method of perceptual hashing to be used")
#     parser.add_argument('-a', '--amount', type=int, default=10, help="Amount of images to be edited for the test")
#     parser.add_argument('-t', '--transformation', type=str, default="none", help="The type of transformation to be applied to the images")
#     parser.add_argument('-f', '--folder', type=str, default="none", help="The folder where images are stored that need to be matched to the original images")
    
#     args = parser.parse_args()
    
#     perception_hash = PerceptionHash(args.method, args.amount, args.transformation, args.folder)
