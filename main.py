import colorsys
import random

import pygame as pg


pg.init()


BOARD_SIZE = 4  # length n either direction
TILE_SIZE = 100
MARGIN_WIDTH = 20
GAP_WIDTH = 5
SCREEN_SIZE = TILE_SIZE * BOARD_SIZE + MARGIN_WIDTH * 2 + GAP_WIDTH * (BOARD_SIZE - 1)
FONT_SIZE = 30
FONT = pg.font.SysFont("Comic Sans MS", FONT_SIZE)
CHANCE_OF_4 = 0.1
BACKGROUND_COLOR = (150, 150, 150)
FONT_COLOR = (255, 255, 255)
TILE_COLORS = {
    2: (188, 32, 223),
    4: (128, 32, 223),
    8: (70, 32, 223),
    16: (32, 51, 223),
    32: (32, 108, 223),
    64: (32, 166, 223),
    128: (32, 223, 223),
    256: (32, 223, 166),
    512: (32, 223, 108),
    1024: (32, 223, 51),
    2048: (70, 223, 32),
    4096: (128, 223, 32),
    8192: (185, 223, 32),
    16384: (223, 204, 32),
    32768: (223, 147, 32),
    65536: (223, 89, 32),
    131072: (223, 32, 32)
}
DIRECTIONS = {
    pg.K_LEFT: "left",
    pg.K_RIGHT: "right",
    pg.K_UP: "up",
    pg.K_DOWN: "down"
}
DIRECTION_ROTATION_LEFT = {  # How many times to rotate from the left position.
    "left": 0,
    "up": 1,
    "right": 2,
    "down": 3
}


screen = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pg.time.Clock()


class Tile:
    def __init__(self, grid_x, grid_y, value=None):
        if value is not None:
            self.value = value
        else:
            self.value = 4 if random.random() < CHANCE_OF_4 else 2
        self.position = (0, 0)
        self.color = TILE_COLORS[self.value]
        self.surface = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surface.get_rect()
        self.surface.fill(self.color)
        number_surf = FONT.render(str(self.value), True, FONT_COLOR, self.color)
        number_rect = number_surf.get_rect()
        number_rect.center = self.rect.center
        self.surface.blit(number_surf, number_rect)
        self.update_position(grid_x, grid_y)

    def update_position(self, x, y):
        self.position = (
            MARGIN_WIDTH + (TILE_SIZE + GAP_WIDTH) * x,
            MARGIN_WIDTH + (TILE_SIZE + GAP_WIDTH) * y
        )
        self.rect.topleft = self.position

    def draw(self):
        screen.blit(self.surface, self.rect)


class Board:
    def __init__(self):
        self.board = [[None for y in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
        self.tiles = set()

        # place the first two tiles:
        tiles_placed = 0
        while tiles_placed < 2:
            x = random.choice(range(BOARD_SIZE))
            y = random.choice(range(BOARD_SIZE))
            if self.board[x][y] is None:
                new_tile = Tile(x, y)
                self.board[x][y] = new_tile
                self.tiles.add(new_tile)
                tiles_placed += 1

    def handle_input(self, direction):
        self.move_tiles(DIRECTION_ROTATION_LEFT[direction])

    def rotate_board(self, times):
        for _ in range(times):
            rotated_board = [i[:] for i in self.board]
            for x in range(BOARD_SIZE):
                for y in range(BOARD_SIZE):
                    rotated_board[x][BOARD_SIZE - 1 - y] = self.board[y][x]
            self.board = [i[:] for i in rotated_board]

    def move_tiles(self, rotate_n):
        self.rotate_board(rotate_n)

        for y in range(BOARD_SIZE):
            for x in range(1, BOARD_SIZE):
                tile = self.board[x][y]
                if tile is not None:
                    left_tile = self.board[x - 1][y]
                    if left_tile is None:
                        self.board[x - 1][y] = tile
                        self.board[x][y] = None

        self.rotate_board(4 - rotate_n)  # Rotate the board back.

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                tile = self.board[x][y]
                if tile is not None:
                     tile.update_position(x, y)

    def draw(self):
        for tile in self.tiles:
            tile.draw()


board = Board()

running = True
while running:
    dt = clock.tick(60)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        elif e.type == pg.KEYDOWN:
            if e.key in DIRECTIONS:
                board.handle_input(DIRECTIONS[e.key])

    #board.update()
    screen.fill(BACKGROUND_COLOR)
    board.draw()
    pg.display.update()

pg.quit()

# TODO: Add animations.