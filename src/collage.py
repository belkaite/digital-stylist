from PIL import Image, ImageFont, ImageDraw
import numpy
import os
from datetime import datetime
from src.wardrobe import WardrobeItem
from typing import List, Tuple


class CollageService:
    """
    Provides functionality for creating a collage from a list of WardrobeItem objects.
    It has operations such as creating a background of the collage, drawing a title on it, resizing images,
    generating a collage (create_blank_image, place_images, paste_collage functions) and saving the final output.
    """

    def __init__(
        self,
        items: List[WardrobeItem],
        main_folder: str,
        subfolder: str,
        background_size: Tuple[int, int] = (3080, 3080),
    ) -> None:
        self.items = items
        self.main_folder = main_folder
        self.subfolder = subfolder
        self.background_size = background_size

    def create_background(self) -> Image.Image:
        background = Image.new("RGB", self.background_size, "white")
        return background

    def draw_title(self, draw: ImageDraw.Draw, season: str, occasion: str) -> None:
        font = ImageFont.truetype("ARIAL.TTF", 100)
        title = f"Your outfit for {occasion} occasion in {season}"
        text_length = draw.textlength(title, font=font)
        image_width = self.background_size[0]
        text_x = (image_width - text_length) / 2
        text_y = 250
        draw.text((text_x, text_y), title, fill="black", font=font)

    def resize_images(self) -> List[Image.Image]:
        resized_images = []
        for item in self.items:
            img = Image.open(item.image_path)
            img = img.resize((1080, 1080))
            resized_images.append(img)
        return resized_images

    def create_blank_image(
        self,
        size: Tuple[int, int] = (1080, 1080),
        color: Tuple[int, int, int] = (255, 255, 255),
    ) -> Image.Image:
        blank = Image.new("RGB", size, color)
        return blank

    def place_images(self) -> Image.Image:
        images = self.resize_images()
        images = [img.convert("RGB") for img in images]

        while len(images) < 4:
            images.append(self.create_blank_image())

        image_arrays = [numpy.array(img) for img in images]
        h1 = numpy.hstack((image_arrays[0], image_arrays[1]))
        h2 = numpy.hstack((image_arrays[2], image_arrays[3]))
        array_image = numpy.vstack((h1, h2))
        collage = Image.fromarray(array_image)
        return collage

    def paste_collage(
        self, background: Image.Image, collage: Image.Image
    ) -> Image.Image:
        background_width, background_height = background.size
        collage_width, collage_height = collage.size
        x = (background_width - collage_width) // 2
        y = (background_height - collage_height) // 2
        background.paste(collage, (x, y))
        return background

    def save_collage(
        self, final_collage: Image.Image, is_favorite: bool = False
    ) -> str:
        main_directory = self.main_folder
        subdirectory = self.subfolder if is_favorite else ""

        collage_directory = os.path.join(main_directory, subdirectory)
        if not os.path.exists(collage_directory):
            os.makedirs(collage_directory)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"collage_{timestamp}.jpg"
        final_collage_path = os.path.join(collage_directory, unique_filename)

        final_collage.save(final_collage_path)

        return final_collage_path
