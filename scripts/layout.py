from reportlab.lib.units import inch

PAGE_WIDTH = 8.27 * inch
PAGE_HEIGHT = 11.69 * inch

MARGIN = 0.7 * inch

def get_grid_position(grid_size):
    usable_width = PAGE_WIDTH - 2 * MARGIN
    cell_size = usable_width / grid_size

    grid_width = cell_size * grid_size
    x_start = (PAGE_WIDTH - grid_width) / 2
    y_start = PAGE_HEIGHT * 0.55

    return x_start, y_start, cell_size

def get_word_list_position():
    return PAGE_HEIGHT * 0.25
