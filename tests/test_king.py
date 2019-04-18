"""
Test that kings behave as expected.
"""

import pytest

from Board import Board
from Pieces import King

def test_king_no_obstacle():
    b = Board()
    for colour in ["WHITE","BLACK"]:
        k = King(colour)
        k.set_position(("F",4))
        k.find_available_moves(b)
        moves = k.available_moves
        assert(len(moves)==8)
        assert(("E",3) in moves)
        assert(("E",4) in moves)
        assert(("E",5) in moves)
        assert(("F",3) in moves)
        assert(("F",5) in moves)
        assert(("G",3) in moves)
        assert(("G",4) in moves)
        assert(("G",5) in moves)


def test_king_on_edge():
    b = Board()
    for colour in ["WHITE","BLACK"]:
        k = King(colour)
        k.set_position(("F",1))
        k.find_available_moves(b)
        moves = k.available_moves
        assert(len(moves)==5)
        assert(("E",1) in moves)
        assert(("E",2) in moves)
        assert(("F",2) in moves)
        assert(("G",1) in moves)
        assert(("G",2) in moves)


def test_king_in_corner():
    b = Board()
    for colour in ["WHITE","BLACK"]:
        k = King(colour)
        k.set_position(("A",1))
        k.find_available_moves(b)
        moves = k.available_moves
        assert(len(moves)==3)
        assert(("B",1) in moves)
        assert(("B",2) in moves)
        assert(("A",2) in moves)
