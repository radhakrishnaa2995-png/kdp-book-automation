from __future__ import annotations

import random
import string
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

from .puzzles import Coordinate, Direction, Puzzle, WordPlacement

ALL_DIRECTIONS: Tuple[Direction, ...] = (
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
)

DIAGONAL_DIRECTIONS = {(1, 1), (-1, -1), (1, -1), (-1, 1)}
REVERSE_DIRECTIONS = {(0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1)}


@dataclass(frozen=True)
class PlacementCandidate:
    direction: Direction
    positions: Tuple[Coordinate, ...]
    score: float


def create_empty_grid(size: int) -> List[List[str]]:
    return [["" for _ in range(size)] for _ in range(size)]



def can_place(grid: Sequence[Sequence[str]], word: str, row: int, col: int, direction: Direction) -> bool:
    size = len(grid)
    dr, dc = direction
    for index, letter in enumerate(word):
        r = row + dr * index
        c = col + dc * index
        if not (0 <= r < size and 0 <= c < size):
            return False
        existing = grid[r][c]
        if existing not in ("", letter):
            return False
    return True



def _occupied_neighbors(grid: Sequence[Sequence[str]], row: int, col: int) -> int:
    size = len(grid)
    count = 0
    for r in range(max(0, row - 1), min(size, row + 2)):
        for c in range(max(0, col - 1), min(size, col + 2)):
            if (r, c) != (row, col) and grid[r][c]:
                count += 1
    return count



def _quadrant_index(size: int, row: int, col: int) -> int:
    half = size / 2
    return (2 if row >= half else 0) + (1 if col >= half else 0)



def _direction_variety_bonus(direction: Direction, direction_counts: Dict[Direction, int]) -> float:
    return 2.25 / (1 + direction_counts.get(direction, 0))



def _build_candidate(
    grid: Sequence[Sequence[str]],
    word: str,
    row: int,
    col: int,
    direction: Direction,
    direction_counts: Dict[Direction, int],
    rng: random.Random,
) -> PlacementCandidate:
    size = len(grid)
    dr, dc = direction
    positions = tuple((row + dr * i, col + dc * i) for i in range(len(word)))
    overlaps = sum(1 for (r, c), letter in zip(positions, word) if grid[r][c] == letter)
    neighbor_penalty = sum(_occupied_neighbors(grid, r, c) for r, c in positions)
    quadrant_bonus = sum(
        1.4 / (1 + sum(1 for rr in range(size) for cc in range(size) if grid[rr][cc] and _quadrant_index(size, rr, cc) == _quadrant_index(size, r, c)))
        for r, c in positions
    )
    diagonal_bonus = 1.5 if direction in DIAGONAL_DIRECTIONS else 0.0
    reverse_bonus = 1.5 if direction in REVERSE_DIRECTIONS else 0.0
    center_row = sum(r for r, _ in positions) / len(positions)
    center_col = sum(c for _, c in positions) / len(positions)
    center_penalty = abs(center_row - (size - 1) / 2) * 0.08 + abs(center_col - (size - 1) / 2) * 0.08
    score = (
        overlaps * 4.0
        + quadrant_bonus
        + diagonal_bonus
        + reverse_bonus
        + _direction_variety_bonus(direction, direction_counts)
        - neighbor_penalty * 0.18
        - center_penalty
        + rng.random() * 0.2
    )
    return PlacementCandidate(direction=direction, positions=positions, score=score)



def place_words(
    grid: List[List[str]],
    word: str,
    rng: random.Random,
    direction_counts: Dict[Direction, int],
) -> WordPlacement | None:
    candidates: List[PlacementCandidate] = []
    size = len(grid)

    for direction in ALL_DIRECTIONS:
        for row in range(size):
            for col in range(size):
                if can_place(grid, word, row, col, direction):
                    candidates.append(
                        _build_candidate(grid, word, row, col, direction, direction_counts, rng)
                    )

    if not candidates:
        return None

    candidates.sort(key=lambda item: item.score, reverse=True)
    shortlist = candidates[: min(12, len(candidates))]
    chosen = rng.choice(shortlist)

    for (r, c), letter in zip(chosen.positions, word):
        grid[r][c] = letter

    direction_counts[chosen.direction] = direction_counts.get(chosen.direction, 0) + 1
    return WordPlacement(
        word=word,
        start=chosen.positions[0],
        end=chosen.positions[-1],
        direction=chosen.direction,
        positions=chosen.positions,
    )



def _fill_empty_cells(grid: List[List[str]], rng: random.Random) -> None:
    alphabet = string.ascii_uppercase
    for row in range(len(grid)):
        for col in range(len(grid)):
            if not grid[row][col]:
                grid[row][col] = rng.choice(alphabet)



def _placement_mix_is_strong(placements: Iterable[WordPlacement]) -> bool:
    placements = list(placements)
    has_diagonal = any(item.direction in DIAGONAL_DIRECTIONS for item in placements)
    has_reverse = any(item.direction in REVERSE_DIRECTIONS for item in placements)
    return has_diagonal and has_reverse



def generate_grid(
    words: Sequence[str],
    size: int,
    theme: str,
    seed: int | None = None,
    max_restarts: int = 250,
) -> Puzzle:
    if not words:
        raise ValueError("At least one word is required to generate a puzzle.")
    if max(len(word) for word in words) > size:
        raise ValueError("Grid size must be at least as long as the longest word.")

    rng = random.Random(seed)
    ordered_words = sorted(words, key=lambda value: (-len(value), value))

    best_partial: tuple[List[List[str]], Dict[str, WordPlacement], Dict[Direction, int]] | None = None

    for _ in range(max_restarts):
        grid = create_empty_grid(size)
        placements: Dict[str, WordPlacement] = {}
        direction_counts: Dict[Direction, int] = {}
        grouped_words = ordered_words[:]
        rng.shuffle(grouped_words)
        grouped_words.sort(key=lambda value: (-len(value), rng.random()))

        for word in grouped_words:
            placement = place_words(grid, word, rng, direction_counts)
            if placement is None:
                break
            placements[word] = placement
        else:
            if len(placements) == len(words) and _placement_mix_is_strong(placements.values()):
                _fill_empty_cells(grid, rng)
                return Puzzle(
                    theme=theme,
                    grid=tuple(tuple(row) for row in grid),
                    words=tuple(sorted(words)),
                    placements=placements,
                )

        if best_partial is None or len(placements) > len(best_partial[1]):
            best_partial = ([row[:] for row in grid], dict(placements), dict(direction_counts))

    raise RuntimeError(
        f"Unable to generate a balanced puzzle for theme '{theme}'. "
        f"Best attempt placed {len(best_partial[1]) if best_partial else 0} of {len(words)} words."
    )
