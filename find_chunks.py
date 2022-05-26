import main


def find_chunks(board, chunk_num):
    queue = []
    checked_squares = []
    chunks = []
    cur_chunk = []
    for y, row in enumerate(board):
        for x, item in enumerate(row):
            if (x, y) in checked_squares:
                continue
            if item != 0:
                continue
            queue.insert(0, (x, y))
            checked_squares.append((x, y))
            while len(queue) > 0:
                cur_x = queue[-1][0]
                cur_y = queue[-1][1]
                if board[cur_y][cur_x] == 0:
                    cur_chunk.append((cur_x, cur_y))
                    for offset in main.OFFSETS:
                        new_x = cur_x + offset[0]
                        new_y = cur_y + offset[1]
                        if 0 <= new_x < len(board[0]) and 0 <= new_y < len(board):
                            if (new_x, new_y) not in checked_squares and (new_x, new_y) not in queue:
                                queue.insert(0, (new_x, new_y))
                checked_squares.append((cur_x, cur_y))
                del queue[-1]
            chunks.append(cur_chunk[:])
            cur_chunk.clear()
    return chunks


def raw_chunks_to_board(raw_chunks, w, h):
    board = [[0 for _ in range(w)] for _ in range(h)]
    for i, chunk in enumerate(raw_chunks):
        paint_chunk_with_color(board, i+1, chunk)
    return board


def paint_chunk_with_color(board, color, chunk):
    for coord in chunk:
        board[coord[1]][coord[0]] = color


def get_chunk_with_coord(chunks, coord):
    for chunk in chunks:
        if coord in chunk:
            return chunk
    return None


def expand_chunk(board, chunk, ignore_in_expansion=tuple()):
    new_chunk = chunk[:]
    for coord in chunk:
        cur_x = coord[0]
        cur_y = coord[1]
        for offset in main.OFFSETS:
            new_x = cur_x + offset[0]
            new_y = cur_y + offset[1]
            if 0 <= new_x < len(board[0]) and 0 <= new_y < len(board):
                if (new_x, new_y) in new_chunk:
                    continue
                if board[new_y][new_x] in ignore_in_expansion:
                    continue
                new_chunk.append((new_x, new_y))
    return new_chunk
