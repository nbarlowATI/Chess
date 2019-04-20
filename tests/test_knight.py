"""
Test that knights behave as expected.
"""

import pytest

from Board import Board
from Pieces import Knight

def test_knight_corner():
    b = Board()
    for colour in ["WHITE","BLACK"]:
        k = Knight(colour)
        k.set_position(("A",1))
        k.find_available_moves(b)
        moves = k.available_moves
        assert(len(moves)==2)
        assert(("B",3) in moves)
        assert(("C",2) in moves)


def test_knight_middle():
    b = Board()
    for colour in ["WHITE","BLACK"]:
        k = Knight(colour)
        k.set_position(("D",4))
        k.find_available_moves(b)
        moves = k.available_moves
        assert(len(moves)==8)
        assert(("B",3) in moves)
        assert(("B",5) in moves)
        assert(("F",3) in moves)
        assert(("F",5) in moves)
        assert(("C",2) in moves)
        assert(("E",2) in moves)
        assert(("C",6) in moves)
        assert(("E",6) in moves)


def test_knight_block():
    b = Board()
    wn1 = Knight("WHITE")
    wn1.set_position(("A",2))
    wn2 = Knight("WHITE")
    wn2.set_position(("B",4))
    b.pieces += [wn1, wn2]
    wn1.find_available_moves(b)
    wn2.find_available_moves(b)
    assert(len(wn1.available_moves)==2)
    assert(("C",1) in wn1.available_moves)
    assert(("C",3) in wn1.available_moves)
    assert(len(wn2.available_moves)==5)
    assert(("A",6) in wn2.available_moves)
    assert(("C",2) in wn2.available_moves)
    assert(("C",6) in wn2.available_moves)
    assert(("D",3) in wn2.available_moves)
    assert(("D",5) in wn2.available_moves)


def test_knight_take():
    b = Board()
    wn = Knight("WHITE")
    wn.set_position(("D",4))
    bn = Knight("BLACK")
    bn.set_position(("C",2))
    b.pieces += [wn, bn]
    wn.find_available_moves(b)
    bn.find_available_moves(b)
    wmoves = wn.available_moves
    bmoves = bn.available_moves
    assert(len(wmoves)==8)
    assert(("C",2) in wmoves)
    assert(len(bmoves)==6)
    assert(("D",4) in bmoves)

