from __future__ import annotations

from .layout_engine import (
    PAGE_HEIGHT,
    PAGE_WIDTH,
    SAFE_MARGIN as MARGIN,
    compute_page_layout,
)



def get_grid_position(grid_size: int, word_count: int = 12):
    layout = compute_page_layout(grid_size, word_count)
    return layout.grid.grid_x, layout.grid.grid_y, layout.grid.cell_size



def get_word_list_position(word_count: int = 12):
    layout = compute_page_layout(12, word_count)
    return layout.words.y
