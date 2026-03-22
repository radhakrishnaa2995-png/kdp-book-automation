from reportlab.lib.pagesizes import A4

WIDTH, HEIGHT = A4

MARGIN = 50

def get_grid_layout(size):
    available_width = WIDTH - 2 * MARGIN
    cell = available_width / size

    start_x = MARGIN
    start_y = HEIGHT - 200

    return cell, start_x, start_y
