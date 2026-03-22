from __future__ import annotations

from .grid import generate_puzzle



def generate_word_search(words, size, theme: str = "Word Search", seed: int | None = None):
    grid, placements = generate_puzzle(words, size=size, theme=theme, seed=seed)
    highlight = [position for coords in placements.values() for position in coords]
    return grid, highlight
