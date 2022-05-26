import main
import find_chunks as fc
from pygame_utils import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650


pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("MineSweeper")

tile_layer = [[((i+j) % 2) + 1 for i in range(main.WIDTH)] for j in range(main.HEIGHT)]
debug_map = fc.raw_chunks_to_board(fc.find_chunks(main.board, 0), main.WIDTH, main.HEIGHT)


tile_images = [None]
tile_images.extend(load_images("img/tiles", ("png", "jpg")))

item_images = scale_list(load_images("img/items", ("png", "jpg")), (32, 32))

debug_tile_images = [None]
debug_tile_images.extend(load_images("img/debug_tiles"))


running = True
debug = True
while running:

    screen.fill((100, 100, 100))

    draw_list(screen, main.board, item_images, (0, 0), (32, 32))
    if debug:
        draw_list(screen, debug_map, debug_tile_images, (0, 0), (32, 32), [0])
    # draw_list(screen, tile_layer, tile_images, (0, 0), (32, 32), [0])

    pg.display.flip()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_TAB:
                debug = not debug


pg.quit()