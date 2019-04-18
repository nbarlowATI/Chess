"""
Test that bishops behave as expected.
"""

import pytest

from Board import Board
from Pieces import Bishop

def test_bishop_corner():
    b = Board()
    for colour in ["WHITE","BLACK"]:
        bish = Bishop(colour)
        bish.set_position(("A",1))
        bish.find_available_moves(b)
        moves = bish.available_moves
        assert(len(moves)==7)
        assert(("B",2) in moves)
        assert(("C",3) in moves)
        assert(("D",4) in moves)
        assert(("E",5) in moves)
        assert(("F",6) in moves)
        assert(("G",7) in moves)
        assert(("H",8) in moves)


def test_bishop_middle():
    b = Board()
    for colour in ["WHITE","BLACK"]:
        bish = Bishop(colour)
        bish.set_position(("D",4))
        bish.find_available_moves(b)
        moves = bish.available_moves
        assert(len(moves)==13)
        assert(("A",1) in moves)
        assert(("H",8) in moves)
        assert(("G",1) in moves)
        assert(("A",7) in moves)


def test_bishop_block():
    b = Board()
    wb1 = Bishop("WHITE")
    wb1.set_position(("A",1))
    wb2 = Bishop("WHITE")
    wb2.set_position(("B",2))
    b.pieces += [wb1, wb2]
    wb1.find_available_moves(b)
    wb2.find_available_moves(b)
    assert(len(wb1.available_moves)==0)
    assert(len(wb2.available_moves)==8)
    assert(("H",8) in wb2.available_moves)
    assert(("C",3) in wb2.available_moves)
    assert(("A",3) in wb2.available_moves)


def test_bishop_take():
    b = Board()
    wb = Bishop("WHITE")
    wb.set_position(("D",4))
    bb = Bishop("BLACK")
    bb.set_position(("B",2))
    b.pieces += [wb, bb]
    wb.find_available_moves(b)
    bb.find_available_moves(b)
    wmoves = wb.available_moves
    bmoves = bb.available_moves
    assert(len(wmoves)==12)
    assert(("A",1) not in wmoves)
    assert(("H",8) in wmoves)
    assert(("G",1) in wmoves)
    assert(("A",7) in wmoves)
    assert(len(bmoves)==5)
    assert(("D",4) in bmoves)
    assert(("C",1) in bmoves)
    assert(("C",3) in bmoves)
    assert(("A",1) in bmoves)
    assert(("A",3) in bmoves)
