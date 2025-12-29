"""Position class, as well as movegen"""

from move import *
from enum import IntEnum
from collections.abc import Iterator

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Position:
    """Holds all information in a chess position.

    https://www.chessprogramming.org/Chess_Position

    Similar to FEN:
    - board: Piece placement as list of 128
    - side: Side to move (WHITE or BLACK)
    - castling: Castling rights (4 bools) (not if castling is actually possible)
    - ep_target: EP target square
    - halfmove: Halfmove clock
    - fullmove: Fullmove counter

    Also movegen methods are here for now.
    """

    def __init__(self, fen: str = START_FEN):
        """Constructs a Position from a given FEN string."""

        self.board: list[PieceCode] = [PC.EMPTY] * 128

        fen_split = fen.split()

        if len(fen_split) != 6:
            raise ValueError("Wrong number of FEN fields")
        
        piece_place = fen_split[0]  # board string

        # Parse piece placement string
        place_rank = piece_place.split('/')
        if len(place_rank) != 8:
            raise ValueError("Not 8 ranks")

        for i in range(8):
            row = 7 - i
            col = 0

            for c in place_rank[i]:
                if c.isdigit():
                    col += int(c)  # skip c spaces
                else:
                    is_black = c.islower()
                    c = c.upper()  # reduce piece checking cases

                    try:
                        # colored
                        piece = PieceCode(PIECETYPE_MAP[c])
                    except KeyError:
                        raise ValueError("Unrecognized piece")

                    # set negative if black
                    if is_black:
                        piece = invert_piece(piece)
                    self.board[sq_index(row, col)] = piece

                    col += 1

            if col != 8:
                raise ValueError("Incorrect lengh row")

        # Parse the rest
        # Side to move
        if fen_split[1] == 'w':
            self.side = Color.WHITE
        elif fen_split[1] == 'b':
            self.side = Color.BLACK
        else:
            raise ValueError("invalid side")

        # Castling rights
        self.castling = [False] * 4
        castling = fen_split[2]
        if castling != '-':
            for c in castling:
                self.castling[CASTLE_MAP[c]] = True

        # EP target
        ep_target_raw = fen_split[3]

        if ep_target_raw == '-':
            self.ep_target = None
        elif is_coord_valid(ep_target_raw) and ep_target_raw[1] in "36":
            self.ep_target = sq_from_coord(ep_target_raw)
        else:
            raise ValueError("Invalid EP target")

        # Half move and full move counters
        self.halfmove = int(fen_split[4])
        self.fullmove = int(fen_split[5])
