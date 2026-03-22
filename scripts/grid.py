import random
import string

DIRECTIONS = [
    (0, 1),   # →
    (1, 0),   # ↓
    (1, 1),   # ↘
    (0, -1),  # ←
    (-1, 0),  # ↑
    (-1, -1), # ↖
]

def create_empty_grid(size):
    return [["" for _ in range(size)] for _ in range(size)]

def can_place(grid, word, row, col, dx, dy):
    size = len(grid)

    for i in range(len(word)):
        r = row + i * dx
        c = col + i * dy

        if r < 0 or r >= size or c < 0 or c >= size:
            return False

        if grid[r][c] not in ("", word[i]):
            return False

    return True

def place_word(grid, word):
    size = len(grid)
    random.shuffle(DIRECTIONS)

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

    return None

def fill_grid(grid):
    for r in range(len(grid)):
        for c in range(len(grid)):
            if grid[r][c] == "":
                grid[r][c] = random.choice(string.ascii_uppercase)

def generate_puzzle(words, size):
    grid = create_empty_grid(size)
    solutions = {}

    for word in words:
        pos = place_word(grid, word)
        if pos:
            solutions[word] = pos

    fill_grid(grid)
    return grid, solutions
