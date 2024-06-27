from hash_methods import HASH_METHODS

hasher = HASH_METHODS["vit"]
hasher = hasher()
print(hasher.calculate_similarity_between_2("assets/test/Similar_image_example_3.png", "assets/test/Similar_image_example_5.png"))