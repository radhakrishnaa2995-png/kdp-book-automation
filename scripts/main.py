import json
import random
from generator import generate_book

def load_themes():
    with open("templates/themes.json") as f:
        return json.load(f)

def main():
    themes = load_themes()

    for i in range(10):
        theme = random.choice(themes)
        file = generate_book(theme, i)
        print(f"Generated: {file}")

if __name__ == "__main__":
    main()
