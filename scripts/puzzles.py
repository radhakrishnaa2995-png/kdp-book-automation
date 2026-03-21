import random
import string

def generate_word_search(words, size=10):
    grid = [['' for _ in range(size)] for _ in range(size)]

    for word in words:
        row = random.randint(0, size-1)
        col = random.randint(0, size-len(word))
        for i, letter in enumerate(word):
            grid[row][col+i] = letter

    for i in range(size):
        for j in range(size):
            if grid[i][j] == '':
                grid[i][j] = random.choice(string.ascii_uppercase)

    return grid

def generate_words(theme):
    base_words = {
        "Farm Animals": ["COW", "GOAT", "PIG", "HEN"],
        "Fruits": ["APPLE", "MANGO", "GRAPE"],
        "Pets": ["DOG", "CAT", "FISH"]
    }
    return base_words.get(theme, ["FUN", "PLAY", "LEARN"])
