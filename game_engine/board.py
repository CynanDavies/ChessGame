from game_engine import FEN_converter


class Board:
    def __init__(self):
        self.board = FEN_converter.fen_to_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        self.selected = None
        self.move_log = None

    def test_status(self, square, colour):
        piece = self.board[square]

        if piece == 0:
            return 0

        elif self.get_colour(piece) != colour:
            if piece != 7:
                return 1
            else:
                return -1
        else:
            return -1

    def get_colour(self, piece_nr):
        if 0 < piece_nr < 17 and piece_nr != 7:
            return 'white'
        elif piece_nr != 7 and piece_nr != 0:
            return 'black'
        else:
            return None