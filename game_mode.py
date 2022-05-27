import pygame as pg
import find_chunks as fc
from settings import *


class GameMode:
    def update(self, *args):
        return

    def check_events(self, e):
        return


class PlayGameMode(GameMode):
    def __init__(self, screen, draw_list, main, item_images, debug, debug_map, debug_tile_images, tile_layer,
                 tile_images, suspect_layer, question_mark_images, raw_chunks, down_tick, flags_left):
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

        draw_list(screen, main.board, item_images, (0, 0), (32, 32))
        if debug:
            draw_list(screen, debug_map, debug_tile_images, (0, 0), (32, 32), [0])
        draw_list(screen, tile_layer, tile_images, (0, 0), (32, 32), [0])
        draw_list(screen, suspect_layer, question_mark_images, (0, 0), (32, 32), [0])

        pressed = pg.mouse.get_pressed()
        if pressed[0]:
            pos = pg.mouse.get_pos()
            grid_pos_x = pos[0] // 32
            grid_pos_y = pos[1] // 32
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

        self.debug = debug
        self.flags_left = flags_left
        self.suspect_layer = suspect_layer

        return self.debug, self.flags_left, self.suspect_layer


class LoseMode(GameMode):
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

        label = self.font.render("You Lost!", 0, (255, 255, 255))
        text_rect = label.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(label, text_rect)


class WinMode(GameMode):
    def __init__(self, screen, draw_list, board, item_images, font):
        self.screen = screen
        self.draw_list = draw_list
        self.board = board
        self.item_images = item_images
        self.font = font

    def update(self, *args):
        self.screen.fill((100, 100, 100))
        self.draw_list(self.screen, self.board, self.item_images, (0, 0), (32, 32))

        label = self.font.render("You Won!", 0, (255, 255, 255))
        text_rect = label.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(label, text_rect)