from board import *

class Move:
    """Encode move with from square, to square, and flags"""
    def __init__(self, from_ind, to_ind, flags=0):
        assert sqvalid(from_ind)
        assert sqvalid(to_ind)
        assert from_ind != to_ind  # null move

        self.from_ = from_ind
        self.to = to_ind
        self.flags = flags

    # TODO: construct from coordinate notation string?


    def __str__(self):
        """Return pure algebraic coordinate notation, like h7h8q"""

        # TODO: implement promotions
        if self.flags:
            raise NotImplementedError

        return sqname(self.from_) + sqname(self.to)


def test_move_str():
    assert str(Move(0x00, 0x12)) == "a1c2"
