from PIL import ImageDraw
from collage import CollageService
from wardrobe import WardrobeService
import random
import textwrap


def select_mode():
    while True:

        print(
    """
What would you like to do next?
1. Learn more about Capsule Wardrobe
2. Generate Capsule Wardrobe outfit for inspo
3. Exit
""",
            end="",
        )

        mode_type = input("Enter your choice (1-3): ")

        if mode_type == "1":
            get_learn_more()
            break
        elif mode_type == "2":
            generate_outfits()
            break
        elif mode_type == "3":
            print("Exiting...See you next time! 👚")
            exit()
        else:
            print("Error: please choose a valid option.")

def get_learn_more():
    paragraph = """
    At the heart of the capsule wardrobe is the art of minimalism. Instead of having a wardrobe filled with once-worn items, imagine a curated collection of essential pieces that can be worn repeatedly and play well together in many stylish combos. Embracing this approach not only simplifies your daily outfit decisions but also is a way to sustainability. With a focus on timeless pieces, a capsule wardrobe is an eco-friendly fashion choice. 🌳
    """
    follow_up = "Now that you're familiar with the Capsule Wardrobe concept, let's explore the program's main feature - generate the outfit!"
    combined_text = textwrap.fill(paragraph) + "\n\n" + textwrap.fill(follow_up)
    
    print(combined_text)
    
    while True:
        next_step = input("Would you like move to the main part? (Yes/Exit)").strip().lower()
        
        if next_step == "yes":
            generate_outfits()
        elif next_step == "exit":
            print("Exiting...See you next time! 👚")
            exit()
        else:
            print("Invalid input: Please input 'Yes' or 'Exit'")
    
def create_collage_selection(wardrobe_service, occasion, season, preference):
    # Get items by occasion and season first
    items_by_occasion = wardrobe_service.get_items_by_occasion(occasion)
    items_by_season = wardrobe_service.get_items_by_season(season)
    
    # Filter the items that are both in the correct season and occasion
    filtered_items = [item for item in items_by_occasion if item in items_by_season]
    
    # Initialize the final selected items list
    final_selected_items = []

    # If user chooses a dress
    if preference == 'dress':
        dresses = wardrobe_service.get_items_by_type(filtered_items, 'dress')
        if dresses:
            final_selected_items.append(random.choice(dresses))
            # Add shoes and jackets/coats
            shoes = wardrobe_service.get_items_by_type(filtered_items, 'shoes')
            coats = wardrobe_service.get_items_by_type(filtered_items, 'coat')
            if shoes:
                final_selected_items.append(random.choice(shoes))
            if coats:
                final_selected_items.append(random.choice(coats))
        else:
            print("No dresses available for the chosen occasion and season.")

    # If user chooses a skirt or trousers
    elif preference in ['skirt', 'trousers']:
        bottoms = wardrobe_service.get_items_by_type(filtered_items, preference)
        tops = wardrobe_service.get_items_by_type(filtered_items, 'top')
        if bottoms and tops:
            final_selected_items.append(random.choice(bottoms))
            final_selected_items.append(random.choice(tops))
            # Add shoes and jackets/coats
            shoes = wardrobe_service.get_items_by_type(filtered_items, 'shoes')
            jackets_coats = wardrobe_service.get_items_by_type(filtered_items, 'jacket') + wardrobe_service.get_items_by_type(filtered_items, 'coat')
            if shoes:
                final_selected_items.append(random.choice(shoes))
            if jackets_coats:
                final_selected_items.append(random.choice(jackets_coats))
        else:
            print("Not enough bottoms or tops available for the chosen occasion and season.")

    return final_selected_items

def generate_outfits():

    while True:
        intro_msg = input("Ready for some chic outfit inspiration from your Digital Stylist? ✨ (Yes/Exit)").strip().lower()
        
        if intro_msg == "yes":
            break
        elif intro_msg == "exit":
            print("Exiting...See you next time! 👚")
            exit()
        else:
            print("Invalid input: Please input 'Yes' or 'Exit'")

    print("Let's start with three quick questions to tailor the right outfit for you...")
    valid_occasions = ['everyday', 'business', 'festive']
    while True:
        occasion_choice = input("1. Your occasion? Pick one: everyday, business or festive? Enter choice: ").strip().lower()
        if occasion_choice in valid_occasions:
            break
        print("Invalid choice. Please enter 'everyday', 'business' or 'festive'.")

    valid_seasons = ['winter', 'spring', 'summer', 'autumn']
    while True:
        season_choice = input("2. Which season are we styling for? Pick one: winter, spring, summer or autumn? Enter choice: ").strip().lower()
        if season_choice in valid_seasons:
            break
        print("Invalid choice. Please enter 'winter', 'spring', 'summer' or 'autumn'.")

    valid_preferences = ['dress', 'skirt', 'trousers']
    while True:
        preference = input("3. What's your preference? Pick one: dress, skirt or trousers? Enter choice: ").strip().lower()
        if preference in valid_preferences:
            break
        print("Invalid choice. Please enter 'dress', 'skirt' or 'trousers'.")


    wardrobe_service = WardrobeService('wardrobe.json')
    final_selected_items = create_collage_selection(wardrobe_service, occasion_choice, season_choice, preference)




    collage_service = CollageService(final_selected_items)
    background = collage_service.create_background()
    draw = ImageDraw.Draw(background)
    collage_service.draw_title(draw,season_choice, occasion_choice)
    collage = collage_service.place_images()
    final_collage = collage_service.paste_collage(background, collage)
    collage_service.save_collage(final_collage)



if __name__ == "__main__":
    print("Welcome to Capsule Wardrobe: Your Digital Stylist! 👗")
    print("------------------------------------------------------\n")
    select_mode()
