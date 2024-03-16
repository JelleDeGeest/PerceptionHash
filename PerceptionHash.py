import argparse
from hash_methods import HASH_METHODS
from result_methods import RESULT_METHODS
import os
import json
from datetime import datetime
from tqdm import tqdm

class PerceptionHash:
    def __init__(self, source, input_folders, distortion_techniques, hashing_techniques, graphs, databases):
        # choose wether to load distorted images or create them
        self.source = source
        # input folder to load images
        self.input_folders = input_folders
        # techniques to check
        self.distortion_techniques = distortion_techniques
        # hashing techniques to use
        self.hashing_techniques = hashing_techniques
        # graphs to generate
        self.graphs = graphs
        # databases to use
        self.databases = databases
        # get date and time
        self.timestamp = datetime.now().strftime("%d_%m_%Y - %H_%M_%S")

        with open("Settings.json") as file:
            self.settings = json.load(file)

        self.execute()

    def execute(self):
        print("------Executing PerceptionHash------")
        print("Source: " + self.source)
        print("Input folders: " + str(self.input_folders))
        print("Distortion techniques: " + str(self.distortion_techniques))
        print("Hashing techniques: " + str(self.hashing_techniques))
        print("Graphs: " + str(self.graphs))

        self.variable_check()
        # get dictionary of folders to hash and their paths
        self.folders_to_hash = self.get_folders_to_hash()
        # get hash objects
        self.hash_objects = self.get_hash_objects()
        self.generate_graphs()
        self.generate_report()
    def variable_check(self):
        # check hashing techniques is valid
        for technique in self.hashing_techniques:
            if technique not in HASH_METHODS.keys():
                raise Exception(f"Hashing method {technique} not found in hash_methods")
        # check result methods is valid
        for graph in self.graphs:
            if graph not in RESULT_METHODS.keys():
                raise Exception(f"Graph method {graph} not found in result_methods")
        # check databases exist
        for database in self.databases:
            for technique in self.hashing_techniques:
                if not os.path.exists(os.path.join(self.settings["working_directory"],"databases", database, technique)):
                    raise Exception(f"Database for {technique} not found in {database}")
            

    def get_folders_to_hash(self):
        # if source is not load then distort images
        if self.source != "load":
            return self.distorted_images()
        
        # if source is load then check if input folders are in settings/exists and get the path
        folders_to_hash = {}
        for folder in self.input_folders:
            # check if folder is in settings
            if folder not in self.settings["input_directories"].keys():
                raise Exception(f"Input folder {folder} not found in Settings.json")
            
            # check if distorted folder exists
            distorted_folder = os.path.join(self.settings["distorted_directory"], folder)
            if not os.path.exists(distorted_folder):
                raise Exception(f"Distorted folder for {folder} not found")
            
            # Check if the selected distotions are in the distorted folder
            for technique in self.distortion_techniques:
                if not os.path.exists(os.path.join(distorted_folder, technique)):
                    raise Exception(f"Distortion technique {technique} not found in {distorted_folder}")

            folders_to_hash[folder] = distorted_folder

        return folders_to_hash

    def distort_images(self, input_folders):
        # TODO
        pass

        # if self.source == "load":
        #     pass
        # else:
        #     # TODO: Implement image distortion
        #     pass
        # distorted_folders = {}
        # for folder in self.distorted_folders:
        #     for technique in self.distortion_techniques:
        #         distorted_folders[technique] = os.path.join("assets", "distorted", folder, technique)
        # return distorted_folders
    

    def get_hash_objects(self):
        hash_objects = []
        for technique in self.hashing_techniques:
            hash_objects.append(HASH_METHODS[technique]())
            hash_objects[-1].set_database(self.databases)
        return hash_objects

    def generate_graphs(self):
        # generate graphs objects
        graph_objects = []
        print(self.folders_to_hash)
        for graph in self.graphs:
            graph_objects.append(RESULT_METHODS[graph](self.hash_objects, self.folders_to_hash))

        # create result folder with curren timestamp
        result_folder = os.path.join(self.settings["working_directory"], "results", self.timestamp)
        os.makedirs(result_folder)

        # execute graph objects
        total = len(graph_objects)
        print("\n"* 6)
        print("------------------TRACKING GRAPH PROGRESS------------------")
        print("\n\n")
        progress_bar = tqdm(total=total)
        for graph in graph_objects:
            progress_bar.set_description(f"Executing {graph.__class__.__name__}")
            graph.execute(result_folder)
            progress_bar.update(1)
        progress_bar.set_description(f"Finished")
        progress_bar.close()

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
