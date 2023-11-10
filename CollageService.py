from PIL import Image, ImageFont
import numpy
import os

class CollageService:
    def __init__(self, items, background_size=(3080, 3080), title="Test", collage_directory = "collage_folder"):
        self.items = items
        self.background_size = background_size
        self.title = title
        self.collage_directory = collage_directory
        if not os.path.exists(collage_directory):
            os.makedirs(collage_directory)

    def create_background(self):
        background = Image.new('RGB', self.background_size, 'white')
        return background

    def draw_title(self, draw):
        font = ImageFont.truetype("ARIAL.TTF", 100)
        title = self.title
        text_length = draw.textlength(title, font=font)
        image_width = self.background_size[0]
        text_x = (image_width - text_length) / 2 
        text_y = 250
        draw.text((text_x, text_y), title, fill="black", font=font)

    def resize_images(self):
        resized_images = []
        for item in self.items:
            img = Image.open(item.image_path)
            img = img.resize((1080, 1080))
            resized_images.append(img)
        return resized_images

    def place_images(self):
        images = self.resize_images()
        # Convert all images to the same mode (e.g., RGB) to ensure same number of channels
        images = [img.convert('RGB') for img in images[:4]]
        image_arrays = [numpy.array(img) for img in images]
        h1 = numpy.hstack((image_arrays[0], image_arrays[1]))
        h2 = numpy.hstack((image_arrays[2], image_arrays[3]))
        array_image = numpy.vstack((h1, h2))
        final_image = Image.fromarray(array_image)
        final_image.save(os.path.join(self.collage_directory, 'test.jpg'))
        return final_image

    def paste_collage(self, background, collage):
        background_width, background_height = background.size
        collage_width, collage_height = collage.size
        x = (background_width - collage_width) // 2
        y = (background_height - collage_height) // 2
        background.paste(collage, (x, y))
        return background

