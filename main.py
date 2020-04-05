"""Copyright (C) 2020 Sebastian Henz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""


import os
import random
import itertools

import pygame as pg


os.environ["SDL_VIDEO_CENTERED"] = "1"
pg.init()


BOARD_SIZE = 4  # length n either direction
TILE_SIZE = 100
GAP_WIDTH = 10
BACKGROUND_PATTERN_OVERSIZE = 4
SMALLER_MARGIN = GAP_WIDTH - BACKGROUND_PATTERN_OVERSIZE // 2
SCREEN_SIZE = (TILE_SIZE * BOARD_SIZE
               + GAP_WIDTH * 2
               + GAP_WIDTH * (BOARD_SIZE - 1))
screen = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
FONT_SIZE = 30
FONT = pg.font.SysFont("Comic Sans MS", FONT_SIZE)
CHANCE_OF_2 = 0.9
BACKGROUND_COLOR = (150, 150, 150)
BACKGROUND_PATTERN_COLOR = [200, 200, 200]
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
DIRECTION_ROTATIONS = {  # How many times to rotate depending on move direction.
    "left": 0,
    "up": 1,
    "right": 2,
    "down": 3
}
TILE_SURFACES = {}
for p in range(1, 18):
    value = 2**p
    surface = pg.Surface((TILE_SIZE, TILE_SIZE))
    color = TILE_COLORS[value]
    surface.fill(color)
    text_surface = FONT.render(str(value), True, FONT_COLOR, color)
    text_rect = text_surface.get_rect()
    text_rect.center = surface.get_rect().center
    surface.blit(text_surface, text_rect)
    TILE_SURFACES[value] = surface
board_coordinates = list(itertools.product(range(BOARD_SIZE), repeat=2))
background = pg.Surface((SCREEN_SIZE, SCREEN_SIZE))
background.fill(BACKGROUND_COLOR)
for x, y in board_coordinates:
    pg.draw.rect(
        background,
        BACKGROUND_PATTERN_COLOR,
        pg.Rect(
            SMALLER_MARGIN + (TILE_SIZE + GAP_WIDTH) * x,
            SMALLER_MARGIN + (TILE_SIZE + GAP_WIDTH) * y,
            TILE_SIZE + BACKGROUND_PATTERN_OVERSIZE,
            TILE_SIZE + BACKGROUND_PATTERN_OVERSIZE
        )
    )


class Game:
    def __init__(self):
        self.running = True
        self.clock = pg.time.Clock()
        self.new_game()

    def new_game(self):
        self.board = [[0 for y in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
        self.new_tile()
        self.new_tile()
        self.game_over = False

    def run(self):
        while self.running:
            self.clock.tick(30)
            self.detect_loss()
            self.handle_input()
            self.draw()

    def new_tile(self, x=None, y=None, value=None):
        if x is None and y is None:
            while True:
                x = random.choice(range(BOARD_SIZE))
                y = random.choice(range(BOARD_SIZE))
                if self.board[x][y] == 0:
                    break
        if value is not None:
            value = value
        else:
            value = 2 if random.random() < CHANCE_OF_2 else 4
        self.board[x][y] = value

    def detect_loss(self):
        """Scan the board and see if the player lost the game.
        If the board is full: for every tile: is there at least one
        neighbor with the same value so it can merge?
        """
        for x, y in board_coordinates:
            value = self.board[x][y]
            if value == 0:
                return
            neighbor_coordinates = (
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1)
            )
            for nx, ny in neighbor_coordinates:
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE \
                        and self.board[nx][ny] == value:
                    return
        self.game_over = True

    def handle_input(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.running = False
                elif e.key in DIRECTIONS and not self.game_over:
                    self.move_tiles(DIRECTIONS[e.key])
                elif e.key == pg.K_n:
                    self.new_game()

    def rotate_board(self, n):
        """Rotate the board n times 90° counterclockwise."""
        for _ in range(n):
            self.board = list(zip(*self.board[::-1]))
        self.board = [list(column) for column in self.board]

    def move_tiles(self, direction):
        n_rotations = DIRECTION_ROTATIONS[direction]
        self.rotate_board(n_rotations)

        locked_positions = set()  # cannot merge in this frame
        spawn_new = False
        something_changed = True
        while something_changed:
            something_changed = False
            for y in range(BOARD_SIZE):
                for x in range(1, BOARD_SIZE):
                    value = self.board[x][y]
                    if value == 0:
                        continue
                    left_x = x -1
                    if (left_x, y) in locked_positions:
                        continue
                    if self.board[left_x][y] == 0:
                        self.board[left_x][y] = value
                        self.board[x][y] = 0
                        something_changed = True
                        spawn_new = True
                    elif self.board[left_x][y] == value:
                        self.board[left_x][y] = value * 2
                        locked_positions.add((left_x, y))
                        self.board[x][y] = 0
                        something_changed = True
                        spawn_new = True

        self.rotate_board(4 - n_rotations)  # rotate to original orientation
        if spawn_new:
            self.new_tile()

    def draw(self):
        screen.blit(background, (0, 0))

        for x, y in board_coordinates:
            if self.board[x][y] > 0:
                position = (
                    GAP_WIDTH + (TILE_SIZE + GAP_WIDTH) * x,
                    GAP_WIDTH + (TILE_SIZE + GAP_WIDTH) * y
                )
                screen.blit(TILE_SURFACES[self.board[x][y]], position)

        pg.display.update()


Game().run()
