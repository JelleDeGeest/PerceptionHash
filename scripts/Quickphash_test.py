# from hash_methods import Phash
import os
from PIL import Image
from perception import hashers

original = "D:\Coding\PerceptionHash/assets\phash_test/0.jpg"
resized = "D:\Coding\PerceptionHash/assets\phash_test/0.jpg_512x512.png"
attakced = "D:\Coding\PerceptionHash/assets\phash_test/0_attacked_50.png"


hasher = hashers.PHash()
hash1, hash2 = hasher.compute(attakced), hasher.compute(original)
print(hash1, hash2)
distance = hasher.compute_distance(hash1, hash2)

print(distance)




# hasher = Phash()
# hasher.set_database(["MetaTestset_1"])
# test_path = "D:\Coding\PerceptionHash/assets\phash_test"
# imgs = {}
# for name in os.listdir(test_path):
#     imgs[name] = Image.open(os.path.join(test_path, name)) 

# results = {}

# print(hasher.get_similar_images(imgs, [0.7,0.8,0.9]))




