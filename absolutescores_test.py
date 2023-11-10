from my_clip_interrogator import Config, Interrogator, LabelTable, load_list
from PIL import Image
import os

ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
db = load_list("assets/db/db_absolutescore_test.txt")
table = LabelTable(db, 'terms', ci)
folder_path = os.path.join("assets", "absolutescore_test")
for file in os.listdir(folder_path):
    image_path = os.path.join(folder_path, file)
    image = Image.open(image_path).convert("RGB")
    best_match = table.rank(ci.image_to_features(image), top_count=1)[0]
    print(best_match)
