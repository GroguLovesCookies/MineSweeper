import random
import find_chunks as fc
from game_mode import *
from pygame_utils import *
from settings import *

# TODO: Giving Option for size

# Good to have: Maintaining stats


pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("MineSweeper")


def play_game():
    import main
    global screen, draw_list

    main.MINE_NUM = int(0.1 * int(main.WIDTH * main.HEIGHT)) + random.randint(-1, 1)
    main.board = main.populate_board(main.board, main.MINE_NUM)
    main.fill_numbers(main.board)

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
    debug = False
    down_tick = 0
    clock = pg.time.Clock()
    flags_left = main.MINE_NUM
    roboto_font = pg.font.Font("fonts/Roboto-Thin.ttf", 28)

    play_mode = PlayGameMode(screen, draw_list, main, item_images, debug, debug_map, debug_tile_images, tile_layer,
                             tile_images, suspect_layer, question_mark_images, raw_chunks, down_tick, flags_left,
                             roboto_font)
    freeze_mode = FinishMode(screen, draw_list, main.board, item_images, roboto_font)

    cur_mode = play_mode
    while running:
        if cur_mode == play_mode:
            screen, draw_list, main, item_images, debug, debug_map, debug_tile_images, tile_layer, \
             tile_images, suspect_layer, question_mark_images, raw_chunks, down_tick = cur_mode.update()
        else:
            cur_mode.update()
        flags_left = main.MINE_NUM - main.count_items(suspect_layer, 1)
        print(flags_left, main.MINE_NUM)

        pg.display.flip()

        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            else:
                if e.type == pg.KEYDOWN and cur_mode == freeze_mode:
                    if e.key == pg.K_r:
                        return "r"
                if cur_mode == play_mode:
                    debug, flags_left, suspect_layer = cur_mode.check_events(e)
                else:
                    cur_mode.check_events(e)

        clock.tick(FPS)

        if down_tick != 0 and cur_mode == play_mode:
            extra_flags, similarities, missed_mines = main.check_win(main.board, suspect_layer)
            screen, draw_list, main, item_images, debug, debug_map, debug_tile_images, tile_layer, \
             tile_images, suspect_layer, question_mark_images, raw_chunks, down_tick = cur_mode.update()
            freeze_mode.extra_flags = extra_flags
            freeze_mode.missed_mines = missed_mines
            freeze_mode.correct = similarities
            cur_mode = freeze_mode
        if flags_left == 0 and cur_mode == play_mode:
            extra_flags, similarities, missed_mines = main.check_win(main.board, suspect_layer)
            screen, draw_list, main, item_images, debug, debug_map, debug_tile_images, tile_layer, \
             tile_images, suspect_layer, question_mark_images, raw_chunks, down_tick = cur_mode.update()
            freeze_mode.extra_flags = extra_flags
            freeze_mode.missed_mines = missed_mines
            freeze_mode.correct = similarities
            cur_mode = freeze_mode


res = "r"
while res == "r":
    res = play_game()
pg.quit()
