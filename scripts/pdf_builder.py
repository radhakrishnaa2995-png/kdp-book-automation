from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .generator import generate_book


WIDTH, HEIGHT = A4


@dataclass
class PDFResult:
    output_file: str


@dataclass
class BatchResult:
    files: List[str]
    seeds: List[int]
    puzzle_counts: List[int]
    batch_seed: int


# --------------------------------------------------
# 🔹 SIMPLE PDF DRAW (MINIMAL SAFE VERSION)
# --------------------------------------------------

def draw_page_number(c: canvas.Canvas, num: int):
    c.setFont("Helvetica", 10)
    c.drawCentredString(WIDTH / 2, 20, str(num))


def draw_puzzle_page(c: canvas.Canvas, puzzle, page_num: int):
    c.setFont("Helvetica", 12)

    y = HEIGHT - 50

    # Theme title
    c.drawString(50, y, f"Theme: {puzzle.theme}")
    y -= 30

    # Grid
    for row in puzzle.grid:
        c.drawString(50, y, " ".join(row))
        y -= 15

    y -= 20

    # Words
    c.drawString(50, y, "Words:")
    y -= 15

    words_line = ", ".join(puzzle.words)
    c.drawString(50, y, words_line)

    draw_page_number(c, page_num)


def draw_solution_page(c: canvas.Canvas, puzzle, page_num: int):
    c.setFont("Helvetica", 12)

    y = HEIGHT - 50
    c.drawString(50, y, f"Solution: {puzzle.theme}")
    y -= 30

    for row in puzzle.grid:
        c.drawString(50, y, " ".join(row))
        y -= 15

    draw_page_number(c, page_num)


# --------------------------------------------------
# 🔹 SINGLE PDF
# --------------------------------------------------

def build_pdf(
    output_file: str,
    puzzle_count: int,
    seed: int | None = None,
) -> PDFResult:

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    book = generate_book(
        puzzle_count=puzzle_count,
        seed=seed,
    )

    c = canvas.Canvas(output_file, pagesize=A4)

    page_num = 1

    # Puzzle pages
    for puzzle in book.puzzles:
        draw_puzzle_page(c, puzzle, page_num)
        c.showPage()
        page_num += 1

    # Solution pages
    for puzzle in book.solutions:
        draw_solution_page(c, puzzle, page_num)
        c.showPage()
        page_num += 1

    c.save()

    return PDFResult(output_file=output_file)


# --------------------------------------------------
# 🔹 BATCH PDF
# --------------------------------------------------

def build_pdf_batch(
    output_dir: str,
    puzzle_counts: List[int],
    seed: int | None = None,
    prefix: str = "kdp_word_search",
) -> BatchResult:

    os.makedirs(output_dir, exist_ok=True)

    files: List[str] = []
    seeds: List[int] = []

    import random
    import secrets

    base_seed = seed if seed is not None else secrets.randbits(63)
    rng = random.Random(base_seed)

    for index, puzzle_count in enumerate(puzzle_counts):

        book_seed = (
            base_seed if seed is not None and index == 0
            else rng.randrange(1, 2**63)
        )

        output_file = os.path.join(
            output_dir,
            f"{prefix}_{index+1:02d}_{puzzle_count}p.pdf"
        )

        result = build_pdf(
            output_file=output_file,
            puzzle_count=puzzle_count,
            seed=book_seed,
        )

        files.append(result.output_file)
        seeds.append(book_seed)

    return BatchResult(
        files=files,
        seeds=seeds,
        puzzle_counts=puzzle_counts,
        batch_seed=base_seed,
    )
