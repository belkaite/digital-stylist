from src.wardrobe import WardrobeService, WardrobeItem
import pytest


class MockWardrobeService(WardrobeService):
    def __init__(self):
        self.wardrobe_items = [
            WardrobeItem(
                id=1,
                name="blue jeans",
                type="trousers",
                occasion=["everyday"],
                season=["winter", "autumn"],
                image_path="",
                image_source="",
            ),
            WardrobeItem(
                id=2,
                name="summer shorts",
                type="trousers",
                occasion=["everyday"],
                season=["summer"],
                image_path="",
                image_source="",
            ),
        ]


def test_get_items_by_winter_season():
    service = MockWardrobeService()
    winter_items = service.get_items_by_season("winter")
    assert len(winter_items) == 1


def test_get_items_by_summer_season():
    service = MockWardrobeService()
    summer_items = service.get_items_by_season("summer")
    assert len(summer_items) == 1


def test_get_items_by_invalid_season():
    service = MockWardrobeService()
    invalid_season_items = service.get_items_by_season("invalid-season")
    assert len(invalid_season_items) == 0


def test_get_items_by_empty_season():
    service = MockWardrobeService()
    empty_season_items = service.get_items_by_season("")
    assert len(empty_season_items) == 0
