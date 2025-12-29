from position import *

def test_position():
    start_pos = Position(START_FEN)

    # Starting board by increasing row (upside down)
    BOARD = [
        [PC.WROOK,PC.WKNIGHT,PC.WBISHOP,PC.WQUEEN,PC.WKING,PC.WBISHOP,PC.WKNIGHT,PC.WROOK],
        [PC.WPAWN]*8,
        [PC.EMPTY]*8,
        [PC.EMPTY]*8,
        [PC.EMPTY]*8,
        [PC.EMPTY]*8,
        [PC.BPAWN]*8,
        [PC.BROOK,PC.BKNIGHT,PC.BBISHOP,PC.BQUEEN,PC.BKING,PC.BBISHOP,PC.BKNIGHT,PC.BROOK],
    ]

    for r in range(8):
        for c in range(8):
            assert start_pos.board[sq_index(r, c)] == BOARD[r][c]

    assert start_pos.side == Color.WHITE
    assert start_pos.castling == [True]*4
    assert start_pos.ep_target == None
    assert start_pos.halfmove == 0
    assert start_pos.fullmove == 1

    # Check position by black's move with EP square
    fen_1e4 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"

    # modify start board
    BOARD[3][4] = PC.WPAWN
    BOARD[1][4] = PC.EMPTY

    pos1 = Position(fen_1e4)

    for r in range(8):
        for c in range(8):
            assert pos1.board[sq_index(r, c)] == BOARD[r][c]


    assert pos1.side == Color.BLACK
    assert pos1.castling == [True]*4
    assert pos1.ep_target == sq_from_coord("e3")
    assert pos1.halfmove == 0
    assert pos1.fullmove == 1
