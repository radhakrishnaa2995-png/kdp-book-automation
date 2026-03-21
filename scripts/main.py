import sys
import os

print("🔥 SCRIPT STARTED")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import json
import random
from generator import generate_book

def load_themes():
    themes_path = os.path.join(BASE_DIR, "..", "templates", "themes.json")
    print("Loading themes from:", themes_path)
    
    with open(themes_path) as f:
        return json.load(f)

def main():
    print("🔥 INSIDE MAIN FUNCTION")

    themes = load_themes()
    print("Themes loaded:", themes)

    for i in range(3):
        theme = random.choice(themes)
        file = generate_book(theme, i)
        print(f"Generated: {file}")

if __name__ == "__main__":
    main()
