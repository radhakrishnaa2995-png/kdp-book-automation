from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from generator import generate_book
from layout_engine import (
    CONTENT_BOTTOM,
    CONTENT_TOP,
    PAGE_WIDTH,
    compute_page_layout,
    draw_grid,
    draw_header,
    draw_page_number,
    draw_solution_page,
    draw_word_list,
)
from puzzle_generator import Puzzle


@dataclass(frozen=True)
class BookBuildResult:
    puzzles: List[Puzzle]
    output_file: str


def _draw_solutions_divider(pdf_canvas, page_number: int) -> None:
    pdf_canvas.setFillColor(colors.black)
    pdf_canvas.setFont("Helvetica-Bold", 32)
    pdf_canvas.drawCentredString(PAGE_WIDTH / 2, CONTENT_TOP - 50, "SOLUTIONS")
    pdf_canvas.setFont("Helvetica", 13)
    pdf_canvas.drawCentredString(
        PAGE_WIDTH / 2,
        CONTENT_TOP - 82,
        "Each solution page matches its puzzle and highlights every hidden word.",
    )
    pdf_canvas.setStrokeColor(colors.HexColor("#9ca3af"))
    pdf_canvas.setLineWidth(1)
    pdf_canvas.line(PAGE_WIDTH / 2 - 120, CONTENT_TOP - 98, PAGE_WIDTH / 2 + 120, CONTENT_TOP - 98)
    pdf_canvas.setFont("Helvetica", 10)
    pdf_canvas.setFillColor(colors.HexColor("#4b5563"))
    pdf_canvas.drawCentredString(PAGE_WIDTH / 2, CONTENT_BOTTOM + 6, str(page_number))


def build_pdf(output_file: str, puzzle_count: int, seed: int | None = None) -> BookBuildResult:
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    book = generate_book(puzzle_count=puzzle_count, seed=seed)

    pdf_canvas = canvas.Canvas(output_file, pagesize=A4)
    pdf_canvas.setTitle("Word Search Puzzle Book")
    pdf_canvas.setAuthor("OpenAI Codex")
    pdf_canvas.setSubject("Amazon KDP-ready themed word search puzzle book")

    page_number = 1
    for puzzle in book.puzzles:
        layout = compute_page_layout(grid_size=len(puzzle.grid), word_count=len(puzzle.words))
        draw_header(pdf_canvas, puzzle.theme, layout, subtitle="Word Search Puzzle")
        draw_grid(pdf_canvas, puzzle, layout)
        draw_word_list(pdf_canvas, puzzle.words, layout)
        draw_page_number(pdf_canvas, page_number, layout)
        pdf_canvas.showPage()
        page_number += 1

    _draw_solutions_divider(pdf_canvas, page_number)
    pdf_canvas.showPage()
    page_number += 1

    for puzzle in book.solutions:
        layout = compute_page_layout(grid_size=len(puzzle.grid), word_count=len(puzzle.words))
        draw_solution_page(pdf_canvas, puzzle, layout, page_number)
        pdf_canvas.showPage()
        page_number += 1

    pdf_canvas.save()
    return BookBuildResult(puzzles=book.puzzles, output_file=output_file)
