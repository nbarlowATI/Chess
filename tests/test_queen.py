"""
Test that queens behave as expected.
"""

import pytest

from Board import Board
from Pieces import Queen

def test_queen_corner():
    b = Board()
    for colour in ["WHITE","BLACK"]:
        q = Queen(colour)
        q.set_position(("A",1))
        q.find_available_moves(b)
        moves = q.available_moves
        assert(len(moves)==21)
        assert(("B",2) in moves)
        assert(("A",8) in moves)
        assert(("H",1) in moves)
        assert(("H",8) in moves)


def test_queen_middle():
    b = Board()
    for colour in ["WHITE","BLACK"]:
        q = Queen(colour)
        q.set_position(("D",4))
        q.find_available_moves(b)
        moves = q.available_moves
        assert(len(moves)==27)
        assert(("A",1) in moves)
        assert(("H",8) in moves)
        assert(("G",1) in moves)
        assert(("A",7) in moves)
        assert(("A",4) in moves)
        assert(("H",4) in moves)
        assert(("D",1) in moves)
        assert(("D",8) in moves)


def test_queen_block():
    b = Board()
    wq1 = Queen("WHITE")
    wq1.set_position(("A",1))
    wq2 = Queen("WHITE")
    wq2.set_position(("B",2))
    b.pieces += [wq1, wq2]
    wq1.find_available_moves(b)
    wq2.find_available_moves(b)
    assert(len(wq1.available_moves)==14)
    assert(("A",8) in wq1.available_moves)
    assert(("H",1) in wq1.available_moves)
    assert(len(wq2.available_moves)==22)
    assert(("H",8) in wq2.available_moves)
    assert(("C",3) in wq2.available_moves)
    assert(("A",3) in wq2.available_moves)
    assert(("B",8) in wq2.available_moves)
    assert(("H",2) in wq2.available_moves)


def test_queen_take_diag():
    b = Board()
    wq = Queen("WHITE")
    wq.set_position(("D",4))
    bq = Queen("BLACK")
    bq.set_position(("B",2))
    b.pieces += [wq, bq]
    wq.find_available_moves(b)
    bq.find_available_moves(b)
    wmoves = wq.available_moves
    bmoves = bq.available_moves
    assert(len(wmoves)==26)
    assert(("A",1) not in wmoves)
    assert(("H",8) in wmoves)
    assert(("G",1) in wmoves)
    assert(("A",7) in wmoves)
    assert(len(bmoves)==19)
    assert(("D",4) in bmoves)
    assert(("C",1) in bmoves)
    assert(("C",3) in bmoves)
    assert(("A",1) in bmoves)
    assert(("A",3) in bmoves)


def test_queen_take_vert():
    b = Board()
    wq = Queen("WHITE")
    wq.set_position(("D",4))
    bq = Queen("BLACK")
    bq.set_position(("B",4))
    b.pieces += [wq, bq]
    wq.find_available_moves(b)
    bq.find_available_moves(b)
    wmoves = wq.available_moves
    bmoves = bq.available_moves
    assert(len(wmoves)==26)
    assert(("A",4) not in wmoves)
    assert(("A",1) in wmoves)
    assert(("H",8) in wmoves)
    assert(("G",1) in wmoves)
    assert(("A",7) in wmoves)
    assert(len(bmoves)==19)
    assert(("D",4) in bmoves)
    assert(("C",4) in bmoves)
    assert(("C",3) in bmoves)
    assert(("A",4) in bmoves)
    assert(("A",3) in bmoves)
