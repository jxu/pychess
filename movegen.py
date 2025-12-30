from board import *

class Direction(IntEnum):
    N = 16
    E = 1
    S = -16
    W = -1
    NE = N + E
    SE = S + E
    SW = S + W
    NW = N + W


Dir = Direction

KNIGHT_DIRECTIONS = (
    Dir.N + Dir.NW,
    Dir.N + Dir.NE,
    Dir.E + Dir.NE,
    Dir.E + Dir.SE,
    Dir.S + Dir.SE,
    Dir.S + Dir.SW,
    Dir.W + Dir.SW,
    Dir.W + Dir.NW,
)

ROOK_DIRECTIONS : tuple = (Dir.N, Dir.E, Dir.S, Dir.W)
BISHOP_DIRECTIONS : tuple = (Dir.NE, Dir.SE, Dir.SW, Dir.NW)

# doesn't include pawn attacks for now
PIECE_DIRECTIONS = {
    PieceType.KNIGHT: KNIGHT_DIRECTIONS,
    PieceType.ROOK: ROOK_DIRECTIONS,
    PieceType.BISHOP: BISHOP_DIRECTIONS,
    PieceType.QUEEN: ROOK_DIRECTIONS + BISHOP_DIRECTIONS,
    PieceType.KING: ROOK_DIRECTIONS + BISHOP_DIRECTIONS,
}

#     Bitboard style: Attacks are regardless of
#     - what is actually on square
#     - what is occupying the targets
#     - legality
#
#     Move generation is left to another function.

def nonslider_attacks(sq: square, piece_type: PieceType):
    """Generate attacked squares for king and knight

    King castling not handled here
    """
    assert piece_type in (PieceType.KING, PieceType.KNIGHT)

    for direction in PIECE_DIRECTIONS[piece_type]:
        step_square = sq + direction
        if sq_valid(step_square):
            yield step_square


def knight_attacks(sq: square):
    yield from nonslider_attacks(sq, PieceType.KNIGHT)


def king_attacks(sq: square):
    yield from nonslider_attacks(sq, PieceType.KING)


def slider_attacks(sq: square, occupancy: list[PieceCode], piece_type: PieceType):
    """Generate ALL (pseudo-legal) slider attacks by square and occupancy

    Occupancy represents the board and empty or non-empty, ignoring color.

    Includes sliders (rook, bishop, queen)
    Attack includes target but no further.
    """
    assert piece_type in (PieceType.ROOK, PieceType.BISHOP, PieceType.QUEEN)

    directions = PIECE_DIRECTIONS[piece_type]

    for direction in directions:
        # start with one step already
        new_sq = sq + direction

        while sq_valid(new_sq):
            yield new_sq
            if occupancy[new_sq] != PieceCode.EMPTY:
                break
            new_sq += direction


def pawn_attacks(sq:square, color: Color):
    """Pawn attacks only, no forward moves"""
    assert sq_row(sq) not in (0, 7)  # illegal pawn row
    assert color != Color.NEUTRAL

    directions = ([Direction.NE, Direction.NW] if color == Color.WHITE
                  else [Direction.SE, Direction.SW])

    for direction in directions:
        step_square = sq + direction
        if sq_valid(step_square):
            yield step_square


#
# def generate_pawn(self, sq: int):
#     """Generate psuedo-legal pawn movement"""
#     piece = self.board[sq]
#     assert get_piece_type(piece) == PAWN
#     assert sq_row(sq) not in (0, 7)  # illegal pawn position
#
#     # handle both colors at once
#
#     direction = NN if get_color(piece) == WHITE else SS
#     capture_dirs = (NE, NW) if get_color(piece) == WHITE else (SE, SW)
#     home_row = 1 if get_color(piece) == WHITE else 6
#     END_ROWS = (0, 7)
#
#     # try single step, including possible promotion
#     step_sq = sq + direction
#     # sq_valid test not needed because pawn can't be in rows 0 or 7
#     if self.board[step_sq] == EMPTY:
#         # promotions
#         if sq_row(step_sq) in END_ROWS:
#             for promo in (KNIGHT, BISHOP, ROOK, QUEEN):
#                 yield Move(sq, step_sq, promotion=promo)  # record promo
#
#         else:
#             yield Move(sq, step_sq)
#
#
#     # try double step from home row if possible
#     if sq_row(sq) == home_row:
#         step2_sq = step_sq + direction
#         # both squares in front must be empty
#         if self.board[step_sq] == EMPTY and self.board[step2_sq] == EMPTY:
#             yield Move(sq, step2_sq, double_pawn_push=True)
#
#     # try capture (including en passant, based on position's target ep square)
#     for dir in capture_dirs:
#         capture_sq = sq + dir
#         if sq_valid(capture_sq):
#             capture_piece = self.board[capture_sq]
#             if (capture_piece != EMPTY and
#                  get_color(piece) != get_color(capture_piece)):
#
#                 # TODO: consolidate with previous promo yield
#                 if sq_row(capture_sq) in END_ROWS:
#                     for promo in (KNIGHT, BISHOP, ROOK, QUEEN):
#                         yield Move(sq, capture_sq, promotion=promo)  # record promo
#
#                 else:
#                     yield Move(sq, capture_sq, capture=True)
#
#             # EP capture
#             if capture_sq == self.ep_target:
#                 yield Move(sq, capture_sq, capture=True)
#
#
#
# def is_attacked(self, sq):
#     """Determine if square (possibly empty) is attacked by enemy piece
#     Enemy is determined by self's side
#
#     (would be much more efficient with bitboards!)
#     """
#     assert sq_valid(sq)
#
#     attacker_color = invert_color(self.side)
#
#     # loop through whole board
#     for i in range(BOARD_SIZE):
#         if not sq_valid(i): continue
#
#         if get_color(self.board[i]) == attacker_color:
#             attacks = self.generate_piece_attacks(i)
#             for move in attacks:
#                 if move.to == sq:
#                     return True
#
#     return False
#
#
# def generate_castle(self):
#     """Generate possible castling moves (by side to move) in the position.
#
#     To castle:
#     - Must have castling rights (tracked seperately by Position object)
#     - Must have empty spaces in between
#     - Cannot castle out of, through, or into check
#       - Not included even for pseudo-legal
#     """
#
#     # arrays in order of WK, WQ, BK, BQ
#     KING_SQUARES = [(E1, F1, G1), (E1, D1, C1), (E8, F8, G8), (E8, D8, C8)]
#
#     IN_BETWEEN = [(F1, G1), (D1, C1, B1), (F8, G8), (D8, C8, B8)]
#     KING_COLOR = (WHITE, WHITE, BLACK, BLACK)
#
#     for i in range(4):
#         # only generate moves for side to move
#         if KING_COLOR[i] != self.side:
#             continue
#
#         # castling rights
#         if self.castling[i]:
#             assert get_piece_type(self.board[KING_SQUARES[i][0]]) == KING
#             # squares empty
#             if all(self.board[s] == EMPTY for s in IN_BETWEEN[i]):
#                 # king not in check
#                 if all(not self.is_attacked(s) for s in KING_SQUARES[i]):
#                     yield Move(KING_SQUARES[i][0], KING_SQUARES[i][-1], castle=True)
#
#
# def make_move(self, move: Move):
#     """Make pseudo-legal move, updating Position flags
#
#     See https://www.chessprogramming.org/Forsyth-Edwards_Notation
#     for how position is stored
#     """
#
#     # ensure to square doesn't have piece of same color
#     assert get_color(self.board[move.to]) != self.side
#
#     # piece to move
#     piece = self.board[move.from_]
#     # piece should be side to move color
#     assert get_color(piece) == self.side
#
#     # do board update: from square is vacated, to square is replaced
#     self.board[move.from_] = EMPTY
#     self.board[move.to] = piece
#
#
#     # castling rights are based on if kings and rooks have moved
#     # (left their from square) or been captured
#
#     # TODO: make more robust without assuming indices WK, WQ, BK, BQ
#     ROOK_SQUARE = (H1, A1, H8, A8)
#     ROOK_PIECE  = (ROOK, ROOK, -ROOK, -ROOK)
#     KING_SQUARE = (E1, E1, E8, E8)
#     KING_PIECE  = (KING, KING, -KING, -KING)
#
#     for i in range(4):
#         if (self.board[ROOK_SQUARE[i]] != ROOK_PIECE[i] or
#                 self.board[KING_SQUARE[i]] != KING_PIECE[i]):
#             self.castling[i] = False
#
#     # EP target set always if double pawn push (assume valid)
#     if move.double_pawn_push:
#         row = sq_row(move.to)
#         # EP is set behind to_square
#         new_row = row - 1 if get_color(piece) == WHITE else row + 1
#         self.ep_target = sq_index(new_row, sq_col(move.to))
#     else:
#         self.ep_target = None
#
#     # Halfmove clock reset to zero after a capture or pawn move,
#     # increment otherwise
#     if move.capture or get_piece_type(piece) == PAWN:
#         self.halfmove = 0
#     else:
#         self.halfmove += 1
#
#     # Fullmove counter increments on black's move
#     if self.side == BLACK:
#         self.fullmove += 1
#
#     # finally, invert side to move
#     self.side = invert_color(self.side)
