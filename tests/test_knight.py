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
    wb1.find_available_moves(b)
    wb2.find_available_moves(b)
    assert(len(wb1.available_moves)==0)
    assert(len(wb2.available_moves)==8)
    assert(("H",8) in wb2.available_moves)
    assert(("C",3) in wb2.available_moves)
    assert(("A",3) in wb2.available_moves)


#def test_bishop_take():
#    b = Board()
#    wb = Bishop("WHITE")
#    wb.set_position(("D",4))
#    bb = Bishop("BLACK")
#    bb.set_position(("B",2))
#    b.pieces += [wb, bb]
#    wb.find_available_moves(b)
#    bb.find_available_moves(b)
#    wmoves = wb.available_moves
#    bmoves = bb.available_moves
#    assert(len(wmoves)==12)
#    assert(("A",1) not in wmoves)
#    assert(("H",8) in wmoves)
#    assert(("G",1) in wmoves)
#    assert(("A",7) in wmoves)
#    assert(len(bmoves)==5)
#    assert(("D",4) in bmoves)
#    assert(("C",1) in bmoves)
#    assert(("C",3) in bmoves)
#    assert(("A",1) in bmoves)
#    assert(("A",3) in bmoves)
#
