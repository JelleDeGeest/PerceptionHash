from hash_methods import HASH_METHODS
from Utilities import rename_images_in_input_folder
import argparse
import json
import os

class DatabaseGenerator():
    def __init__(self, input_dir, input_dirname, workdir):
        self.input_dir = input_dir
        self.input_dirname = input_dirname
        self.workdir = workdir
        self.hash_objects = []

        self.execute()

    def execute(self):
        print("------Executing DatabaseGenerator------")
        print("Input directory name: " + self.input_dirname)
        self.generate_hash_objects()
        self.check_required_variables()
        self.generate_databases()

    def generate_hash_objects(self):
        for value in HASH_METHODS.values():
            self.hash_objects.append(value())
    
    def check_required_variables(self):
        # check that input dir exists and is contains images
        if not os.path.exists(self.input_dir):
            raise Exception("Input directory does not exist")
        if len(os.listdir(self.input_dir)) == 0:
            raise Exception("Input directory is empty")
        
        # check that the input folder has the correct naming structure
        rename_images_in_input_folder(self.input_dir, self.input_dirname)

        # check if the databases folder exists, if not create it
        self.database_path = os.path.join(self.workdir, "databases", self.input_dirname)
        if not os.path.exists(self.database_path):
            os.makedirs(self.database_path)

    def generate_databases(self):
        print("---Generating databases---")
        for hash_object in self.hash_objects:
            print("Generating database for " + hash_object.__class__.__name__)
            current_db_folder = os.path.join(self.database_path, hash_object.__class__.__name__)
            # if database folder already exists raise error
            if os.path.exists(current_db_folder):
                print(f"Database folder for {hash_object.__class__.__name__} already exists, delete it if you want to regenerate the database.")
                print(current_db_folder)
            else:
                os.mkdir(current_db_folder)
                hash_object.database_generation(self.input_dir, current_db_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A framework to generate a hash database of a specific input folder.")
    # read in Settings.json to get the input folders
    with open("Settings.json") as file:
        settings = json.load(file)

    parser.add_argument('-i', '--input', type=str, choices=settings["input_directories"].keys(), help="The folder containing the original images, you can add input folders in Settings.json")
    
    args = parser.parse_args()

    # check if the input folder is given
    if args.input is None:
        parser.error("You need to select an input folder with the -i option. Use -h for help.")
    
    databaseGenerator = DatabaseGenerator(settings["input_directories"][args.input], args.input, settings["working_directory"])
