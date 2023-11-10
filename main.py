import json
from PIL import Image, ImageDraw, ImageFont
import os
import numpy


class WardrobeItem:
    def __init__(self, id, name, type, occasion, season, image_path):
        self.id = id
        self.name = name
        self.type = type
        self.occasion = occasion
        self.season = season
        self.image_path = image_path
    
    #This string representation is what is shown when I print an instance of the class, or when you use the str() function on an instance.
    def __str__(self):
        return f"{self.name} (Type: {self.type}, Occasions: {', '.join(self.occasion)}, Seasons: {', '.join(self.season)})"

#deserializing JSON data back into Python objects 
def load_wardrobe_items(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file) #parses the JSON data into Python objects
        return [WardrobeItem(**item) for item in data] #unpacking operator ** is used to unpack dictionary items into function arguments.
        #WardrobeItem(**item) creates a new instance of the WardrobeItem class.
        #**item unpacks the dictionary so that its key-value pairs are passed as keyword arguments to the WardrobeItem class's __init__ method.

def get_items_by_occasion(items, occasion):
    return [item for item in items if occasion in item.occasion]

def get_items_by_season(items, season):
    return [item for item in items if season in item.season]

collage_directory = "collage_folder"

if not os.path.exists(collage_directory):
    os.makedirs(collage_directory)

def resize_images(items):
    resized_images = []
    for item in items:
        img = Image.open(item.image_path)
        img = img.resize((1080, 1080))
        resized_images.append(img)
    return resized_images

def create_background():
    background = Image.new('RGB', (3080, 3080), 'white')
    return background

def draw_title(draw):
    font = ImageFont.truetype("ARIAL.TTF", 100)
    title = "Test"
    text_length = draw.textlength(title, font=font)
    image_width = 3080
    text_x = (image_width - text_length) / 2 
    text_y = 250
    draw.text((text_x, text_y), title, fill="black", font=font)

def place_images(items):
    images = resize_images(items)
    # Convert all images to the same mode (e.g., RGB) to ensure same number of channels
    images = [img.convert('RGB') for img in images[:4]]
    image_arrays = [numpy.array(img) for img in images]
    h1 = numpy.hstack((image_arrays[0], image_arrays[1]))
    h2 = numpy.hstack((image_arrays[2], image_arrays[3]))
    array_image = numpy.vstack((h1, h2))
    final_image = Image.fromarray(array_image)
    final_image.save(os.path.join(collage_directory, 'test.jpg'))
    return final_image

def create_collage(background, collage):
    background_width, background_height = background.size
    collage_width, collage_height = collage.size
    x = (background_width - collage_width) // 2
    y = (background_height - collage_height) // 2
    background.paste(collage, (x, y))
    return background


if __name__ == "__main__":
    season_choice = input("What's your season? Choose between: winter, spring, summer, autumn: ")
    occasion_choice = input("What's your ocassion? Choose between: everyday, business, festive: ")
    wardrobe_items = load_wardrobe_items('wardrobe.json')
    items_images = resize_images(wardrobe_items)
    season_item = get_items_by_season(wardrobe_items, season_choice)
    ocassion_item = get_items_by_occasion(wardrobe_items, occasion_choice)
    background = create_background()
    draw = ImageDraw.Draw(background)
    collage_title = draw_title(draw)
    collage = create_collage(background, place_images(wardrobe_items))
    collage_filename = "test.jpg"
    collage_path = os.path.join(collage_directory, collage_filename)
    create_collage(collage, place_images(wardrobe_items))
    collage.save(collage_path)
    collage.show()
    print(f"Collage saved to {collage_path}")


