from __future__ import annotations

import random
from typing import Dict, Iterable, List, Tuple

from scripts.puzzle import Puzzle, WordPlacement
from scripts.puzzle_generator import can_place, create_empty_grid, generate_grid, place_words

Coordinate = Tuple[int, int]



def generate_puzzle(words: Iterable[str], size: int, theme: str = "Word Search", seed: int | None = None):
    puzzle = generate_grid(tuple(words), size=size, theme=theme, seed=seed)
    positions: Dict[str, List[Coordinate]] = {
        word: list(placement.positions) for word, placement in puzzle.placements.items()
    }
    return [list(row) for row in puzzle.grid], positions


__all__ = [
    "Puzzle",
    "WordPlacement",
    "can_place",
    "create_empty_grid",
    "generate_grid",
    "generate_puzzle",
    "place_words",
    "random",
]
