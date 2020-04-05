"""Copyright (C) 2019 Sebastian Henz

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





# class Tile:
#     def __init__(self, grid_x, grid_y, value=None):
#         if value is not None:
#             self.value = value
#         else:
#             self.value = 4 if random.random() < CHANCE_OF_2 else 2
#         self.position = (0, 0)
#         self.color = TILE_COLORS[self.value]
#         self.surface = pg.Surface((TILE_SIZE, TILE_SIZE))
#         self.rect = self.surface.get_rect()
#         self.surface.fill(self.color)
#         number_surf = FONT.render(str(self.value), True, FONT_COLOR, self.color)
#         number_rect = number_surf.get_rect()
#         number_rect.center = self.rect.center
#         self.surface.blit(number_surf, number_rect)
#         self.update_position(grid_x, grid_y)
#         self.merge_lock = True  # If True tile will not merge with others.
#
#     def update_position(self, x, y):
#         self.position = (
#             GAP_WIDTH + (TILE_SIZE + GAP_WIDTH) * x,
#             GAP_WIDTH + (TILE_SIZE + GAP_WIDTH) * y
#         )
#         self.rect.topleft = self.position
#
#     def draw(self):
#         screen.blit(self.surface, self.rect)


# class Board:
#     def __init__(self):
#         self.board = [[None for y in range(BOARD_SIZE)]
#                       for x in range(BOARD_SIZE)]
#         self.tiles = set()
#
#         self.surface = pg.Surface((SCREEN_SIZE, SCREEN_SIZE))
#         self.surface.fill(BACKGROUND_COLOR)
#         smaller_margin = GAP_WIDTH - BACKGROUND_PATTERN_OVERSIZE // 2
#         for x in range(BOARD_SIZE):
#             for y in range(BOARD_SIZE):
#                 pg.draw.rect(
#                     self.surface,
#                     BACKGROUND_PATTERN_COLOR,
#                     pg.Rect(
#                         smaller_margin + (TILE_SIZE + GAP_WIDTH) * x,
#                         smaller_margin + (TILE_SIZE + GAP_WIDTH) * y,
#                         TILE_SIZE + BACKGROUND_PATTERN_OVERSIZE,
#                         TILE_SIZE + BACKGROUND_PATTERN_OVERSIZE
#                     )
#                 )

        # # Place the first two tiles:
        # self.spawn_new_tile()
        # self.spawn_new_tile()

    # def spawn_new_tile(self, x=None, y=None, value=None):
    #     if x is None and y is None:
    #         while True:
    #             x = random.choice(range(BOARD_SIZE))
    #             y = random.choice(range(BOARD_SIZE))
    #             if self.board[x][y] is None:
    #                 break
    #     new_tile = Tile(x, y, value)
    #     self.board[x][y] = new_tile
    #     self.tiles.add(new_tile)
    #     # print(f"Spawned new tile at {x}, {y}, value = {value}")
    #     # print("---")

    # def handle_input(self, direction):
    #     self.move_tiles(DIRECTION_ROTATION_LEFT[direction])

    # def rotate_board(self, times):
    #     for _ in range(times):
    #         rotated_board = [i[:] for i in self.board]
    #         for x in range(BOARD_SIZE):
    #             for y in range(BOARD_SIZE):
    #                 rotated_board[x][BOARD_SIZE - 1 - y] = self.board[y][x]
    #         self.board = [i[:] for i in rotated_board]

    # def move_tiles(self, rotate_n):
    #     self.rotate_board(rotate_n)
    #
    #     spawn_new_random = False
    #     something_changed = True
    #     # Loop until the board does not change anymore.
    #     while something_changed:
    #         something_changed = False
    #         for y in range(BOARD_SIZE):
    #             for x in range(1, BOARD_SIZE):
    #                 tile = self.board[x][y]
    #                 if tile is None or (x - 1) < 0:
    #                     continue
    #
    #                 left_tile = self.board[x - 1][y]
    #                 if left_tile is None:
    #                     self.board[x - 1][y] = tile
    #                     self.board[x][y] = None
    #                     something_changed = True
    #                     spawn_new_random = True
    #                 elif (left_tile.value == tile.value
    #                       and not left_tile.merge_lock
    #                       and not tile.merge_lock):
    #                     new_value = tile.value * 2
    #                     self.tiles.remove(left_tile)
    #                     self.board[x - 1][y] = None
    #                     self.tiles.remove(tile)
    #                     self.board[x][y] = None
    #                     self.spawn_new_tile(x - 1, y, new_value)
    #                     something_changed = True
    #                     spawn_new_random = True
    #
    #     if spawn_new_random:
    #         self.spawn_new_tile()
    #
    #     self.rotate_board(4 - rotate_n)  # Rotate the board back.
    #
    #     for x in range(BOARD_SIZE):
    #         for y in range(BOARD_SIZE):
    #             tile = self.board[x][y]
    #             if tile is not None:
    #                 tile.update_position(x, y)
    #                 tile.merge_lock = False

    # def detect_loss(self):
    #     # Scan the board and see if the player lost the game.
    #     # If the board is full: for every tile: is there at least one
    #     # neighbor with the same value so it can merge?
    #     if len(self.tiles) < BOARD_SIZE * BOARD_SIZE:
    #         return False
    #     for x in range(BOARD_SIZE):
    #         for y in range(BOARD_SIZE):
    #             value = self.board[x][y].value
    #             neighbors_xy = [
    #                 [x - 1, y],
    #                 [x + 1, y],
    #                 [x, y - 1],
    #                 [x, y + 1]
    #             ]
    #             for n in neighbors_xy:
    #                 if (0 <= n[0] < 4) and (0 <= n[1] < 4):
    #                     if self.board[n[0]][n[1]].value == value:
    #                         return False
    #     print("You lost the game.")
    #     return True
    #
    # def draw(self):
    #     screen.blit(self.surface, (0, 0))
    #     for tile in self.tiles:
    #         tile.draw()


class Game:
    def __init__(self):
        self.running = True
        self.board = [[0 for y in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
        self.board_coordinates = list(itertools.product(range(BOARD_SIZE), repeat=2))
        self.screen = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

        # Place the first two tiles:
        self.new_tile()
        self.new_tile()

        self.background = pg.Surface((SCREEN_SIZE, SCREEN_SIZE))
        self.background.fill(BACKGROUND_COLOR)
        for x, y in self.board_coordinates:
            pg.draw.rect(
                self.background,
                BACKGROUND_PATTERN_COLOR,
                pg.Rect(
                    SMALLER_MARGIN + (TILE_SIZE + GAP_WIDTH) * x,
                    SMALLER_MARGIN + (TILE_SIZE + GAP_WIDTH) * y,
                    TILE_SIZE + BACKGROUND_PATTERN_OVERSIZE,
                    TILE_SIZE + BACKGROUND_PATTERN_OVERSIZE
                )
            )

    def run(self):
        clock = pg.time.Clock()
        while self.running:
            dt = clock.tick(60)
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
        print(f"Spawned new tile at {x}, {y}, value = {value}")
        print("---")

    def detect_loss(self):
        """Scan the board and see if the player lost the game.
        If the board is full: for every tile: is there at least one
        neighbor with the same value so it can merge?
        """
        for x, y in self.board_coordinates:
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
        self.running = False

    def handle_input(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.running = False
                if e.key in DIRECTIONS:
                    self.move_tiles(DIRECTIONS[e.key])

    def rotate_board(self, n):
        """Rotate the board n times 90° clockwise."""
        self.board = list(zip(*self.board))[::-1]

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
                    for left_x in range(0, x):
                        if (left_x, y) in locked_positions:
                            continue
                        if self.board[left_x][y] == 0:
                            self.board[left_x][y] = value
                            self.board[x][y] = 0
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
        self.screen.blit(self.background, (0, 0))

        pg.display.update()


Game().run()
