def piece_to_number(piece, fen):
    piece_numbers = {
        'P': 1,
        'N': 2,
        'B': 3,
        'R': 4,
        'Q': 5,
        'K': 6,

        'p': 17,
        'n': 18,
        'b': 19,
        'r': 20,
        'q': 21,
        'k': 22,
    }

    return piece_numbers[piece]


def fen_to_board(fen):
    board = []
    fen = fen.split()

    for i in range(21):
        board.append(7)

    for i in fen[0]:
        if i.isdigit():
            for sq in range(int(i)):
                board.append(0)
        elif i == '/':
            board.append(7)
            board.append(7)
        else:
            board.append(piece_to_number(i, fen))

    for i in range(21):
        board.append(7)

    return board
