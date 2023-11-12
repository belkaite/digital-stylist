from PIL import ImageDraw
import os
from collage import CollageService
from wardrobe import WardrobeService
import random


def create_collage_selection(wardrobe_service, occasion, season, outfit_choice):
    # Get items by occasion and season first
    items_by_occasion = wardrobe_service.get_items_by_occasion(occasion)
    items_by_season = wardrobe_service.get_items_by_season(season)
    
    # Filter the items that are both in the correct season and occasion
    filtered_items = [item for item in items_by_occasion if item in items_by_season]
    
    # Initialize the final selected items list
    final_selected_items = []

    # If user chooses a dress
    if outfit_choice == 'dress':
        dresses = wardrobe_service.get_items_by_type(filtered_items, 'dresses')
        if dresses:
            final_selected_items.append(random.choice(dresses))
            # Add shoes and jackets/coats
            shoes = wardrobe_service.get_items_by_type(filtered_items, 'shoes')
            coats = wardrobe_service.get_items_by_type(filtered_items, 'coats')
            if shoes:
                final_selected_items.append(random.choice(shoes))
            if coats:
                final_selected_items.append(random.choice(coats))
        else:
            print("No dresses available for the chosen occasion and season.")

    # If user chooses a skirt or trousers
    elif outfit_choice in ['skirt', 'trousers']:
        bottoms = wardrobe_service.get_items_by_type(filtered_items, outfit_choice)
        tops = wardrobe_service.get_items_by_type(filtered_items, 'tops')
        if bottoms and tops:
            final_selected_items.append(random.choice(bottoms))
            final_selected_items.append(random.choice(tops))
            # Add shoes and jackets/coats
            shoes = wardrobe_service.get_items_by_type(filtered_items, 'shoes')
            jackets_coats = wardrobe_service.get_items_by_type(filtered_items, 'jackets') + wardrobe_service.get_items_by_type(filtered_items, 'coats')
            if shoes:
                final_selected_items.append(random.choice(shoes))
            if jackets_coats:
                final_selected_items.append(random.choice(jackets_coats))
        else:
            print("Not enough bottoms or tops available for the chosen occasion and season.")

    return final_selected_items




if __name__ == "__main__":
    occasion_choice = input("What's your occasion? Choose between: everyday, business, festive: ")
    season_choice = input("What's your season? Choose between: winter, spring, summer, autumn: ")
    outfit_choice = input("Do you want to wear a dress, skirt, or trousers? ")

    wardrobe_service = WardrobeService('wardrobe.json')
    final_selected_items = create_collage_selection(wardrobe_service, occasion_choice, season_choice, outfit_choice)




    collage_service = CollageService(final_selected_items)
    background = collage_service.create_background()
    draw = ImageDraw.Draw(background)
    collage_service.draw_title(draw,season_choice, occasion_choice)
    collage = collage_service.place_images()
    final_collage = collage_service.paste_collage(background, collage)
    collage_service.save_collage(final_collage)

