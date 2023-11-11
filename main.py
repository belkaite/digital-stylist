import json
from PIL import ImageDraw
import os
from CollageService import CollageService
import random


class WardrobeItem:
    def __init__(self, id, name, type, occasion, season, image_path, image_source):
        self.id = id
        self.name = name
        self.type = type
        self.occasion = occasion
        self.season = season
        self.image_path = image_path
        self.image_source = image_source
    
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

def get_items_by_type(items, type):
    return [item for item in items if type == item.type]


if __name__ == "__main__":
    occasion_choice = input("What's your ocassion? Choose between: everyday, business, festive: ")
    season_choice = input("What's your season? Choose between: winter, spring, summer, autumn: ")

    wardrobe_items = load_wardrobe_items('wardrobe.json')

    selected_items_occasion = get_items_by_occasion(wardrobe_items, occasion_choice)
    selected_items_season = get_items_by_season(wardrobe_items, season_choice)
    selected_items = [item for item in selected_items_occasion if item in selected_items_season]
    shoes = get_items_by_type(selected_items, "shoes")
    bottoms = get_items_by_type(selected_items, "bottoms")
    tops = get_items_by_type(selected_items, "tops")
    jackets = get_items_by_type(selected_items, "jackets")

    final_selected_items = []
    for type in [shoes, bottoms, tops, jackets]:
        if type != []:  
            final_selected_items.append(random.choice(type))
        else:
            print(f"Not enough items in the category.")
    
    if len(final_selected_items) < 4:
        print("Not enough items for each category. ")


    collage_service = CollageService(final_selected_items)
    background = collage_service.create_background()
    draw = ImageDraw.Draw(background)
    collage_service.draw_title(draw)
    collage = collage_service.place_images()
    final_collage = collage_service.paste_collage(background, collage)
    collage_filename = "test.jpg"
    collage_path = os.path.join(collage_service.collage_directory, collage_filename)
    final_collage.save(collage_path)
    final_collage.show()
    print(f"Collage saved to {collage_path}")

