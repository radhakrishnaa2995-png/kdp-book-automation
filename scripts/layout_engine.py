from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Sequence

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth

from .puzzle import Puzzle

PAGE_WIDTH, PAGE_HEIGHT = A4
SAFE_MARGIN = 0.75 * inch
CONTENT_LEFT = SAFE_MARGIN
CONTENT_RIGHT = PAGE_WIDTH - SAFE_MARGIN
CONTENT_BOTTOM = SAFE_MARGIN
CONTENT_TOP = PAGE_HEIGHT - SAFE_MARGIN
CONTENT_WIDTH = CONTENT_RIGHT - CONTENT_LEFT
CONTENT_HEIGHT = CONTENT_TOP - CONTENT_BOTTOM

TITLE_FONT = "Helvetica-Bold"
BODY_FONT = "Helvetica"
GRID_FONT = "Courier-Bold"


@dataclass(frozen=True)
class GridLayout:
    box_x: float
    box_y: float
    box_size: float
    grid_x: float
    grid_y: float
    cell_size: float
    padding: float


@dataclass(frozen=True)
class WordListLayout:
    x: float
    y: float
    width: float
    height: float
    columns: int
    column_width: float
    line_height: float


@dataclass(frozen=True)
class PageLayout:
    title_y: float
    subtitle_y: float
    grid: GridLayout
    words: WordListLayout
    page_number_y: float



def _word_column_count(word_count: int) -> int:
    return 3 if word_count >= 10 else 2



def _word_list_height(word_count: int, columns: int, line_height: float = 17.0) -> float:
    rows = ceil(word_count / columns)
    return 22 + rows * line_height



def compute_page_layout(grid_size: int, word_count: int) -> PageLayout:
    title_y = CONTENT_TOP - 8
    subtitle_y = title_y - 28
    page_number_y = CONTENT_BOTTOM + 6

    columns = _word_column_count(word_count)
    line_height = 17.0
    words_height = _word_list_height(word_count, columns, line_height)
    words_y = page_number_y + 26
    column_gap = 14.0
    words_width = CONTENT_WIDTH
    column_width = (words_width - column_gap * (columns - 1)) / columns

    max_grid_top = subtitle_y - 28
    max_grid_bottom = words_y + words_height + 22
    max_grid_width = CONTENT_WIDTH
    max_grid_height = max_grid_top - max_grid_bottom
    padding = 16.0
    cell_size = min((max_grid_width - padding * 2) / grid_size, (max_grid_height - padding * 2) / grid_size)
    if cell_size <= 18:
        raise ValueError("Not enough vertical space to render the requested grid safely.")

    inner_size = cell_size * grid_size
    box_size = inner_size + padding * 2
    box_x = (PAGE_WIDTH - box_size) / 2
    box_y = max_grid_bottom + (max_grid_height - box_size) / 2
    grid_x = box_x + padding
    grid_y = box_y + box_size - padding - cell_size / 2

    return PageLayout(
        title_y=title_y,
        subtitle_y=subtitle_y,
        grid=GridLayout(
            box_x=box_x,
            box_y=box_y,
            box_size=box_size,
            grid_x=grid_x,
            grid_y=grid_y,
            cell_size=cell_size,
            padding=padding,
        ),
        words=WordListLayout(
            x=CONTENT_LEFT,
            y=words_y,
            width=words_width,
            height=words_height,
            columns=columns,
            column_width=column_width,
            line_height=line_height,
        ),
        page_number_y=page_number_y,
    )



def draw_header(pdf_canvas, title: str, layout: PageLayout, subtitle: str | None = None) -> None:
    pdf_canvas.setFillColor(colors.black)
    title_size = fit_title_size(title)
    pdf_canvas.setFont(TITLE_FONT, title_size)
    pdf_canvas.drawCentredString(PAGE_WIDTH / 2, layout.title_y, title.upper())
    if subtitle:
        pdf_canvas.setFont(BODY_FONT, 12)
        pdf_canvas.drawCentredString(PAGE_WIDTH / 2, layout.subtitle_y, subtitle)



def draw_grid(pdf_canvas, puzzle: Puzzle, layout: PageLayout, highlight_paths: bool = False) -> None:
    grid_layout = layout.grid
    size = len(puzzle.grid)

    pdf_canvas.setStrokeColor(colors.HexColor("#1f2937"))
    pdf_canvas.setLineWidth(1.6)
    pdf_canvas.rect(grid_layout.box_x, grid_layout.box_y, grid_layout.box_size, grid_layout.box_size, stroke=1, fill=0)

    pdf_canvas.setStrokeColor(colors.HexColor("#d1d5db"))
    pdf_canvas.setLineWidth(0.4)
    for index in range(1, size):
        offset = index * grid_layout.cell_size
        pdf_canvas.line(
            grid_layout.grid_x + offset,
            grid_layout.box_y + grid_layout.padding,
            grid_layout.grid_x + offset,
            grid_layout.box_y + grid_layout.box_size - grid_layout.padding,
        )
        pdf_canvas.line(
            grid_layout.box_x + grid_layout.padding,
            grid_layout.box_y + grid_layout.padding + offset,
            grid_layout.box_x + grid_layout.box_size - grid_layout.padding,
            grid_layout.box_y + grid_layout.padding + offset,
        )

    if highlight_paths:
        highlight_colors = [
            colors.HexColor("#dc2626"),
            colors.HexColor("#2563eb"),
            colors.HexColor("#16a34a"),
            colors.HexColor("#d97706"),
            colors.HexColor("#7c3aed"),
            colors.HexColor("#db2777"),
        ]
        for index, placement in enumerate(sorted(puzzle.placements.values(), key=lambda item: item.word)):
            color = highlight_colors[index % len(highlight_colors)]
            start_row, start_col = placement.start
            end_row, end_col = placement.end
            start_x = grid_layout.grid_x + start_col * grid_layout.cell_size + grid_layout.cell_size / 2
            start_y = grid_layout.grid_y - start_row * grid_layout.cell_size
            end_x = grid_layout.grid_x + end_col * grid_layout.cell_size + grid_layout.cell_size / 2
            end_y = grid_layout.grid_y - end_row * grid_layout.cell_size

            pdf_canvas.setStrokeColor(color)
            pdf_canvas.setLineWidth(max(2.2, grid_layout.cell_size * 0.18))
            pdf_canvas.line(start_x, start_y, end_x, end_y)
            pdf_canvas.circle(start_x, start_y, grid_layout.cell_size * 0.12, stroke=1, fill=0)
            pdf_canvas.circle(end_x, end_y, grid_layout.cell_size * 0.12, stroke=1, fill=0)

    pdf_canvas.setFillColor(colors.black)
    pdf_canvas.setFont(GRID_FONT, max(14, min(24, grid_layout.cell_size * 0.58)))
    for row_index, row in enumerate(puzzle.grid):
        for col_index, letter in enumerate(row):
            center_x = grid_layout.grid_x + col_index * grid_layout.cell_size + grid_layout.cell_size / 2
            baseline_y = grid_layout.grid_y - row_index * grid_layout.cell_size - grid_layout.cell_size * 0.16
            pdf_canvas.drawCentredString(center_x, baseline_y, letter)



def draw_word_list(pdf_canvas, words: Sequence[str], layout: PageLayout) -> None:
    words_layout = layout.words
    pdf_canvas.setFillColor(colors.HexColor("#111827"))
    pdf_canvas.setFont(TITLE_FONT, 13)
    pdf_canvas.drawString(words_layout.x, words_layout.y + words_layout.height - 6, "Find these words")

    pdf_canvas.setFont(BODY_FONT, 11.5)
    sorted_words = sorted(words)
    rows = ceil(len(sorted_words) / words_layout.columns)
    column_gap = 14.0

    for index, word in enumerate(sorted_words):
        column = index // rows
        row = index % rows
        x = words_layout.x + column * (words_layout.column_width + column_gap)
        y = words_layout.y + words_layout.height - 26 - row * words_layout.line_height
        pdf_canvas.drawString(x, y, word)



def draw_page_number(pdf_canvas, page_number: int, layout: PageLayout) -> None:
    pdf_canvas.setFillColor(colors.HexColor("#4b5563"))
    pdf_canvas.setFont(BODY_FONT, 10)
    pdf_canvas.drawCentredString(PAGE_WIDTH / 2, layout.page_number_y, str(page_number))



def draw_solution_page(pdf_canvas, puzzle: Puzzle, layout: PageLayout, page_number: int) -> None:
    draw_header(pdf_canvas, puzzle.theme, layout, subtitle="Solution")
    draw_grid(pdf_canvas, puzzle, layout, highlight_paths=True)
    draw_word_list(pdf_canvas, puzzle.words, layout)
    draw_page_number(pdf_canvas, page_number, layout)



def fit_title_size(text: str, max_size: float = 36, min_size: float = 28) -> float:
    size = max_size
    while size > min_size and stringWidth(text.upper(), TITLE_FONT, size) > CONTENT_WIDTH:
        size -= 1
    return size
