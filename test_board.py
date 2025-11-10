from board import *

def test_sq_valid():
    assert sq_valid(0x00)
    assert sq_valid(0x77)
    assert not sq_valid(0x80)
    assert not sq_valid(-1)


def test_sq_name():
    assert sq_name(0x00) == "a1"
    assert sq_name(0x57) == "h6"


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




