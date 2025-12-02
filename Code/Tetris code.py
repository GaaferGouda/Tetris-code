import pygame
import random

pygame.font.init()

# GLOBAL VARS
s_width = 800
s_height = 700
play_width = 300     # 300 // 10 = 30px per block
play_height = 600    # 600 // 20 = 30px per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPES
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 0, 255),
    (128, 0, 128)
]


class Piece(object):
    rows = 20
    columns = 10

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(20):
        for j in range(10):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        for j, char in enumerate(line):
            if char == '0':
                positions.append((shape.x + j, shape.y + i))

    # offset correction
    return [(x - 2, y - 4) for x, y in positions]


def valid_space(shape, grid):
    accepted_positions = [
        (j, i)
        for i in range(20)
        for j in range(10)
        if grid[i][j] == (0, 0, 0)
    ]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions and pos[1] > -1:
            return False
    return True


def check_lost(positions):
    return any(y < 1 for _, y in positions)


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (
        top_left_x + play_width/2 - label.get_width()/2,
        top_left_y + play_height/2 - label.get_height()/2
    ))


def draw_grid(surface):
    for i in range(20):
        pygame.draw.line(surface, (128, 128, 128),
                         (top_left_x, top_left_y + i*30),
                         (top_left_x + play_width, top_left_y + i*30))
    for j in range(10):
        pygame.draw.line(surface, (128, 128, 128),
                         (top_left_x + j*30, top_left_y),
                         (top_left_x + j*30, top_left_y + play_height))


def clear_rows(grid, locked):
    inc = 0
    for i in range(19, -1, -1):
        if (0, 0, 0) not in grid[i]:
            inc += 1
            for j in range(10):
                locked.pop((j, i), None)

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < i:
                locked[(x, y + inc)] = locked.pop(key)


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape", 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + 150

    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        for j, char in enumerate(line):
            if char == '0':
                pygame.draw.rect(
                    surface, shape.color,
                    (sx + j*30, sy + i*30, 30, 30)
                )

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, grid):
    surface.fill((0, 0, 0))

    font = pygame.font.SysFont("comicsans", 60)
    label = font.render("TETRIS", 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, 30))

    for i in range(20):
        for j in range(10):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j*30, top_left_y + i*30, 30, 30))

    draw_grid(surface)
    pygame.draw.rect(surface, (255, 0, 0),
                     (top_left_x, top_left_y, play_width, play_height), 5)


def main():
    global grid
    locked_positions = {}
    grid = create_grid()

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_speed = 0.27
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # falling
        if fall_time / 1000 >= fall_speed:
            current_piece.y += 1
            fall_time = 0
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                change_piece = True

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)

        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                locked_positions[(pos[0], pos[1])] = current_piece.color

            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            clear_rows(grid, locked_positions)

        draw_window(win, grid)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("YOU LOST", 60, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False


def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle("Press any key to start", 60, (255, 255, 255), win)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")
main_menu()
