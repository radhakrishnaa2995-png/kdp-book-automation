import random
import string

DIRECTIONS = [
    (0, 1),   # right
    (1, 0),   # down
    (1, 1),   # diagonal
    (-1, 1),  # up-right
]

def can_place(grid, word, row, col, dx, dy):
    for i in range(len(word)):
        r = row + i * dx
        c = col + i * dy

        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid):
            return False

        if grid[r][c] not in ("", word[i]):
            return False

    return True


def place_word(grid, word):
    size = len(grid)

    for _ in range(100):
        dx, dy = random.choice(DIRECTIONS)
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)

        if can_place(grid, word, row, col, dx, dy):
            positions = []
            for i in range(len(word)):
                r = row + i * dx
                c = col + i * dy
                grid[r][c] = word[i]
                positions.append((r, c))
            return positions

    return []


def generate_grid(words, size):
    grid = [["" for _ in range(size)] for _ in range(size)]
    highlights = []

    for word in words:
        pos = place_word(grid, word)
        highlights.extend(pos)

    # Fill blanks
    for i in range(size):
        for j in range(size):
            if grid[i][j] == "":
                grid[i][j] = random.choice(string.ascii_uppercase)

    return grid, highlights
