import json

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

class WardrobeService:
    def __init__(self, filepath):
        self.wardrobe_items = self.load_wardrobe_items(filepath)

    def load_wardrobe_items(self, filepath):
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                if not data:
                    raise ValueError("Oops..The wardrobe file is empty.")
                return [WardrobeItem(**item) for item in data]
        except json.JSONDecodeError:
            raise ValueError("Oops.. JSON file is not in the correct format or empty.")
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {filepath} was not found.")


    def get_items_by_occasion(self, occasion):
        return [item for item in self.wardrobe_items if occasion in item.occasion]

    def get_items_by_season(self, season):
        return [item for item in self.wardrobe_items if season in item.season]

    def get_items_by_type(self, items, type):
        return [item for item in items if type == item.type]