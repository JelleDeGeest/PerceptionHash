import os
from clip_interrogator import Config, Interrogator, LabelTable, load_list
from PIL import Image
from Utilities import concatenate_images

class ClipInterrogator():

    def __init__(self, amount, transformation, folder):
        self.amount = amount
        self.transformation = transformation
        self.folder = folder
        self.original_folder = "meta_testset"

        self.ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
        self.db = load_list("assets/db/db_clip_interrogator_500.txt")
        self.table = LabelTable(self.db, 'terms', self.ci)
        

        self.execute()
    
    def execute(self):

        #check if folder exists
        self.folder_path = os.path.join("assets", "distorted", self.folder)
        if not os.path.exists(self.folder_path):
            raise FileNotFoundError(f"The folder {self.folder_path} does not exist.")
        
        #check if folder contains files
        if not os.listdir(self.folder_path):
            raise FileNotFoundError(f"The folder {self.folder_path} is empty.")
        
        right = 0
        wrong = 0

        for file in os.listdir(self.folder_path):
            image_path = os.path.join(self.folder_path, file)
            image = Image.open(image_path).convert("RGB")
            best_match = self.table.rank(self.ci.image_to_features(image), top_count=1)[0]

            if int(file[1:7]) == int(self.db.index(best_match)):
                right += 1
            else:
                wrong += 1
                print(f"Wrong match for {file} is {str(self.db.index(best_match))}")
                concatenate_images(image_path, os.path.join("assets", self.original_folder, f"R{str(self.db.index(best_match)).zfill(6)}.jpg"), os.path.join("assets", "wrong_matches", f"{file}_wrong_match.jpg"))
            
        print(f"Succesful matches: {right}")
        print(f"Unsuccesful matches: {wrong}")
            

