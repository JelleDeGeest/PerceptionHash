from clip_interrogator import Interrogator, Config
from PIL import Image

images = [
    Image.open("assets/test/test_1.png").convert("RGB"),
    Image.open("assets/test/test_2.png").convert("RGB"),
    Image.open("assets/test/test_3.png").convert("RGB"),
    Image.open("assets/test/test_4.png").convert("RGB"),
]

interrogator = Interrogator(Config(clip_model_name="ViT-L-14/openai"))

for image in images:
    print(interrogator.interrogate(image))
