from __future__ import annotations

import random
from typing import Dict, List


# --------------------------------------------------
# 🔹 BASE THEMES (HIGH-QUALITY DATA)
# --------------------------------------------------

BASE_THEME_CATALOG: Dict[str, List[str]] = {
    "Wild Animals": [
        "ANTELOPE","BADGER","CHEETAH","COYOTE","GAZELLE","HYENA","JAGUAR","LEOPARD","MEERKAT","PANTHER",
        "WARTHOG","WILDBEEST","GORILLA","OTTER","RACCOON","WOLF","ZEBRA","TIGER","FOX","LYNX"
    ],
    "Farm Animals": [
        "BUFFALO","CHICKEN","DONKEY","DUCKLING","GOAT","HORSE","LAMB","PIGLET","ROOSTER","SHEEP",
        "STALLION","TURKEY","COW","OX","CALF","HEN","MULE","COLT","FOAL","RAM"
    ],
    "Ocean Animals": [
        "ANCHOVY","DOLPHIN","EEL","LOBSTER","MANATEE","OCTOPUS","ORCA","SEAHORSE","SHRIMP","SQUID",
        "STARFISH","WALRUS","TUNA","SALMON","CRAB","JELLYFISH","WHALE","SEAL","CORAL","CLAM"
    ],
    "Fruits": [
        "APPLE","BANANA","MANGO","GRAPE","ORANGE","PAPAYA","PEACH","PLUM","CHERRY","KIWI",
        "LEMON","LIME","GUAVA","FIG","DATE","APRICOT","AVOCADO","COCONUT","LYCHEE","PINEAPPLE"
    ],
    "Vegetables": [
        "CARROT","POTATO","TOMATO","ONION","GARLIC","SPINACH","BROCCOLI","CABBAGE","RADISH","TURNIP",
        "CUCUMBER","PEAS","BEANS","OKRA","PUMPKIN","CAULIFLOWER","LETTUCE","CELERY","BEETROOT","ZUCCHINI"
    ],
    "Vehicles": [
        "AIRPLANE","AMBULANCE","BICYCLE","BULLDOZER","HELICOPTER","LIMOUSINE","MOTORBIKE","SCOOTER","SUBMARINE","TRACTOR",
        "TRAMCAR","YACHT","CAR","BUS","TRAIN","TRUCK","VAN","JEEP","FERRY","METRO"
    ],
    "Space": [
        "ASTEROID","COMET","GALAXY","JUPITER","MERCURY","NEBULA","ORBIT","PLUTO","ROCKET","SATURN",
        "TELESCOPE","VENUS","EARTH","MARS","URANUS","NEPTUNE","STAR","MOON","SUN","COSMOS"
    ],
    "School Items": [
        "BACKPACK","BINDER","CALCULATOR","CRAYON","ERASER","HIGHLIGHTER","NOTEBOOK","PENCILCASE","PROTRACTOR","SCISSORS",
        "TEXTBOOK","WORKSHEET","PENCIL","PEN","RULER","MARKER","BOARD","CHALK","DESK","BOOK"
    ],
    "Professions": [
        "ARCHITECT","CHEF","DENTIST","FIREFIGHTER","JOURNALIST","PARAMEDIC","MECHANIC","NURSE","PHARMACIST","PILOT",
        "SCIENTIST","TEACHER","LAWYER","ENGINEER","DOCTOR","ARTIST","DRIVER","FARMER","TAILOR","CARPENTER"
    ],
    "Colors": [
        "RED","BLUE","GREEN","YELLOW","ORANGE","PURPLE","PINK","BROWN","BLACK","WHITE",
        "GRAY","CYAN","MAGENTA","VIOLET","INDIGO","MAROON","BEIGE","OLIVE","NAVY","TEAL"
    ],
}


# --------------------------------------------------
# 🔹 AUTO EXPAND TO 100 THEMES
# --------------------------------------------------

def expand_catalog(base_catalog: Dict[str, List[str]], target_size: int = 100) -> Dict[str, List[str]]:
    expanded = dict(base_catalog)
    counter = 1

    base_items = list(base_catalog.items())

    while len(expanded) < target_size:
        for theme, words in base_items:
            new_theme = f"{theme} {counter}"

            new_words = words.copy()
            random.shuffle(new_words)

            expanded[new_theme] = new_words[:20]

            if len(expanded) >= target_size:
                break

        counter += 1

    return expanded


# 🔥 FINAL CATALOG
THEME_CATALOG: Dict[str, List[str]] = expand_catalog(BASE_THEME_CATALOG, 100)


# --------------------------------------------------
# 🔹 THEME MANAGER
# --------------------------------------------------

class ThemeManager:
    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)
        self.catalog = THEME_CATALOG
        self.used_themes = set()
        self.used_words = set()

    # ✅ FIXED (required by generator.py)
    def theme_count(self) -> int:
        return len(self.catalog)

    def generate_unique_theme(self) -> str:
        available = [t for t in self.catalog if t not in self.used_themes]

        if not available:
            raise ValueError("No themes left. Increase catalog size.")

        theme = self.rng.choice(available)
        self.used_themes.add(theme)
        return theme

    def get_words_for_theme(
        self,
        theme: str,
        min_words: int = 15,
        max_words: int = 20,
    ) -> List[str]:

        if theme not in self.catalog:
            raise KeyError(f"Unknown theme: {theme}")

        words = self.catalog[theme]

        count = self.rng.randint(min_words, max_words)
        selected = self.rng.sample(words, count)

        self.used_words.update(selected)

        return selected


# --------------------------------------------------
# 🔹 GLOBAL HELPERS (USED BY GENERATOR)
# --------------------------------------------------

_DEFAULT_MANAGER = ThemeManager()


def generate_unique_theme(manager: ThemeManager | None = None) -> str:
    manager = manager or _DEFAULT_MANAGER
    return manager.generate_unique_theme()


def get_words_for_theme(
    theme: str,
    manager: ThemeManager | None = None,
    min_words: int = 15,
    max_words: int = 20,
) -> List[str]:
    manager = manager or _DEFAULT_MANAGER
    return manager.get_words_for_theme(theme, min_words, max_words)
