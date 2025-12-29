from movegen import *

def test_knight():
    targets = stepper_attacks(SQ.D5, PieceType.KNIGHT)
    assert sorted(targets) == [
        SQ.C3, SQ.E3, SQ.B4, SQ.F4, SQ.B6, SQ.F6, SQ.C7, SQ.E7
    ]

    targets = stepper_attacks(SQ.H1, PieceType.KNIGHT)
    assert sorted(targets) == [SQ.F2, SQ.G3]


#
# def moves_as_str(moves):
#     """Return moveslist as list of algebraic UCI move strings"""
#     return sorted([str(m) for m in moves])
#
#
# def test_rook():
#     pos = Position("8/2K5/8/2R2P2/8/8/2r5/2k5 w - - 0 1")
#     moves = pos.generate_piece_attacks(SQ("c5"))  # c5 white rook
#
#
#
#
# def test_bishop():
#     pos = Position("8/4P3/8/2Bk4/2b5/8/5p2/5K2 w - - 0 1")
#     moves = pos.generate_piece_attacks(SQ("c5"))  # white bishop
#
#
#
# def test_queen():
#     pos = Position("8/8/8/3Q4/8/8/8/8 w - - 0 1")
#     moves = pos.generate_piece_attacks(SQ("d5"))
#
#
# def test_king_step():
#     # doesn't include castling!
#     pos = Position("8/8/8/3K4/6k1/8/8/8 w - - 0 1")
#     moves = pos.generate_piece_attacks(SQ("d5"))
#
#

#
#
#
# def test_pawn():
#     pos = Position("1k3b2/6P1/8/4pPpP/3p4/1P2N3/1PPP4/1K6 w - e6 0 1")
#
#     # single or double push
#     assert moves_as_str(pos.generate_piece_attacks(SQ("c2"))) == ["c2c3", "c2c4"]
#     assert moves_as_str(pos.generate_piece_attacks(SQ("b2"))) == []
#
#
#     assert moves_as_str(pos.generate_piece_attacks(SQ("d2"))) == ["d2d3"]
#     # e.p.
#     assert moves_as_str(pos.generate_piece_attacks(SQ("f5"))) == ["f5e6", "f5f6"]
#     assert moves_as_str(pos.generate_piece_attacks(SQ("h5"))) == ["h5h6"]
#
#
#     # promotions
#     assert moves_as_str(pos.generate_piece_attacks(SQ("g7"))) == \
#            ["g7f8b", "g7f8n", "g7f8q", "g7f8r",
#     "g7g8b", "g7g8n", "g7g8q", "g7g8r"]
#
#     # black pawn
#     pos.side = BLACK
#     assert moves_as_str(pos.generate_piece_attacks(SQ("d4"))) == ["d4d3", "d4e3"]
#
#     # EP is pseudo-legal here, but not legal
#     pos = Position("8/6bb/8/8/R1pP2k1/4P3/P7/K7 b - - 0 10")
#     assert moves_as_str(pos.generate_pawn(C4)) == ["c4c3"]
#
#
# def test_is_attacked():
#     # Test only for castling
#     pos = Position("r3kN1r/1K6/8/8/2B1R3/8/8/8 b kq - 0 1")
#
#     assert not pos.is_attacked(SQ("f8"))  # occupied but not attacked
#     assert pos.is_attacked(SQ("e8"))  # king in check
#     assert pos.is_attacked(SQ("g8"))
#     assert pos.is_attacked(SQ("b8"))
#     assert pos.is_attacked(SQ("c8"))
#     assert not pos.is_attacked(SQ("d8"))
#
#
# def test_castle():
#     # starting position
#     pos = Position(START_FEN)
#     assert list(pos.generate_castle()) == []
#
#
#     # all castling position
#     pos = Position("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
#
#     moves = pos.generate_castle()
#     # white castling
#     assert moves_as_str(moves) == ["e1c1", "e1g1"]
#     # black castling
#     pos.side = BLACK
#     assert moves_as_str(pos.generate_castle()) == ["e8c8", "e8g8"]
#
#     # can't castle out of check
#     pos = Position("r3k2r/8/2Q5/8/8/8/8/4K3 b kq - 0 1")
#     assert list(pos.generate_castle()) == []
#
#     # can't castle through/into check
#     # kingside through check, queenside is ok here
#     pos = Position("r3k2r/8/8/8/5R2/8/8/4K3 b kq - 0 1")
#     assert moves_as_str(pos.generate_castle()) == ["e8c8"]
#
#     # queenside through check, kingside is ok
#     pos = Position("r3k2r/8/8/8/2R5/8/8/4K3 b kq - 0 1")
#     assert moves_as_str(pos.generate_castle()) == ["e8g8"]
#
#     # b8 is attacked but king doesn't go through
#     pos = Position("r3k2r/8/8/8/1Q6/8/8/4K3 b kq - 0 1")
#     assert moves_as_str(pos.generate_castle()) == ["e8c8"]
#
#
# def test_make_move():
#     # Assume moves are all valid
#     pos = Position(START_FEN)
#
#     # 1. e4
#     pos.make_move(Move(E2, E4, double_pawn_push=True))
#     # pawn actually moved
#     assert pos.board[E2] == EMPTY
#     assert pos.board[E4] == PAWN
#
#     # switched sides after move
#     assert pos.side == BLACK
#
#     # castling rights preserved
#     assert pos.castling == [True]*4
#     # ensure EP square is marked even if it's not possible
#     assert pos.ep_target == E3
#     # halfmove clock reset to zero after pawn move!
#     assert pos.halfmove == 0
#     # fullmove counter not incremented
#     assert pos.fullmove == 1
#
#     # 1. ...c5
#     pos.make_move(Move(C7, C5, double_pawn_push=True))
#
#     assert pos.board[C7] == EMPTY
#     assert pos.board[C5] == -PAWN
#     assert pos.side == WHITE
#     assert pos.castling == [True]*4
#     assert pos.ep_target == C6
#     assert pos.halfmove == 0
#     assert pos.fullmove == 2
#
#     # 2. ...Nf3
#     pos.make_move(Move(G1, F3))
#
#     assert pos.board[G1] == EMPTY
#     assert pos.board[F3] == KNIGHT
#     assert pos.side == BLACK
#     assert pos.castling == [True]*4
#     assert pos.ep_target == None
#     assert pos.halfmove == 1
#     assert pos.fullmove == 2
#
#     # Test castling rights
#     italian_fen = "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"
#     pos = Position(italian_fen)
#     pos.make_move(Move(E1, E2))  # move king
#     assert pos.castling == [False, False, True, True]
#
#     pos = Position(italian_fen)  # recreated
#     pos.make_move(Move(H1, F1))  # move rook
#     assert pos.castling == [False, True, True, True]
#


