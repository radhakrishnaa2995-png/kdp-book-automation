from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from .puzzle_generator import can_place, create_empty_grid, generate_grid, place_words
from .puzzles import Coordinate, WordPlacement

GridMatrix = List[List[str]]
PlacementMap = Dict[str, List[Coordinate]]


def _to_mutable_grid(grid: Tuple[Tuple[str, ...], ...]) -> GridMatrix:
    return [list(row) for row in grid]


def _to_position_map(placements: Dict[str, WordPlacement]) -> PlacementMap:
    return {
        word: list(placement.positions)
        for word, placement in placements.items()
    }


def generate_puzzle(
    words: Iterable[str],
    size: int,
    theme: str = "Word Search",
    seed: int | None = None,
) -> tuple[GridMatrix, PlacementMap]:
    normalized_words = tuple(words)
    if not normalized_words:
        raise ValueError("At least one word is required to generate a puzzle.")

    puzzle = generate_grid(
        words=normalized_words,
        size=size,
        theme=theme,
        seed=seed,
    )
    return _to_mutable_grid(puzzle.grid), _to_position_map(puzzle.placements)


__all__ = [
    "Coordinate",
    "GridMatrix",
    "PlacementMap",
    "can_place",
    "create_empty_grid",
    "generate_grid",
    "generate_puzzle",
    "place_words",
]
