import time
from game_engine.board import Board


def check_if_bit_is_set(bit, test_number):
    if test_number & 1 << (bit - 1):
        return True
    else:
        return False


def set_bit(value, bit):
    return value | (1 << bit)


def clear_bit(value, bit):
    return value & ~(1 << bit)


def test_time():
    differences = []

    for i in range(10):

        start_time = time.time()
        for i in range(10000):
            pass
        end_time = time.time()
        time1 = end_time - start_time

        start_time = time.time()
        for i in range(10000):
            pass
        end_time = time.time()
        time2 = end_time - start_time

        differences.append(time1 / time2)

    total = 0

    for i in differences:
        total += i

    print(f'First function takes {time1} seconds')
    print(f'Second function takes {time2} seconds')
    print(f'The first function takes {total / 10} of the anmount of time that the second one does')


def check_direction(chess_board, starting_square, colour, x_dir, y_dir, move_storage, recursive):
    square = starting_square + x_dir + y_dir * 10
    status = chess_board.test_status(square, colour)
    if status == 1:
        move_storage.append(square)
        return move_storage
    elif status == 0:
        move_storage.append(square)
        if recursive:
            check_direction(chess_board, square, colour, x_dir, y_dir, move_storage, True)
        return move_storage
    elif status == -1:
        return move_storage
    else:
        raise ValueError('Something went wrong with the status testing of a square')


def bishop(chess_board, starting_square):
    moves = []
    colour = chess_board.get_colour(chess_board.board[starting_square])
    for row in [x for x in range(-1, 2) if x != 0]:
        for col in [y for y in range(-1, 2) if y != 0]:
            temp = check_direction(chess_board, starting_square, colour, row, col, [], True)
            for i in temp:
                moves.append(i)
    return moves


def rook(chess_board, starting_square):
    moves = []
    colour = chess_board.get_colour(chess_board.board[starting_square])
    for row in [x for x in range(-1, 2)]:
        for col in [y for y in range(-1, 2)]:
            if abs(row) != abs(col):
                temp = check_direction(chess_board, starting_square, colour, row, col, [], True)
                for i in temp:
                    moves.append(i)
    return moves


def queen(chess_board, starting_square):
    moves = []
    colour = chess_board.get_colour(chess_board.board[starting_square])
    for row in [x for x in range(-1, 2)]:
        for col in [y for y in range(-1, 2)]:
            if row != 0 or col != 0:
                temp = check_direction(chess_board, starting_square, colour, row, col, [], True)
                for i in temp:
                    moves.append(i)
    return moves


def king(chess_board, starting_square, threats):
    moves = []
    colour = chess_board.get_colour(chess_board.board[starting_square])
    for row in [x for x in range(-1, 2)]:
        for col in [y for y in range(-1, 2)]:
            if row != 0 or col != 0:
                temp = check_direction(chess_board, starting_square, colour, row, col, [], False)
                for i in temp:
                    moves.append(i)

    if chess_board.board[starting_square] == clear_bit(chess_board.board[starting_square], 3):
        if chess_board.board[starting_square + 3] == clear_bit(chess_board.board[starting_square + 3], 3):
            if chess_board.board[starting_square + 1] == 0 and chess_board.board[starting_square + 2] == 0:
                if chess_board.board[starting_square + 1] not in threats and chess_board[starting_square + 2] not in threats:
                    moves.append(starting_square + 2)

        if chess_board.board[starting_square - 4] == clear_bit(chess_board.board[starting_square - 4], 3):
            if chess_board.board[starting_square - 1] == 0 and chess_board.board[starting_square - 2] == 0 and chess_board.board[starting_square - 3] == 0:
                if chess_board.board[starting_square - 1] not in threats and chess_board[starting_square - 2] not in threats:
                    moves.append(starting_square - 2)

    # Rook movement

    return moves


def pawn(chess_board, starting_square):
    moves = []
    colour = chess_board.get_colour(chess_board.board[starting_square])
    if colour == 'black':
        direction = 1
    else:
        direction = -1

    if chess_board.test_status(starting_square + direction * 10, colour) == 0:
        moves.append(starting_square + direction * 10)

        if chess_board.board[starting_square] == 1 or chess_board.board[starting_square] == 17:
            if chess_board.test_status(starting_square + direction * 20, colour) == 0:
                moves.append(starting_square + direction * 20)

    if chess_board.test_status(starting_square + direction * 10 - 1, colour) == 1:
        moves.append(starting_square + direction * 10 - 1)

    if chess_board.test_status(starting_square + direction * 10 + 1, colour) == 1:
        moves.append(starting_square + direction * 10 + 1)

    return moves


def knight(chess_board, starting_square):
    moves = []
    colour = chess_board.get_colour(chess_board.board[starting_square])
    temp_moves = [starting_square - 21, starting_square -19, starting_square - 12, starting_square - 8, starting_square + 8, starting_square + 12, starting_square + 19, starting_square + 21]
    for i in temp_moves:
        if chess_board.test_status(i, colour) != -1:
            moves.append(i)

    return moves


def all(board, colour):
    threats = []
    index = -1
    for i in board.board:
        index += 1
        if board.get_colour(i) == colour:
            moves = move_for_type(i, board, index)
            for option in moves:
                threats.append(option)

    threats = list(dict.fromkeys(threats))
    return threats


def move(chess_board, starting_square, destination_square):
    piece_type = chess_board.board[starting_square]
    moves = move_for_type(piece_type, chess_board, starting_square)

    if destination_square in moves:
        chess_board.board[destination_square] = set_bit(chess_board.board[starting_square], 3)
        chess_board.board[starting_square] = 0
    else:
        print('invalid move')

    if moves is []:
        print('no moves')


def move_for_type(piece_type, chess_board, starting_square):
    piece_type = clear_bit(piece_type, 3)
    piece_type = clear_bit(piece_type, 4)

    if piece_type == 1:
        return pawn(chess_board, starting_square)

    elif piece_type == 2:
        return knight(chess_board, starting_square)

    elif piece_type == 3:
        return bishop(chess_board, starting_square)

    elif piece_type == 4:
        return rook(chess_board, starting_square)

    elif piece_type == 5:
        return queen(chess_board, starting_square)

    elif piece_type == 6:
        return king(chess_board, starting_square)

    else:
        return []


test = Board()
print(king(test, 25, None))