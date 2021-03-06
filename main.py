import random


# Constants
WIDTH = 0
HEIGHT = 0
PERCENTAGE = 10
MINE_NUM = int(PERCENTAGE/100 * int(WIDTH*HEIGHT)) + random.randint(-PERCENTAGE//10, PERCENTAGE//10)
OFFSETS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


# Initialize Board
board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]


def populate_board(board_to_populate, mine_number):
    """A function to pick mines randomly"""
    board_to_populate = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for _ in range(mine_number):
        x = random.randint(0, len(board_to_populate[0])-1)
        y = random.randint(0, len(board_to_populate)-1)
        while board_to_populate[y][x] == 9:
            x = random.randint(0, len(board_to_populate[0])-1)
            y = random.randint(0, len(board_to_populate)-1)
        board_to_populate[y][x] = 9
    return board_to_populate


def fill_numbers(board_to_fill):
    for y, row_to_fill in enumerate(board_to_fill):
        for x, item_to_fill in enumerate(row_to_fill):
            if item_to_fill == 9:
                continue
            board_to_fill[y][x] = count_neighbours(board_to_fill, x, y)


def count_neighbours(board_to_fill, x, y):
    num_neighbours = 0
    for offset in OFFSETS:
        offset_x = offset[0]
        offset_y = offset[1]
        new_x = x + offset_x
        new_y = y + offset_y
        if new_x < 0 or new_y < 0:
            continue
        try:
            if board_to_fill[new_y][new_x] == 9:
                num_neighbours += 1
        except IndexError:
            continue
    return num_neighbours


def check_win(mine_map, flags):
    extra_flags = []
    similarities = []
    missed_mines = []
    for i, mine_row, flag_row in zip(range(len(mine_map)), mine_map, flags):
        for j, mine_item, flag_item in zip(range(len(mine_row)), mine_row, flag_row):
            if flag_item == 1:
                if mine_item == 9:
                    similarities.append((j, i))
                else:
                    extra_flags.append((j, i))
            else:
                if mine_item == 9:
                    missed_mines.append((j, i))
    return extra_flags, similarities, missed_mines


def count_items(array, num=0):
    count = 0
    for row in array:
        for item in row:
            if item == num:
                count += 1
    return count
