import random
import string

def generate_word_search(words, size):
    grid = [['' for _ in range(size)] for _ in range(size)]
    highlight = []

    for word in words:
        placed = False
        while not placed:
            row = random.randint(0, size-1)
            col = random.randint(0, size-len(word))

            try:
                for i in range(len(word)):
                    if grid[row][col+i] not in ('', word[i]):
                        raise Exception

                for i in range(len(word)):
                    grid[row][col+i] = word[i]
                    highlight.append((row, col+i))

                placed = True
            except:
                continue

    for i in range(size):
        for j in range(size):
            if grid[i][j] == '':
                grid[i][j] = random.choice(string.ascii_uppercase)

    return grid, highlight
