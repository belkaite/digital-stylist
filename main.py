import json
from PIL import Image, ImageDraw, ImageFont
import os


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

def load_images(items):
    return [Image.open(item.image_path) for item in items]

def create_collage_background(collage_size):
    collage = Image.new('RGB', (collage_size, collage_size + 50), 'white')
    return collage, ImageDraw.Draw(collage)

def draw_title(draw, title):
    font = ImageFont.load_default()  # Use a default font
    draw.text((10, 10), title, fill="black", font=font)

def place_images_on_collage(draw, images, collage_size, collage):
    single_image_size = collage_size // len(images)
    for i, image in enumerate(images):
        image.thumbnail((single_image_size, single_image_size))
        x = i % 2 * single_image_size
        y = 50  # Offset by the height of the title
        collage.paste(image, (x, y))
        border_color = 'black'
        border_width = 5
        draw.rectangle([x, y, x + single_image_size, y + single_image_size], outline=border_color, width=border_width)

def create_collage(items, title, occasion, collage_size=600):
    images = load_images(items)
    collage, draw = create_collage_background(collage_size)
    draw_title(draw, title)
    place_images_on_collage(draw, images, collage_size, collage)

    collage_filename = f"{title.replace(' ', '_')}_{occasion}.jpg"
    collage_path = os.path.join(collage_directory, collage_filename)
    collage.save(collage_path)
    collage.show()
    return collage_path


if __name__ == "__main__":
    season_choice = input("What's your season? Choose between: winter, spring, summer, autumn: ")
    occasion_choice = input("What's your ocassion? Choose between: everyday, business, festive: ")
    wardrobe_items = load_wardrobe_items('wardrobe.json')
    items_images = load_images(wardrobe_items)
    for img in items_images:
        print(img.size)
    season_item = get_items_by_season(wardrobe_items, season_choice)
    ocassion_item = get_items_by_occasion(wardrobe_items, occasion_choice)
    
    # Create a collage of all items for the specific occasion
    collage_path = create_collage(wardrobe_items, "My Everyday Outfit", ocassion_item)
    print(f"Collage saved to {collage_path}")


