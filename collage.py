from PIL import Image, ImageFont
import numpy
import os
from datetime import datetime

class CollageService:
    def __init__(self, items, main_folder, subfolder, background_size=(3080, 3080)):
        self.items = items
        self.main_folder = main_folder
        self.subfolder = subfolder
        self.background_size = background_size

    def create_background(self):
        background = Image.new('RGB', self.background_size, 'white')
        return background

    def draw_title(self, draw, season, occasion):
        font = ImageFont.truetype("ARIAL.TTF", 100)
        title = f"Your outfit for {occasion} occasion in {season}"
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
    
    def create_blank_image(self, size=(1080, 1080), color=(255, 255, 255)):
        blank = Image.new('RGB', size, color)
        return blank

    def place_images(self):
        images = self.resize_images()
        images = [img.convert('RGB') for img in images]  # Convert all images to the same mode (e.g., RGB) to ensure same number of channels

        while len(images) < 4:
            images.append(self.create_blank_image())
       
        image_arrays = [numpy.array(img) for img in images]
        h1 = numpy.hstack((image_arrays[0], image_arrays[1]))
        h2 = numpy.hstack((image_arrays[2], image_arrays[3]))
        array_image = numpy.vstack((h1, h2))
        collage = Image.fromarray(array_image)
        return collage

    def paste_collage(self, background, collage):
        background_width, background_height = background.size
        collage_width, collage_height = collage.size
        x = (background_width - collage_width) // 2
        y = (background_height - collage_height) // 2
        background.paste(collage, (x, y))
        return background
    
    def save_collage(self, final_collage, is_favorite=False):
        main_directory = self.main_folder
        subdirectory = self.subfolder if is_favorite else ""



        collage_directory = os.path.join(main_directory, subdirectory) 
        if not os.path.exists(collage_directory):
            os.makedirs(collage_directory)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"collage_{timestamp}.jpg"
        final_collage_path = os.path.join(collage_directory, unique_filename)
    
        final_collage.save(final_collage_path)
    
        return final_collage_path

    

        

