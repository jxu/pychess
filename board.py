"""Piece and board definitions.

0x88 board
https://www.chessprogramming.org/0x88

128-byte array stores the board. Half of the board are normal squares.
the other half of the board is garbage, for boundary checking
the (0-indexed) row and col are indexed in binary as 0rrr0fff
Note that square a1 is 0x00

  a  b  c  d  e  f  g  h < file
8 70 71 72 73 74 75 76 77|78 79 7A 7B 7C 7D 7E 7F
7 60 61 62 63 64 65 66 67|68 69 6A 6B 6C 6D 6E 6F
6 50 51 52 53 54 55 56 57|58 59 5A 5B 5C 5D 5E 5F
5 40 41 42 43 44 45 46 47|48 49 4A 4B 4C 4D 4E 4F
4 30 31 32 33 34 35 36 37|38 39 3A 3B 3C 3D 3E 3F
3 20 21 22 23 24 25 26 27|28 29 2A 2B 2C 2D 2E 2F
2 10 11 12 13 14 15 16 17|18 19 1A 1B 1C 1D 1E 1F
1 00 01 02 03 04 05 06 07|08 09 0A 0B 0C 0D 0E 0F
^ rank

"""


# Piece definitions (negative for black)
EMPTY   = 0
PAWN    = 1
KNIGHT  = 2
BISHOP  = 3
ROOK    = 4
QUEEN   = 5
KING    = 6


PIECE_MAP = {
    'P': PAWN,
    'N': KNIGHT,
    'B': BISHOP,
    'R': ROOK,
    'Q': QUEEN,
    'K': KING
}

def is_piece_black(piece):
    return piece < 0

# 0x88 board coordinate transformations
# A square is represented by an index into a 128 entry 0x88 board
# Uses an int for efficiency

# row 0-7 encodes ranks 1-8
# file index 0-7 encodes files a-h
def sq_index(row, col):
    assert 0 <= row <= 7 and 0 <= col <= 7
    return 16 * row + col


def sq_valid(sq):
    """Check if sq is a valid square on the chessboard."""
    return (sq & 0x88) == 0  # the magic


def sq_col(sq):
    """Get square column 0-7 (corresponds to files 1-8)"""
    return sq & 0x7


def sq_row(sq):
    """Get square row 0-7 (corresponds to rows a-h)"""
    return sq >> 4


def sq_name(sq: int) -> str:
    """Get algebraic coordinates from square index."""
    assert sq_valid(sq)
    return "abcdefgh"[sq_col(sq)] + str(sq_row(sq) + 1)


def sq_name_valid(sq_name: str):
    return ((len(sq_name) == 2) and 
            (sq_name[0] in "abcdefgh") and 
            (sq_name[1] in "12345678"))


class Position:
    """Holds all information to set up a chess position, like FEN."""

    def __init__(self, fen):
        """Constructs a Position from a given FEN string."""

        self.board = [EMPTY] * 128

        fen_split = fen.split()

        # TODO: turn asserts into proper error handling
        assert len(fen_split) == 6
        
        piece_place = fen_split[0]  # board string

        self.black_move = fen_split[1] == 'b'
        assert fen_split[1] in "wb"

        self.castling = fen_split[2]

        self.ep_target = fen_split[3]

        assert (self.ep_target == '-' or 
            (sq_name_valid(self.ep_target) and self.ep_target[1] in "36"))

        self.halfmove = int(fen_split[4])

        self.fullmove = int(fen_split[5])

        # Parse piece placement string
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
                    self.board[sq_index(rank, file)] = piece

                    file += 1

            if file != 8:
                raise ValueError("Incorrect rank placement")


START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_fen():
    start_pos = Position(START_FEN)

    rank0 = (ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK)

    for r in range(8):
        for f in range(8):
            piece = start_pos.board[sq_index(r, f)]
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
    assert start_pos.fullmove == 1



