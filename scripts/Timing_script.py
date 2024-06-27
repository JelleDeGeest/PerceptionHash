from perception.hashers import PHash, PDQHash, DHash
import timeit
import numpy as np
from PIL import Image


def test(hashes, hasher_name):
    hasher = hashes
    image_path1 = 'assets/test/Similar_image_example_5.png'
    image_path2 = 'assets/test/Similar_image_example_3.png'

    # Load images and convert to RGB
    image1 = Image.open(image_path1).convert('RGB')
    image2 = Image.open(image_path2).convert('RGB')

    hash1 = hasher.compute(image1)
    hash2 = hasher.compute(image2)
    print(hash1)

    # Measure the time taken to generate the hashes and calculate variance
    timings = [timeit.timeit(lambda: hasher.compute_isometric(image1), number=1) for _ in range(10)]
    mean_time = np.mean(timings)
    variance = np.var(timings)

    print(f"Time taken to generate hash for image 1 {hasher_name}: {mean_time} seconds")
    print(f"Variance of time taken to generate hash for image 1 {hasher_name}: {variance}")

    # Measure the time taken to calculate the distance
    distance_time = timeit.timeit(lambda: hasher.compute_distance(hash1, hash2), number=100000) / 100000
    distance = hasher.compute_distance(hash1, hash2)
    print(f"Time taken to calculate distance {hasher_name}: {distance_time} seconds")

lijst = [ (PDQHash(), 'PDQHash')]
# lijst = [ (PHash(), 'PHash'), (PHash(hash_size=12), 'PHash_144'), (PHash(hash_size=16), 'PHash_256') ]
for hash, name in lijst:
    test(hash, name)