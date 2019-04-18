"""
Test that rooks behave as expected.
"""

import pytest

from Board import Board
from Pieces import Rook

def test_rook_no_obstacle():
    b = Board()
    for colour in ["WHITE","BLACK"]:
        r = Rook(colour)
        r.set_position(("F",4))
        r.find_available_moves(b)
        moves = r.available_moves
        assert(len(moves)==14)
        assert(("E",4) in moves)
        assert(("G",4) in moves)
        assert(("F",3) in moves)
        assert(("F",5) in moves)
        assert(("F",8) in moves)
        assert(("F",1) in moves)
        assert(("A",4) in moves)
        assert(("H",4) in moves)


def test_rook_on_edge():
    b = Board()
    for colour in ["WHITE","BLACK"]:
        r = Rook(colour)
        r.set_position(("F",1))
        r.find_available_moves(b)
        moves = r.available_moves
        assert(len(moves)==14)
        assert(("A",1) in moves)
        assert(("H",1) in moves)
        assert(("F",8) in moves)

def test_rook_blocked():
    b = Board()
    r1 = Rook("WHITE")
    r1.set_position(("B",1))
    r2 = Rook("WHITE")
    r2.set_position(("B",2))
    b.pieces += [r1,r2]
    r1.find_available_moves(b)
    r2.find_available_moves(b)
    assert(len(r1.available_moves)==7)
    assert(len(r2.available_moves)==13)


def test_rook_take():
    b = Board()
    r1 = Rook("WHITE")
    r1.set_position(("B",2))
    r2 = Rook("BLACK")
    r2.set_position(("F",2))
    b.pieces += [r1,r2]
    r1.find_available_moves(b)
    r2.find_available_moves(b)
    assert(len(r1.available_moves)==12)
    assert(len(r2.available_moves)==13)
