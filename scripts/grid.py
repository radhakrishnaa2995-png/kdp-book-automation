from __future__ import annotations

import random
from typing import Dict, Iterable, List, Tuple

# ✅ Import ONLY from puzzle_generator (NO puzzles.py import)
from .puzzle_generator import (
    can_place,
    create_empty_grid,
    generate_grid,
    place_words,
)

Coordinate = Tuple[int, int]


def generate_puzzle(
    words: Iterable[str],
    size: int,
    theme: str = "Word Search",
    seed: int | None = None,
):
    """
    Generates a word search puzzle grid and returns:
    - grid (2D list)
    - positions of each word
    """

    puzzle = generate_grid(tuple(words), size=size, theme=theme, seed=seed)

    # Extract positions safely (no dependency on Puzzle class)
    positions: Dict[str, List[Coordinate]] = {
        word: list(placement.positions)
        for word, placement in puzzle.placements.items()
    }

    return [list(row) for row in puzzle.grid], positions


# ✅ Export only safe utilities (NO Puzzle / WordPlacement)
__all__ = [
    "can_place",
    "create_empty_grid",
    "generate_grid",
    "generate_puzzle",
    "place_words",
    "random",
]
