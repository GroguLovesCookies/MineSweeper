import random


# Constants
WIDTH = int(input("Enter Width: "))
HEIGHT = int(input("Enter Height: "))
MINE_NUM = int(0.1 * int(WIDTH*HEIGHT)) + random.randint(-1, 1)
OFFSETS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


# Initialize Board
board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]


def populate_board(board_to_populate, mine_number):
    """A function to pick mines randomly"""
    for _ in range(mine_number):
        x = random.randint(0, len(board_to_populate[0])-1)
        y = random.randint(0, len(board_to_populate)-1)
        board_to_populate[y][x] = 9


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


populate_board(board, MINE_NUM)
fill_numbers(board)
for row in board:
    for item in row:
        if item == 9:
            print("M", end=" ")
        else:
            print(item, end=" ")
    print("")
