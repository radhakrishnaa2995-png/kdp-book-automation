from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from layout import *
import random

WIDTH, HEIGHT = A4

def draw_title_page(c, theme):
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(WIDTH/2, HEIGHT/2 + 50, f"{theme} Word Search")

    c.setFont("Helvetica", 18)
    c.drawCentredString(WIDTH/2, HEIGHT/2, "Fun Puzzle Book for Kids")

    c.showPage()


def draw_grid(c, grid):
    size = len(grid)
    x, y, cell = get_grid_position(size)

    c.setFont("Helvetica-Bold", int(cell * 0.5))

    for r in range(size):
        for col in range(size):
            c.drawCentredString(
                x + col * cell + cell/2,
                y - r * cell,
                grid[r][col]
            )


def draw_words(c, words):
    y = get_word_list_position()
    x = 80

    for i, word in enumerate(words):
        c.roundRect(x, y, 100, 25, 8)
        c.drawCentredString(x + 50, y + 8, word)

        x += 120
        if x > 400:
            x = 80
            y -= 40


def draw_solution(c, grid, solution):
    size = len(grid)
    x, y, cell = get_grid_position(size)

    c.setFont("Helvetica-Bold", int(cell * 0.5))

    for r in range(size):
        for col in range(size):
            highlight = False

            for positions in solution.values():
                if (r, col) in positions:
                    highlight = True

            if highlight:
                c.setFillColor(colors.red)
            else:
                c.setFillColor(colors.black)

            c.drawCentredString(
                x + col * cell + cell/2,
                y - r * cell,
                grid[r][col]
            )


def add_page_number(c, num):
    c.setFont("Helvetica", 10)
    c.drawCentredString(WIDTH/2, 20, str(num))


def build_pdf(filename, puzzles, solutions, theme):
    c = canvas.Canvas(filename, pagesize=A4)

    draw_title_page(c, theme)

    page = 1

    for i, (grid, words) in enumerate(puzzles):
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(WIDTH/2, HEIGHT - 80, f"Puzzle {i+1}")

        draw_grid(c, grid)
        draw_words(c, words)

        add_page_number(c, page)
        page += 1
        c.showPage()

    # SOLUTIONS
    for i, (grid, sol) in enumerate(solutions):
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(WIDTH/2, HEIGHT - 80, f"Solution {i+1}")

        draw_solution(c, grid, sol)

        add_page_number(c, page)
        page += 1
        c.showPage()

    c.save()
