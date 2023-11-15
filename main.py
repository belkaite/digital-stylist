from src.collage import CollageService
from src.wardrobe import WardrobeService
from src.utilities import (
    intro_message,
    occasions_message,
    seasons_message,
    preference_message,
    create_collage_selection,
)
from PIL import ImageDraw
import textwrap


"""
The main file for the Capsule Wardrobe program. This file orchestrates the user interaction and the overall 
workflow of generating personalized outfit collages. It leverages functions from the utilities file for user prompts 
and uses the WardrobeService and CollageService classes for creating and managing wardrobe items and collages.
"""


def select_mode() -> None:
    while True:
        print(
            """
What would you like to do next?
1. Learn more about Capsule Wardrobe
2. 🌟 Generate Capsule Wardrobe outfit for inspiration 🌟 
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


def get_learn_more() -> None:
    paragraph = """
    At the heart of the capsule wardrobe is the art of minimalism. Instead of having a wardrobe filled with once-worn items, imagine a curated collection of essential pieces that can be worn repeatedly and play well together in many stylish combos. Embracing this approach not only simplifies your daily outfit decisions but also is a way to sustainability. With a focus on timeless pieces, a capsule wardrobe is an eco-friendly fashion choice. 🌳
    """
    follow_up = "Now that you're familiar with the Capsule Wardrobe concept, let's explore the program's main feature - generate the outfit!"
    combined_text = textwrap.fill(paragraph) + "\n\n" + textwrap.fill(follow_up)

    print(combined_text)

    while True:
        next_step = (
            input("Would you like move to the main part? (Yes/Exit)").strip().lower()
        )

        if next_step == "yes":
            generate_outfits()
        elif next_step == "exit":
            print("Exiting...See you next time! 👚")
            exit()
        else:
            print("Invalid input: Please input 'Yes' or 'Exit'")


def generate_outfits() -> None:
    intro_message()

    print(
        "Let's start with three quick questions to tailor the right outfit for you..."
    )
    while True:
        valid_occasions = ["everyday", "business", "festive"]
        occasion_choice = occasions_message(valid_occasions)

        valid_seasons = ["winter", "spring", "summer", "autumn"]
        seasons_choice = seasons_message(valid_seasons)

        valid_preferences = ["dress", "skirt", "trousers"]
        preference = preference_message(valid_preferences)

        try:
            wardrobe_service = WardrobeService("wardrobe.json")
            final_selected_items = create_collage_selection(
                wardrobe_service, occasion_choice, seasons_choice, preference
            )
        except ValueError as e:
            print(f"{e}")
            print(
                "It's a quick goodbye from us – time to fix this issue. See you in a bit! 👚"
            )
            exit()
        collage_service = CollageService(
            final_selected_items, main_folder="Outfits", subfolder="Favorites"
        )
        background = collage_service.create_background()
        draw = ImageDraw.Draw(background)
        collage_service.draw_title(draw, seasons_choice, occasion_choice)
        collage = collage_service.place_images()
        final_collage = collage_service.paste_collage(background, collage)
        # collage_service.save_collage(final_collage)
        final_collage.show()

        while True:
            continue_msg = (
                input(
                    f"""
Do you like the outfit? (Yes/No): 
'Yes' - The outfit will be added to the {collage_service.subfolder} folder under the {collage_service.main_folder} folder.
'No' - The outfit will still be saved in the {collage_service.main_folder}, so you can revisit it anytime in the future!
"""
                )
                .strip()
                .lower()
            )

            if continue_msg in ["yes", "no"]:
                break
            else:
                print("Invalid input: Please enter 'Yes' or 'No'")

        if continue_msg == "yes":
            saved_path = collage_service.save_collage(final_collage, is_favorite=True)
            print(f"💌 Added to {collage_service.subfolder}: {saved_path}")
        else:
            saved_path = collage_service.save_collage(final_collage)
            print(f"✅ Added to {collage_service.main_folder}: {saved_path}")

        while True:
            new_outfit_msg = (
                input("Would you like to create another outfit? (Yes/No): ")
                .strip()
                .lower()
            )
            if new_outfit_msg in ["yes", "no"]:
                break
            else:
                print("Invalid input: Please enter 'Yes' or 'No'")

        if new_outfit_msg == "no":
            print(
                f"All set! Remember, your chic outfits are waiting in the {collage_service.main_folder} for whenever inspiration needed. See you next time! 👚"
            )
            exit()


if __name__ == "__main__":
    print("------------------------------------------------------\n")
    print("Welcome to Capsule Wardrobe: Your Digital Stylist! 👗")
    print("------------------------------------------------------\n")
    select_mode()
