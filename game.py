import main
import find_chunks as fc
from pygame_utils import *


SCREEN_WIDTH = 800
FPS = 60
SCREEN_HEIGHT = 650


pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("MineSweeper")


tile_layer = [[((i+j) % 2) + 1 for i in range(main.WIDTH)] for j in range(main.HEIGHT)]

raw_chunks = fc.find_chunks(main.board, 0)
raw_chunks = [fc.expand_chunk(main.board, chunk, (9,)) for chunk in raw_chunks]
debug_map = fc.raw_chunks_to_board(raw_chunks, main.WIDTH, main.HEIGHT)


tile_images = [None]
tile_images.extend(load_images("img/tiles", ("png", "jpg")))

item_images = scale_list(load_images("img/items", ("png", "jpg")), (32, 32))

debug_tile_images = [None]
debug_tile_images.extend(load_images("img/debug_tiles"))


running = True
debug = True
frame_timer = 200
down_tick = 0
clock = pg.time.Clock()
while running:
    frame_timer -= down_tick
    if frame_timer == 0:
        running = False
    screen.fill((100, 100, 100))

    draw_list(screen, main.board, item_images, (0, 0), (32, 32))
    if debug:
        draw_list(screen, debug_map, debug_tile_images, (0, 0), (32, 32), [0])
    draw_list(screen, tile_layer, tile_images, (0, 0), (32, 32), [0])

    pressed = pg.mouse.get_pressed()
    if pressed[0]:
        pos = pg.mouse.get_pos()
        grid_pos_x = pos[0]//32
        grid_pos_y = pos[1]//32
        if 0 <= grid_pos_x < main.WIDTH and 0 <= grid_pos_y < main.HEIGHT:
            if tile_layer[grid_pos_y][grid_pos_x] != 0:
                if main.board[grid_pos_y][grid_pos_x] == 0:
                    chunk = fc.get_chunk_with_coord(raw_chunks, (grid_pos_x, grid_pos_y))
                    fc.paint_chunk_with_color(tile_layer, 0, chunk)
                elif main.board[grid_pos_y][grid_pos_x] == 9:
                    tile_layer[grid_pos_y][grid_pos_x] = 0
                    down_tick = 1
                else:
                    tile_layer[grid_pos_y][grid_pos_x] = 0

    pg.display.flip()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_TAB:
                debug = not debug
    clock.tick(FPS)


pg.quit()