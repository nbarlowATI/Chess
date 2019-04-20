"""
test the functions of the board class, 
e.g. saving/loading snapshots.
"""

import pytest

from Board import Board, COLNAMES
from Pieces import King

def test_empty_square():
    b = Board()
    for col in COLNAMES:
        for row in range(1,9):
            assert(b.is_empty((col,row)))


def test_get_piece():
    b = Board()
    k = King("WHITE")
    k.current_position = ("E",1)
    b.pieces.append(k)
    for col in COLNAMES:
        for row in range(1,9):
            if not (col, row) == ("E",1):
                assert(b.is_empty((col,row)))
            else:
                p = b.piece_at((col, row))
                assert(p.colour=="WHITE")
                assert(p.piece_type=="King")

def test_snapshot():
    b = Board()
    k = King("WHITE")
    k.current_position = ("E",1)
    b.pieces.append(k)
    b.save_snapshot()
    b.pieces[0].current_position = ("F",1)
    assert(b.is_empty(("E",1)))
    assert(not b.is_empty(("F",1)))
    b.load_snapshot()
    assert(b.is_empty(("F",1)))
    assert(not b.is_empty(("E",1)))
