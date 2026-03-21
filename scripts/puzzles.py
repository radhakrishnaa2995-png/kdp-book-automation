import random

# 🧠 Sudoku generator (simple)
def generate_sudoku():
    return [[random.randint(1, 9) for _ in range(9)] for _ in range(9)]

# 🔢 Dot-to-dot
def generate_dot_to_dot():
    return list(range(1, 21))

# 🎨 Coloring prompts
def generate_coloring():
    prompts = [
        "Color a happy elephant",
        "Color a big mango",
        "Color a cute puppy"
    ]
    return random.choice(prompts)
