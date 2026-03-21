import sys
import os

# Fix path for GitHub Actions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import json
import random
from generator import generate_book


def load_themes():
    # Correct path for GitHub
    themes_path = os.path.join(BASE_DIR, "..", "templates", "themes.json")
    
    with open(themes_path) as f:
        return json.load(f)


def main():
    themes = load_themes()

    print("Themes loaded:", themes)

    for i in range(10):
        theme = random.choice(themes)
        file = generate_book(theme, i)
        print(f"Generated: {file}")


if __name__ == "__main__":
    main()
