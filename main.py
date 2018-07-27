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
BACKGROUND_COLOR = (100, 100, 100)
FONT_COLOR = (230, 230, 230)
TILE_COLORS = {}
for i in range(1, 18):
    TILE_COLORS[2**i] = [int(j * 255) for j in colorsys.hsv_to_rgb(20 * i, 0.75, 1)]
DIRECTIONS = {
    pg.K_LEFT: "left",
    pg.K_RIGHT: "right",
    pg.K_UP: "up",
    pg.K_DOWN: "down"
}


screen = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pg.time.Clock()


class Tile:
    def __init__(self, position, value=None):
        if value is not None:
            self.value = value
        else:
            self.value = 4 if random.random() < CHANCE_OF_4 else 2
        self.position = position
        self.color = TILE_COLORS[self.value]
        self.surface = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surface.get_rect()
        self.surface.fill(self.color)
        number_surf = FONT.render(str(self.value), True, FONT_COLOR, self.color)
        number_rect = number_surf.get_rect()
        number_rect.center = self.rect.center
        self.rect.topleft = self.position
        self.surface.blit(number_surf, number_rect)

    def draw(self):
        screen.blit(self.surface, self.rect)


class Board:
    def __init__(self):
        self.board = [[None for y in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
        self.tiles = set()
        self.tiles_are_moving = False

        # place the first two tiles:
        tiles_placed = 0
        while tiles_placed < 2:
            x = random.choice(range(BOARD_SIZE))
            y = random.choice(range(BOARD_SIZE))
            if self.board[x][y] is None:
                new_tile = Tile(
                    position=(
                        MARGIN_WIDTH + (TILE_SIZE + GAP_WIDTH) * x,
                        MARGIN_WIDTH + (TILE_SIZE + GAP_WIDTH) * y
                    ),
                    value = 1024
                )
                self.board[x][y] = new_tile
                self.tiles.add(new_tile)
                tiles_placed += 1

    def update(self, dt):
        pass

    def move_tiles(self, direction):
        pass

    def draw(self):
        for tile in self.tiles:
            tile.draw()


#test = Tile(position=(20, 50), value=2048)
board = Board()

running = True
while running:
    dt = clock.tick(60)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        elif e.type == pg.KEYDOWN:
            if e.key in DIRECTIONS:
                board.move_tiles(DIRECTIONS[e.key])

    board.update(dt)
    screen.fill(BACKGROUND_COLOR)
    board.draw()
    pg.display.update()

pg.quit()