import random

def intro_message():
    while True:
        intro_msg = input("Ready for some chic outfit inspiration from your Digital Stylist? ✨ (Yes/Exit)").strip().lower()
        
        if intro_msg == "yes":
            break
        elif intro_msg == "exit":
            print("Exiting...See you next time! 👚")
            exit()
        else:
            print("Invalid input: Please input 'Yes' or 'Exit'")

def occasions_message(valid_occasions):
    while True:
        occasion_choice = input("1. Your occasion? Pick one: everyday, business or festive? Enter choice: ").strip().lower()
        if occasion_choice in valid_occasions:
            break
        print("Invalid choice. Please enter 'everyday', 'business' or 'festive'.")
    return occasion_choice

def seasons_message(valid_seasons):
    while True:
        season_choice = input("2. Which season are we styling for? Pick one: winter, spring, summer or autumn? Enter choice: ").strip().lower()
        if season_choice in valid_seasons:
            break
        print("Invalid choice. Please enter 'winter', 'spring', 'summer' or 'autumn'.")
    return season_choice

def preference_message(valid_preferences):
    while True:
        preference = input("3. What's your preference? Pick one: dress, skirt or trousers? Enter choice: ").strip().lower()
        if preference in valid_preferences:
            break
        print("Invalid choice. Please enter 'dress', 'skirt' or 'trousers'.")
    return preference

  
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
        shoes = wardrobe_service.get_items_by_type(filtered_items, 'shoes')
        coats = wardrobe_service.get_items_by_type(filtered_items, 'coat')

        if not dresses:
            raise ValueError("Oh no! No dresses in a wardrobe for the chosen occasion and season.")
        if not shoes:
            raise ValueError("Oh no! No suitable shoes in a wardrobe for the chosen occasion and season.")

        final_selected_items.append(random.choice(dresses))
        final_selected_items.append(random.choice(shoes))

        if coats:
            final_selected_items.append(random.choice(coats))
        else:
            print("Hmmm.. No coats in a wardrobe, but proceeding with available dress and shoes.")

    # If user chooses a skirt or trousers
    elif preference in ['skirt', 'trousers']:
        bottoms = wardrobe_service.get_items_by_type(filtered_items, preference)
        tops = wardrobe_service.get_items_by_type(filtered_items, 'top')
        shoes = wardrobe_service.get_items_by_type(filtered_items, 'shoes')

        if not bottoms:
            raise ValueError(f"Oh no! No {preference} in a wardrobe for the chosen occasion and season.")
        if not tops:
            raise ValueError("Oh no! No tops in a wardrobe for the chosen occasion and season.")
        if not shoes:
            raise ValueError("Oh no! No shoes in a wardrobe for the chosen occasion and season.")

        final_selected_items.append(random.choice(bottoms))
        final_selected_items.append(random.choice(tops))
        final_selected_items.append(random.choice(shoes))

        # Optional: Add jackets or coats if available
        jackets_coats = wardrobe_service.get_items_by_type(filtered_items, 'jacket') + wardrobe_service.get_items_by_type(filtered_items, 'coat')
        if jackets_coats:
            final_selected_items.append(random.choice(jackets_coats))
        else:
            print("Hmmm.. No coats or jackets in a wardrobe, but proceeding with available skirt/trousers and tops.")

    return final_selected_items
