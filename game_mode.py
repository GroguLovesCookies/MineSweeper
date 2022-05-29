import pygame as pg
import find_chunks as fc
import settings
from button import Button


class GameMode:
    def update(self, *args):
        return

    def check_events(self, e):
        return


class PlayGameMode(GameMode):
    def __init__(self, screen, draw_list, main, item_images, debug, debug_map, debug_tile_images, tile_layer,
                 tile_images, suspect_layer, question_mark_images, raw_chunks, down_tick, flags_left, font):
        self.screen = screen
        self.draw_list = draw_list
        self.main = main
        self.item_images = item_images
        self.debug = debug
        self.debug_map = debug_map
        self.debug_tile_images = debug_tile_images
        self.tile_layer = tile_layer
        self.tile_images = tile_images
        self.suspect_layer = suspect_layer
        self.question_mark_images = question_mark_images
        self.raw_chunks = raw_chunks
        self.down_tick = down_tick
        self.flags_left = flags_left
        self.font = font
        self.frame = 0

    def update(self, *args):
        screen = self.screen
        draw_list = self.draw_list
        main = self.main
        item_images = self.item_images
        debug = self.debug
        debug_map = self.debug_map
        debug_tile_images = self.debug_tile_images
        tile_layer = self.tile_layer
        tile_images = self.tile_images
        suspect_layer = self.suspect_layer
        question_mark_images = self.question_mark_images
        raw_chunks = self.raw_chunks
        down_tick = self.down_tick

        screen.fill((100, 100, 100))
        self.frame += 1

        time = self.frame//settings.FPS
        minutes = time//60
        seconds = time % 60

        label = self.font.render(str(minutes).rjust(2, "0") + ":" + str(seconds).rjust(2, "0"), 1, (255, 255, 255))
        rect = label.get_rect()
        rect.bottomright = (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        screen.blit(label, rect)

        counter = self.font.render(str(self.flags_left) + "/" + str(main.MINE_NUM), 1, (255, 255, 255))
        rect = counter.get_rect()
        rect.bottomleft = (0, settings.SCREEN_HEIGHT)
        screen.blit(counter, rect)

        draw_list(screen, main.board, item_images, (0, 0), (32, 32))
        if debug:
            draw_list(screen, debug_map, debug_tile_images, (0, 0), (32, 32), [0], 4)
        draw_list(screen, tile_layer, tile_images, (0, 0), (32, 32), [0])
        draw_list(screen, suspect_layer, question_mark_images, (0, 0), (32, 32), [0])

        self.screen = screen
        self.draw_list = draw_list
        self.main = main
        self.item_images = item_images
        self.debug = debug
        self.debug_map = debug_map
        self.debug_tile_images = debug_tile_images
        self.tile_layer = tile_layer
        self.tile_images = tile_images
        self.suspect_layer = suspect_layer
        self.question_mark_images = question_mark_images
        self.raw_chunks = raw_chunks
        self.down_tick = down_tick

        return (screen, draw_list, main, item_images, debug, debug_map, debug_tile_images, tile_layer,
                tile_images, suspect_layer, question_mark_images, raw_chunks, down_tick)

    def check_events(self, e):
        debug = self.debug
        flags_left = self.flags_left
        main = self.main
        suspect_layer = self.suspect_layer
        down_tick = 0

        if e.type == pg.KEYDOWN:
            if e.key == pg.K_TAB:
                debug = not debug
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 3:
                pos = pg.mouse.get_pos()
                grid_pos_x = pos[0] // 32
                grid_pos_y = pos[1] // 32
                if 0 <= grid_pos_x < main.WIDTH and 0 <= grid_pos_y < main.HEIGHT:
                    if suspect_layer[grid_pos_y][grid_pos_x] == 0 and flags_left > 0:
                        suspect_layer[grid_pos_y][grid_pos_x] = 1
                        flags_left -= 1
                    elif suspect_layer[grid_pos_y][grid_pos_x] == 1:
                        suspect_layer[grid_pos_y][grid_pos_x] = 0
                        flags_left += 1
            if e.button == 1:
                pos = pg.mouse.get_pos()
                grid_pos_x = pos[0] // 32
                grid_pos_y = pos[1] // 32
                if 0 <= grid_pos_x < main.WIDTH and 0 <= grid_pos_y < main.HEIGHT:
                    if self.tile_layer[grid_pos_y][grid_pos_x] != 0 and suspect_layer[grid_pos_y][grid_pos_x] == 0:
                        if main.board[grid_pos_y][grid_pos_x] == 0:
                            chunk = fc.get_chunk_with_coord(self.raw_chunks, (grid_pos_x, grid_pos_y))
                            fc.paint_chunk_with_color(self.tile_layer, 0, chunk, suspect_layer, [1])
                        elif main.board[grid_pos_y][grid_pos_x] == 9:
                            self.tile_layer[grid_pos_y][grid_pos_x] = 0
                            down_tick = 1
                        else:
                            self.tile_layer[grid_pos_y][grid_pos_x] = 0

        self.debug = debug
        self.flags_left = flags_left
        self.suspect_layer = suspect_layer

        return self.debug, self.flags_left, self.suspect_layer, down_tick


class FinishMode(GameMode):
    def __init__(self, screen, draw_list, board, item_images, font):
        self.screen = screen
        self.draw_list = draw_list
        self.board = board
        self.item_images = item_images
        self.font = font
        self.extra_flags = []
        self.missed_mines = []
        self.correct = []

    def update(self, *args):
        self.screen.fill((100, 100, 100))
        for item in self.extra_flags:
            self.board[item[1]][item[0]] = 10
        for item in self.missed_mines:
            self.board[item[1]][item[0]] = 11
        self.draw_list(self.screen, self.board, self.item_images, (0, 0), (32, 32))

        if len(self.extra_flags) != 0 or len(self.missed_mines) != 0:
            label = self.font.render("You Lost! Press R to Play Again!", 1, (255, 255, 255))
        else:
            label = self.font.render("You Won! Press R to Play Again!", 1, (255, 255, 255))

        text_rect = label.get_rect()
        text_rect.bottom = settings.SCREEN_HEIGHT
        text_rect.center = (settings.SCREEN_WIDTH/2, text_rect.center[1])

        self.screen.blit(label, text_rect)


class ChooseSizeMode(GameMode):
    def __init__(self, screen, font):
        self.screen = screen
        self.button_img = pg.image.load("img/button.png")
        self.buttons = []
        self.origin_point = ((settings.SCREEN_WIDTH-224)//2, (settings.SCREEN_HEIGHT-144)//2)
        self.sizes = ["10x10", "12x10", "15x15", "20x15", "20x20", "25x20"]
        for x in range(3):
            for y in range(2):
                pos_x = self.origin_point[0] + x*(64+16)
                pos_y = self.origin_point[1] + y*(64+16)
                i = y*3 + x
                self.buttons.append(Button(self.screen, self.button_img, pos_x, pos_y, self.sizes[i], font))

    def update(self):
        self.screen.fill((100, 100, 100))
        for button in self.buttons:
            item = button.update()
            if item is not None:
                return item
