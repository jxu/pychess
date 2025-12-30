from move import *

def test_move_uci():
    assert Move(BoardSquare.A1, BoardSquare.C2).uci() == "a1c2"
    assert Move(BoardSquare.E7, BoardSquare.E8,
                promotion=PieceType.QUEEN).uci() == "e7e8q"
