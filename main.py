import json
from PIL import ImageDraw
import os
from collage import CollageService
from wardrobe import WardrobeService
import random

if __name__ == "__main__":
    occasion_choice = input("What's your ocassion? Choose between: everyday, business, festive: ")
    season_choice = input("What's your season? Choose between: winter, spring, summer, autumn: ")

    wardrobe_items = WardrobeService('wardrobe.json')

    selected_items_occasion = wardrobe_items.get_items_by_occasion(occasion_choice)
    selected_items_season = wardrobe_items.get_items_by_season(season_choice)
    selected_items = [item for item in selected_items_occasion if item in selected_items_season]
    shoes = wardrobe_items.get_items_by_type(selected_items, "shoes")
    bottoms = wardrobe_items.get_items_by_type(selected_items, "bottoms")
    tops = wardrobe_items.get_items_by_type(selected_items, "tops")
    jackets = wardrobe_items.get_items_by_type(selected_items, "jackets")

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

