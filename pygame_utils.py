import os
import pygame as pg


def get_files(path, ending=None):
    if ending is None:
        return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and
            f.endswith("." + ending)]


def draw_list(screen, list_to_draw, sprite_list, origin_point, sprite_dim, skip_items=[]):
    for y, row in enumerate(list_to_draw):
        for x, item in enumerate(row):
            if item in skip_items:
                continue
            pos_x = origin_point[0] + sprite_dim[0]*x
            pos_y = origin_point[1] + sprite_dim[1]*y
            sprite_to_use = sprite_list[item]
            screen.blit(sprite_to_use, (pos_x, pos_y))


def load_images(dir_path, supported_types=("png", "jpg"), keyed=False):
    if keyed:
        loaded = {}
    else:
        loaded = []
    for ending in supported_types:
        for path in get_files(dir_path, ending):
            if keyed:
                name = os.path.split(path)[-1].split(".")[0]
                loaded[name] = pg.image.load(path)
            else:
                loaded.append(pg.image.load(path))
    return loaded
