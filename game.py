import main
import find_chunks as fc
from game_mode import *
from pygame_utils import *

SCREEN_WIDTH = 800
FPS = 60
SCREEN_HEIGHT = 650

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("MineSweeper")

tile_layer = [[((i + j) % 2) + 1 for i in range(main.WIDTH)] for j in range(main.HEIGHT)]
suspect_layer = [[0 for _ in range(main.WIDTH)] for _ in range(main.HEIGHT)]

raw_chunks = fc.find_chunks(main.board, 0)
raw_chunks = [fc.expand_chunk(main.board, chunk, (9,)) for chunk in raw_chunks]
debug_map = fc.raw_chunks_to_board(raw_chunks, main.WIDTH, main.HEIGHT)

tile_images = [None]
tile_images.extend(load_images("img/tiles", ("png", "jpg")))

item_images = scale_list(load_images("img/items", ("png", "jpg")), (32, 32))

debug_tile_images = [None]
debug_tile_images.extend(load_images("img/debug_tiles"))

question_mark_images = [None]
question_mark_images.extend(scale_list(load_images("img/question_mark"), (32, 32)))

running = True
debug = True
frame_timer = 120
down_tick = 0
clock = pg.time.Clock()
flags_left = main.MINE_NUM
play_mode = PlayGameMode(screen, draw_list, main, item_images, debug, debug_map, debug_tile_images, tile_layer,
                         tile_images, suspect_layer, question_mark_images, raw_chunks, down_tick, flags_left)
freeze_mode = GameMode()

cur_mode = play_mode

while running:
    frame_timer -= down_tick
    if frame_timer == 0:
        running = False
    if cur_mode == play_mode:
        screen, draw_list, main, item_images, debug, debug_map, debug_tile_images, tile_layer, \
         tile_images, suspect_layer, question_mark_images, raw_chunks, down_tick = cur_mode.update()
    else:
        cur_mode.update()

    pg.display.flip()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        else:
            if cur_mode == play_mode:
                debug, flags_left, suspect_layer = cur_mode.check_events(e)
            else:
                cur_mode.check_events(e)
    clock.tick(FPS)
    if down_tick != 0 and cur_mode == play_mode:
        screen, draw_list, main, item_images, debug, debug_map, debug_tile_images, tile_layer, \
        tile_images, suspect_layer, question_mark_images, raw_chunks, down_tick = cur_mode.update()
        cur_mode = freeze_mode

pg.quit()
