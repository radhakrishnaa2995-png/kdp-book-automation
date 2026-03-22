from __future__ import annotations

import os
import random
import re
from dataclasses import dataclass, field
from typing import Dict, List

from theme_api import OPENROUTER_MODEL_ENV, fetch_themes, fetch_themes_from_openrouter


THEME_CATALOG: Dict[str, List[str]] = {
    "Wild Animals": ["ANTELOPE", "BADGER", "CHEETAH", "COYOTE", "GAZELLE", "HYENA", "JAGUAR", "LEOPARD", "MEERKAT", "PANTHER", "WARTHOG", "WILDBEEST"],
    "Farm Animals": ["BUFFALO", "CHICKEN", "DONKEY", "DUCKLING", "GOAT", "HORSE", "LAMB", "PIGLET", "ROOSTER", "SHEEP", "STALLION", "TURKEY"],
    "Ocean Animals": ["ANCHOVY", "DOLPHIN", "EEL", "LOBSTER", "MANATEE", "OCTOPUS", "ORCA", "SEAHORSE", "SHRIMP", "SQUID", "STARFISH", "WALRUS"],
    "Birds": ["ALBATROSS", "CANARY", "FALCON", "FLAMINGO", "HERON", "KINGFISHER", "MACAW", "OSTRICH", "PARAKEET", "PELICAN", "PUFFIN", "SPARROW"],
    "Pets": ["BETTA", "BUDGIE", "CHINCHILLA", "FERRET", "GECKO", "GERBIL", "GOLDFISH", "GUINEAPIG", "HAMSTER", "KITTEN", "PUPPY", "TERRAPIN"],
    "Insects": ["APHID", "BUMBLEBEE", "CATERPILLAR", "CRICKET", "DRAGONFLY", "EARWIG", "FIREFLY", "GRASSHOPPER", "HORNET", "LADYBUG", "MANTIS", "TERMITE"],
    "Fruits": ["APRICOT", "BLACKBERRY", "CLEMENTINE", "CRANBERRY", "FIG", "GRAPEFRUIT", "LYCHEE", "MANDARIN", "NECTARINE", "PAPAYA", "PERSIMMON", "PINEAPPLE"],
    "Vegetables": ["ARTICHOKE", "ASPARAGUS", "BEETROOT", "BROCCOLI", "CAULIFLOWER", "CUCUMBER", "EGGPLANT", "PARSNIP", "RADISH", "SPINACH", "TURNIP", "ZUCCHINI"],
    "Flowers": ["AZALEA", "BLUEBELL", "CARNATION", "DAFFODIL", "GARDENIA", "HIBISCUS", "IRIS", "JASMINE", "LAVENDER", "MAGNOLIA", "ORCHID", "PETUNIA"],
    "Trees": ["ASPEN", "BIRCH", "CEDAR", "CYPRESS", "HAZEL", "MAPLE", "POPLAR", "REDWOOD", "SEQUOIA", "SPRUCE", "WILLOW", "YEWTREE"],
    "Weather": ["BLIZZARD", "BREEZE", "CYCLONE", "DOWNPOUR", "DRIZZLE", "FORECAST", "HAILSTONE", "LIGHTNING", "MONSOON", "OVERCAST", "THUNDER", "TORNADO"],
    "Seasons": ["APRIL", "AUGUST", "AUTUMN", "FEBRUARY", "JANUARY", "JULY", "JUNE", "MARCH", "SEPTEMBER", "SOLSTICE", "SPRING", "WINTER"],
    "Space": ["ASTEROID", "COMET", "GALAXY", "JUPITER", "MERCURY", "NEBULA", "ORBIT", "PLUTO", "ROCKET", "SATURN", "TELESCOPE", "VENUS"],
    "Planets and Sky": ["AURORA", "COSMOS", "ECLIPSE", "EQUINOX", "METEOR", "MOONBEAM", "NOVA", "QUASAR", "STARLIGHT", "SUNRISE", "TWILIGHT", "ZENITH"],
    "Vehicles": ["AIRPLANE", "AMBULANCE", "BICYCLE", "BULLDOZER", "HELICOPTER", "LIMOUSINE", "MOTORBIKE", "SCOOTER", "SUBMARINE", "TRACTOR", "TRAMCAR", "YACHT"],
    "Construction Machines": ["BACKHOE", "CRANE", "DUMPER", "EXCAVATOR", "FORKLIFT", "GRADER", "PAVER", "PILEDRIVER", "ROADROLLER", "SKIDSTEER", "TRENCHER", "WRECKER"],
    "Sports": ["ARCHERY", "BADMINTON", "BASEBALL", "BOXING", "CRICKETBAT", "FENCING", "GYMNASTICS", "HANDBALL", "JUDO", "KARATE", "RUGBY", "VOLLEYBALL"],
    "Outdoor Activities": ["BACKPACKING", "CAMPING", "CANOEING", "CLIMBING", "FISHING", "HIKING", "KAYAKING", "PICNICKING", "ROWING", "SKATEBOARD", "SNORKELING", "SURFING"],
    "School Items": ["BACKPACK", "BINDER", "CALCULATOR", "CRAYON", "ERASER", "HIGHLIGHTER", "NOTEBOOK", "PENCILCASE", "PROTRACTOR", "SCISSORS", "TEXTBOOK", "WORKSHEET"],
    "Classroom Words": ["ASSEMBLY", "CAFETERIA", "CLASSROOM", "HOMEWORK", "LIBRARIAN", "PLAYGROUND", "PRINCIPAL", "RECESS", "SEMESTER", "SPELLING", "TIMETABLE", "WHITEBOARD"],
    "Professions": ["ARCHITECT", "CHEF", "DENTIST", "FIREFIGHTER", "JOURNALIST", "PARAMEDIC", "MECHANIC", "NURSE", "PHARMACIST", "PILOT", "SCIENTIST", "TEACHER"],
    "Hospital": ["AMBULATORY", "BANDAGE", "CLINIC", "DIAGNOSIS", "HEARTBEAT", "INHALER", "MEDICINE", "PATIENT", "STETHOSCOPE", "SURGEON", "SYRINGE", "THERAPY"],
    "Body Parts": ["ANKLE", "ELBOW", "EYEBROW", "FOREHEAD", "KNUCKLE", "LUNGS", "SHOULDER", "SPINE", "STOMACH", "THROAT", "THUMB", "WRIST"],
    "Clothes": ["APRON", "BLAZER", "CARDIGAN", "GLOVES", "JACKET", "OVERALLS", "PAJAMAS", "RAINCOAT", "SCARF", "SLIPPERS", "SWEATER", "TROUSERS"],
    "Accessories": ["BACKPACKSTRAP", "BARRETTE", "BRACELET", "CUFFLINK", "EARRING", "HEADBAND", "KEYCHAIN", "LOCKET", "NECKLACE", "SUNGLASSES", "UMBRELLA", "WRISTWATCH"],
    "Kitchen Items": ["BLENDER", "COLANDER", "CUTLERY", "FRYINGPAN", "KETTLE", "LADLE", "MEASURINGCUP", "MIXER", "SAUCEPOT", "SKILLET", "SPATULA", "WHISK"],
    "Baking": ["BAGUETTE", "BROWNIE", "CHEESECAKE", "CROISSANT", "CUPCAKE", "DONUT", "FROSTING", "MUFFIN", "PASTRY", "PRETZEL", "SOURDOUGH", "WAFFLE"],
    "Household Items": ["ARMCHAIR", "BOOKCASE", "CUSHION", "DOORBELL", "DRESSER", "FOOTSTOOL", "LAMPSHADE", "MATTRESS", "PAINTING", "PILLOWCASE", "RUGRUNNER", "WARDROBE"],
    "Tools": ["ANVIL", "CHISEL", "DRILLBIT", "HAMMER", "MALLET", "PLIERS", "RATCHET", "SANDER", "SCREWDRIVER", "TOOLBOX", "VISEGRIP", "WRENCH"],
    "Shapes": ["ARROWHEAD", "CRESCENT", "CUBE", "CYLINDER", "DECAGON", "HEXAGON", "OCTAGON", "OVAL", "PENTAGON", "PYRAMID", "RECTANGLE", "TRAPEZOID"],
    "Colors": ["AMBER", "AQUA", "BURGUNDY", "CHARCOAL", "CRIMSON", "EMERALD", "INDIGO", "MAGENTA", "NAVY", "SCARLET", "TURQUOISE", "VIOLET"],
    "Music": ["ACCORDION", "BAGPIPE", "CELLO", "CLARINET", "DRUMMER", "FLUTE", "HARMONICA", "MANDOLIN", "PICCOLO", "SAXOPHONE", "TROMBONE", "UKULELE"],
    "Art Supplies": ["CANVAS", "CHARCOALSTICK", "EASEL", "GLITTER", "MARKER", "PAINTBRUSH", "PALETTE", "PASTEL", "SKETCHBOOK", "STENCIL", "WATERCOLOR", "YARN"],
    "Festivals": ["BUNTING", "CARNIVAL", "FIREWORK", "GARLAND", "LANTERN", "PARADE", "PINATA", "SPARKLER", "STREAMER", "TAMBOURINE", "TICKETBOOTH", "TRADITION"],
    "Holidays": ["CHIMNEY", "GIFTWRAP", "MISTLETOE", "ORNAMENT", "PUMPKIN", "REINDEER", "SLEIGH", "SNOWFLAKE", "STOCKING", "TINSEL", "VALENTINE", "WREATH"],
    "Garden": ["COMPOST", "FLOWERBED", "GARDENHOSE", "GREENHOUSE", "HOSEPIPE", "MULCH", "PLANTER", "PRUNER", "SEEDLING", "SHOVEL", "TROWEL", "WHEELBARROW"],
    "Camping Gear": ["BINOCULARS", "CAMPFIRE", "COMPASS", "FLASHLIGHT", "HAMMOCK", "LANTERNPOST", "SLEEPINGBAG", "TARPAULIN", "TENTPEG", "THERMOS", "TRAILMAP", "WATERBOTTLE"],
    "Beach": ["BEACHTOWEL", "BUCKET", "CABANA", "DRIFTWOOD", "LIFEGUARD", "SANDCASTLE", "SEASHELL", "SHORELINE", "SUNSCREEN", "SURFBOARD", "SWIMRING", "UMBRELLASTAND"],
    "Desserts": ["BAKLAVA", "CARAMEL", "CUSTARD", "ECLAIR", "GELATO", "MACARON", "MERINGUE", "PARFAIT", "PUDDING", "SORBET", "STRUDEL", "TRUFFLE"],
    "Breakfast": ["BAGEL", "CEREAL", "GRANOLA", "HASHBROWN", "OMELET", "PANCAKE", "PORRIDGE", "SAUSAGE", "SMOOTHIE", "TOAST", "WAFFLEIRON", "YOGURT"],
    "Technology": ["ALGORITHM", "BATTERY", "BROWSER", "KEYBOARD", "LAPTOP", "MONITOR", "PASSWORD", "PRINTER", "SOFTWARE", "TABLET", "TOUCHSCREEN", "WEBCAM"],
    "Robotics": ["ANDROID", "AUTOMATION", "CIRCUIT", "GEARBOX", "GYROSCOPE", "MICROCHIP", "MOTORUNIT", "PROTOTYPE", "SENSOR", "SERVO", "SWITCHBOARD", "WIRING"],
    "Pirates": ["ANCHOR", "BANDANA", "COMPASSROSE", "CUTLASS", "GALLEON", "JOLLYROGER", "LOOKOUT", "PARROT", "PLUNDER", "SEADOG", "SPYGLASS", "TREASURE"],
    "Medieval": ["ARMOR", "BASTION", "CATAPULT", "DRAWBRIDGE", "HERALDRY", "KINGDOM", "LONGBOW", "MOAT", "SWORDSMAN", "TURRET", "VILLAGER", "YEOMAN"],
    "Dinosaurs": ["ALLOSAURUS", "ANKYLOSAURUS", "BRACHIOSAURUS", "DIPLODOCUS", "IGUANODON", "PTEROSAUR", "SAUROPOD", "SPINOSAURUS", "STEGOSAURUS", "TRICERATOPS", "TYRANNOSAUR", "VELOCIRAPTOR"],
    "Mythical Creatures": ["BASILISK", "CENTAUR", "CHIMERA", "DRAGON", "GARGOYLE", "GRIFFIN", "KRAKEN", "MERMAID", "MINOTAUR", "PEGASUS", "PHOENIX", "UNICORN"],
    "Countries": ["ARGENTINA", "BELGIUM", "CANADA", "DENMARK", "ESTONIA", "FINLAND", "GHANA", "HUNGARY", "JAMAICA", "MOROCCO", "NORWAY", "VIETNAM"],
    "Cities": ["ATHENS", "BANGKOK", "BERLIN", "CAIRO", "DUBLIN", "HOUSTON", "LISBON", "MADRID", "NAGOYA", "OSLO", "PRAGUE", "TORONTO"],
    "Landforms": ["ARCHIPELAGO", "CANYON", "CLIFFSIDE", "DELTAPLAIN", "GLACIER", "HIGHLAND", "ISLAND", "LAGOON", "MOUNTAIN", "PENINSULA", "PLATEAU", "VOLCANO"],
    "Rocks and Minerals": ["AMETHYST", "BASALT", "CRYSTAL", "EMERALDITE", "FELDSPAR", "GARNET", "GRANITE", "MARBLE", "OBSIDIAN", "QUARTZ", "TOPAZ", "TURMALINE"],
    "Transportation Hubs": ["AIRPORT", "BICYCLERACK", "BOARDINGGATE", "BUSDEPOT", "CHECKPOINT", "DOCKYARD", "HARBOR", "HELIPAD", "JUNCTION", "PLATFORM", "RUNWAY", "TERMINAL"],
    "Forest": ["ACORN", "BLUEJAY", "FERN", "FOXGLOVE", "MUSHROOM", "PINECONE", "RACCOON", "SAPLING", "SQUIRREL", "TREEHOUSE", "UNDERGROWTH", "WOODLAND"],
    "Arctic": ["AURORABEAR", "BLUBBER", "FJORD", "GLACIAL", "ICEBERG", "IGLOO", "NARWHAL", "PERMAFROST", "POLARFOX", "SEALPUP", "SNOWDRIFT", "TUNDRA"],
    "Desert": ["ARROYO", "CACTUS", "DUNES", "GILAMONSTER", "MIRAGE", "OASIS", "ROADRUNNER", "SANDSTORM", "SCORPION", "SUNSTONE", "TUMBLEWEED", "YUCCA"],
    "Jungle": ["ANACONDA", "BANANATREE", "CANOPY", "CHIMPANZEE", "GORILLA", "JAGUARUNDI", "LEMUR", "MONSOONVINE", "ORANGUTAN", "TOUCAN", "TREEFROG", "VINE"],
    "Underwater": ["BUBBLES", "CORALREEF", "DEEPSEA", "KELPFOREST", "LAGOONFISH", "PEARL", "REEFSHARK", "SANDDOLLAR", "SEAGRASS", "SHIPWRECK", "WATERCURRENT", "WHALESONG"],
    "Superheroes": ["CAPE", "EMBLEM", "GADGET", "HEADQUARTERS", "HEROIC", "JUSTICE", "MASK", "RESCUE", "SIDEKICK", "SUPERPOWER", "VILLAIN", "WINGSUIT"],
    "Magic": ["CAULDRON", "ENCHANTMENT", "FAMILIAR", "POTION", "RUNE", "SPELLBOOK", "STARWAND", "TALISMAN", "WAND", "WHISPER", "WIZARD", "ZAP"],
}


def _normalize_word(word: str) -> str:
    return re.sub(r"[^A-Z]", "", word.upper())


@dataclass
class ThemeManager:
    seed: int | None = None
    api_url: str | None = None
    openrouter_api_key: str | None = None
    openrouter_model: str | None = None
    api_batch_size: int = 24
    api_timeout: float = 30.0
    catalog: Dict[str, List[str]] = field(default_factory=lambda: {k: list(v) for k, v in THEME_CATALOG.items()})

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        self.used_themes: set[str] = set()
        self.used_words: set[str] = set()
        self.known_words: set[str] = set()
        self.openrouter_api_key = self.openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        self.openrouter_model = self.openrouter_model or os.getenv(OPENROUTER_MODEL_ENV, "openai/gpt-4o-mini")

        if self.api_url or self.openrouter_api_key:
            self.catalog = {}
        else:
            original_catalog = dict(self.catalog)
            self.catalog = {}
            self._validate_catalog(original_catalog)

    def _register_theme(self, theme: str, words: List[str]) -> None:
        if theme in self.catalog or theme in self.used_themes:
            return
        normalized = []
        for word in words:
            clean = _normalize_word(word)
            if len(clean) < 3:
                return
            if clean in self.known_words or clean in self.used_words:
                return
            normalized.append(clean)
        if len(normalized) < 10:
            return
        self.catalog[theme] = normalized
        self.known_words.update(normalized)

    def _validate_catalog(self, catalog: Dict[str, List[str]]) -> None:
        for theme, words in catalog.items():
            self._register_theme(theme, words)
        if not self.catalog:
            raise ValueError("Theme catalog is empty after validation.")

    def _ensure_dynamic_themes(self, minimum_count: int = 1) -> None:
        if not (self.api_url or self.openrouter_api_key):
            return
        available = [theme for theme in self.catalog if theme not in self.used_themes]
        if len(available) >= minimum_count:
            return

        if self.api_url:
            generated = fetch_themes(
                api_url=self.api_url,
                count=max(self.api_batch_size, minimum_count),
                min_words=10,
                max_words=12,
                excluded_themes=self.used_themes | set(self.catalog.keys()),
                excluded_words=self.used_words | self.known_words,
                timeout=self.api_timeout,
            )
        else:
            generated = fetch_themes_from_openrouter(
                count=max(self.api_batch_size, minimum_count),
                min_words=10,
                max_words=12,
                excluded_themes=self.used_themes | set(self.catalog.keys()),
                excluded_words=self.used_words | self.known_words,
                api_key=self.openrouter_api_key,
                model=self.openrouter_model,
                timeout=self.api_timeout,
            )

        for item in generated:
            self._register_theme(item.theme, item.words)

    def available_themes(self) -> List[str]:
        self._ensure_dynamic_themes()
        remaining = [theme for theme in self.catalog if theme not in self.used_themes]
        return sorted(remaining)

    def generate_unique_theme(self) -> str:
        self._ensure_dynamic_themes()
        available = self.available_themes()
        if not available:
            raise ValueError(
                "No unused themes remain. Provide a theme API URL, set OPENROUTER_API_KEY, or expand the local catalog."
            )
        theme = self.rng.choice(available)
        self.used_themes.add(theme)
        return theme

    def get_words_for_theme(self, theme: str, min_words: int = 10, max_words: int = 12) -> List[str]:
        self._ensure_dynamic_themes()
        if theme not in self.catalog:
            raise KeyError(f"Unknown theme: {theme}")

        pool = [word for word in self.catalog[theme] if word not in self.used_words]
        if len(pool) < min_words:
            raise ValueError(
                f"Theme '{theme}' does not have enough unused words for a puzzle."
            )

        target = min(len(pool), self.rng.randint(min_words, max_words))
        selected = self.rng.sample(pool, target)
        self.used_words.update(selected)
        return sorted(selected)

    def theme_count(self) -> int:
        return 1_000_000 if (self.api_url or self.openrouter_api_key) else len(self.catalog)


_DEFAULT_MANAGER = ThemeManager()


def generate_unique_theme(manager: ThemeManager | None = None) -> str:
    manager = manager or _DEFAULT_MANAGER
    return manager.generate_unique_theme()


def get_words_for_theme(
    theme: str,
    manager: ThemeManager | None = None,
    min_words: int = 10,
    max_words: int = 12,
) -> List[str]:
    manager = manager or _DEFAULT_MANAGER
    return manager.get_words_for_theme(theme, min_words=min_words, max_words=max_words)
