import PIL

def concatenate_images(image_path1, image_path2, output_path):
    image1 = PIL.Image.open(image_path1)
    image2 = PIL.Image.open(image_path2)

    image1_width, image1_height = image1.size
    image2_width, image2_height = image2.size

    new_image = PIL.Image.new('RGB', (image1_width + image2_width, max(image1_height, image2_height)))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_width, 0))

    new_image.save(output_path)