# Piece definitions (negative for black)
EMPTY = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

PIECE_MAP = {'P': PAWN, 'N': KNIGHT, 'B': BISHOP, 'R': ROOK,
             'Q': QUEEN, 'K': KING}


# 0x88 board coordinate transformations (all 0-indexed)
# rank index 0-7 encodes ranks 1-8
# file index 0-7 encodes files a-h
def sqind(rank07: int, file07: int) -> int:
    return 16 * rank07 + file07


def sqvalid(ind):
    return ind & 0x88 == 0  # the magic


# needed?
def sqrank(ind):
    return ind & 0x7


def sqfile(ind):
    assert (ind >> 4) < 8
    return ind >> 4


def sqname(ind: int) -> str:
    """Get algebraic coordinates from square index."""
    assert sqvalid(ind)
    return "abcdefgh"[sqrank(ind)] + str(sqfile(ind) + 1)


class Position:
    """Holds all information to set up a chess position, like FEN.

    0x88 board
    the other half of the board is garbage, for boundary checking
    the 0-indexed rank and file are indexed as %0rrr0fff


       a  b  c  d  e  f  g  h
    8 70 71 72 73 74 75 76 77|78 79 7A 7B 7C 7D 7E 7F
    7 60 61 62 63 64 65 66 67|
    6 50 51 52 53 54 55 56 57|
    5 40 41 42 43 44 45 46 47|
    4 30 31 32 33 34 35 36 37|
    3 20 21 22 23 24 25 26 27|
    2 10 11 12 13 14 15 16 17|
    1 00 01 02 03 04 05 06 07|

    """

    board = [EMPTY] * 128
    black_move = False
    castling = None  # subset of "KQkq" for now

    def __init__(self, fen):
        (piece_place, side, self.castling, self.ep_target,
         halfmove, movecounter) = fen.split()

        place_rank = piece_place.split('/')
        if len(place_rank) != 8:
            raise ValueError("Not 8 ranks")

        for i in range(8):
            rank = 7 - i
            file = 0

            for c in place_rank[i]:
                if c.isdigit():
                    file += int(c)  # skip c spaces
                else:
                    is_black = c.islower()
                    c = c.upper()  # reduce piece checking cases

                    try:
                        piece = PIECE_MAP[c]
                    except KeyError:
                        raise ValueError("Unrecognized piece")

                    # set negative if black
                    if is_black:
                        piece = -piece
                    self.board[sqind(rank, file)] = piece

                    file += 1

            if file != 8:
                raise ValueError("Incorrect rank placement")

        self.black_move = side == 'b'
        self.halfmove = int(halfmove)
        self.movecounter = int(movecounter)





def test_fen():
    start_pos = \
        Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    rank0 = (ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK)

    for r in range(8):
        for f in range(8):
            piece = start_pos.board[sqind(r, f)]
            if r == 0:
                assert piece == rank0[f]
            elif r == 1:
                assert piece == PAWN
            elif r == 6:
                assert piece == -PAWN
            elif r == 7:
                assert piece == -rank0[f]
            else:
                assert piece == EMPTY

    assert start_pos.castling == "KQkq"
    assert start_pos.black_move == False
    assert start_pos.halfmove == 0
    assert start_pos.movecounter == 1


def test_sqvalid():
    assert sqvalid(0x00)
    assert sqvalid(0x77)
    assert not sqvalid(0x80)
    assert not sqvalid(-1)


def test_sqname():
    assert sqname(0x00) == "a1"
    assert sqname(0x77) == "h8"
