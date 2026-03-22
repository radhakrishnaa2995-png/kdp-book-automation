from __future__ import annotations
from typing import Dict, List, Tuple

from .grid import generate_puzzle

Coordinate = Tuple[int, int]


class WordPlacement:
    def __init__(self, word: str, positions: List[Coordinate]):
        self.word = word
        self.positions = positions


class Puzzle:
    def __init__(self, grid: List[List[str]], placements: Dict[str, List[Coordinate]]):
        self.grid = grid
        self.placements = placements


def generate_word_search(
    words,
    size,
    theme: str = "Word Search",
    seed: int | None = None,
):
    """
    Generates a word search puzzle and returns:
    - grid (2D list)
    - highlight positions (flattened list)
    """

    grid, placements = generate_puzzle(
        words,
        size=size,
        theme=theme,
        seed=seed,
    )

    # Flatten all word positions for highlighting
    highlight = [
        position
        for coords in placements.values()
        for position in coords
    ]

    return grid, highlight


__all__ = [
    "Puzzle",
    "WordPlacement",
    "generate_word_search",
]
