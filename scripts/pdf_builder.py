from __future__ import annotations

import os
import random
import secrets
from dataclasses import dataclass
from typing import List, Sequence

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .generator import GeneratedBook, generate_book
from .layout_engine import (
    CONTENT_BOTTOM,
    CONTENT_TOP,
    PAGE_WIDTH,
    compute_page_layout,
    draw_page_background,
    draw_grid,
    draw_header,
    draw_page_number,
    draw_solution_page,
    draw_theme_clipart,
    draw_word_list,
)
from .puzzles import Puzzle
from .comfyui_client import ComfyUIClient


@dataclass(frozen=True)
class BookBuildResult:
    puzzles: List[Puzzle]
    output_file: str
    seed: int
    signature: str


@dataclass(frozen=True)
class BatchBuildResult:
    files: List[str]
    puzzle_counts: List[int]
    seeds: List[int]
    batch_seed: int



def _draw_solutions_divider(pdf_canvas, page_number: int) -> None:
    draw_page_background(pdf_canvas)
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



def _render_book(
    book: GeneratedBook,
    output_file: str,
    comfyui_url: str | None = None,
    comfyui_workflow: str | None = None,
    comfyui_checkpoint: str = "v1-5-pruned-emaonly.ckpt",
) -> BookBuildResult:
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    pdf_canvas = canvas.Canvas(output_file, pagesize=A4)
    pdf_canvas.setTitle("Word Search Puzzle Book")
    pdf_canvas.setAuthor("OpenAI Codex")
    pdf_canvas.setSubject("Amazon KDP-ready themed word search puzzle book")

    page_number = 1
    comfyui_client = (
        ComfyUIClient(
            base_url=comfyui_url,
            workflow_path=comfyui_workflow,
            checkpoint_name=comfyui_checkpoint,
        )
        if comfyui_url
        else None
    )
    comfyui_warning_shown = False
    for puzzle in book.puzzles:
        layout = compute_page_layout(grid_size=len(puzzle.grid), word_count=len(puzzle.words))
        draw_page_background(pdf_canvas)
        clipart_path = None
        if comfyui_client:
            try:
                clipart_path = comfyui_client.render_theme_clipart(puzzle.theme)
            except Exception as exc:
                if not comfyui_warning_shown:
                    print(f"⚠️ ComfyUI unavailable or workflow failed: {exc}")
                    comfyui_warning_shown = True
                clipart_path = None
        draw_theme_clipart(pdf_canvas, clipart_path, layout, theme_label=puzzle.theme)
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
        draw_page_background(pdf_canvas)
        clipart_path = None
        if comfyui_client:
            try:
                clipart_path = comfyui_client.render_theme_clipart(puzzle.theme)
            except Exception as exc:
                if not comfyui_warning_shown:
                    print(f"⚠️ ComfyUI unavailable or workflow failed: {exc}")
                    comfyui_warning_shown = True
                clipart_path = None
        draw_theme_clipart(pdf_canvas, clipart_path, layout, theme_label=puzzle.theme)
        draw_solution_page(pdf_canvas, puzzle, layout, page_number)
        pdf_canvas.showPage()
        page_number += 1

    pdf_canvas.save()
    return BookBuildResult(
        puzzles=book.puzzles,
        output_file=output_file,
        seed=book.seed,
        signature=book.signature,
    )



def build_pdf(
    output_file: str,
    puzzle_count: int,
    seed: int | None = None,
    theme_api_url: str | None = None,
    openrouter_model: str | None = None,
    comfyui_url: str | None = None,
    comfyui_workflow: str | None = None,
    comfyui_checkpoint: str = "v1-5-pruned-emaonly.ckpt",
) -> BookBuildResult:
    book = generate_book(
        puzzle_count=puzzle_count,
        seed=seed,
        theme_api_url=theme_api_url,
        openrouter_model=openrouter_model,
    )
    return _render_book(
        book=book,
        output_file=output_file,
        comfyui_url=comfyui_url,
        comfyui_workflow=comfyui_workflow,
        comfyui_checkpoint=comfyui_checkpoint,
    )



def build_pdf_batch(
    output_dir: str,
    pdf_count: int | None = None,
    puzzle_count: int | None = None,
    puzzle_counts: Sequence[int] | None = None,
    seed: int | None = None,
    prefix: str = "kdp_word_search",
    theme_api_url: str | None = None,
    openrouter_model: str | None = None,
    comfyui_url: str | None = None,
    comfyui_workflow: str | None = None,
    comfyui_checkpoint: str = "v1-5-pruned-emaonly.ckpt",
) -> BatchBuildResult:
    os.makedirs(output_dir, exist_ok=True)

    if puzzle_counts is None:
        if puzzle_count is None or pdf_count is None:
            raise ValueError("Provide either puzzle_counts or both pdf_count and puzzle_count.")
        puzzle_counts = [puzzle_count] * pdf_count
    else:
        puzzle_counts = list(puzzle_counts)
        if not puzzle_counts:
            raise ValueError("puzzle_counts cannot be empty.")

    batch_seed = seed if seed is not None else secrets.randbits(63)
    rng = random.Random(batch_seed)
    used_page_signatures: set[str] = set()
    used_book_signatures: set[str] = set()
    files: List[str] = []
    seeds: List[int] = []

    for index, current_puzzle_count in enumerate(puzzle_counts):
        book_seed = rng.randrange(1, 2**63)
        book = generate_book(
            puzzle_count=current_puzzle_count,
            seed=book_seed,
            blocked_page_signatures=used_page_signatures,
            blocked_book_signatures=used_book_signatures,
            max_attempts=40,
            theme_api_url=theme_api_url,
            openrouter_model=openrouter_model,
        )

        used_book_signatures.add(book.signature)
        used_page_signatures.update(puzzle.signature for puzzle in book.puzzles)

        filename = os.path.join(output_dir, f"{prefix}_{index + 1:02d}_{current_puzzle_count}p.pdf")
        result = _render_book(
            book=book,
            output_file=filename,
            comfyui_url=comfyui_url,
            comfyui_workflow=comfyui_workflow,
            comfyui_checkpoint=comfyui_checkpoint,
        )
        files.append(result.output_file)
        seeds.append(result.seed)

    return BatchBuildResult(
        files=files,
        puzzle_counts=list(puzzle_counts),
        seeds=seeds,
        batch_seed=batch_seed,
    )
