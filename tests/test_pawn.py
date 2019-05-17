"""
Test that pawns behave as expected.
"""

import pytest

from Board import Board
from Pieces import Pawn

def test_white_pawn_init_moves():
    b = Board()
    p = Pawn("WHITE")
    p.set_position(("A",2))
    p.find_available_moves(b)
    moves = p.available_moves
    assert(len(moves)==2)
    assert(("A",3) in moves)
    assert(("A",4) in moves)


def test_black_pawn_init_moves():
    b = Board()
    p = Pawn("BLACK")
    p.set_position(("A",7))
    p.find_available_moves(b)
    moves = p.available_moves
    assert(len(moves)==2)
    assert(("A",6) in moves)
    assert(("A",5) in moves)


def test_pawn_blocked():
    b = Board()
    wp = Pawn("WHITE")
    wp.set_position(("A",4))
    bp = Pawn("BLACK")
    bp.set_position(("A",5))
    b.pieces.append(wp)
    b.pieces.append(bp)
    wp.find_available_moves(b)
    wmoves = wp.available_moves
    assert(len(wmoves)==0)
    bp.find_available_moves(b)
    bmoves = bp.available_moves
    assert(len(bmoves)==0)


def test_pawn_take():
    """
    test that pawns diagonally ahead of one another
    have the potential take square in their list
    of available moves.
    """
    b = Board()
    wp = Pawn("WHITE")
    wp.set_position(("A",4))
    wp2 = Pawn("WHITE")
    wp2.set_position(("A",5))
    bp = Pawn("BLACK")
    bp.set_position(("B",5))
    b.pieces.append(wp)
    b.pieces.append(wp2)
    b.pieces.append(bp)
    wp.find_available_moves(b)
    bp.find_available_moves(b)
    wmoves = wp.available_moves
    assert(len(wmoves)==1)
    assert(("B",5) in wmoves)
    bmoves = bp.available_moves
    assert(len(bmoves)==3)
    assert(("A",4) in bmoves)


def test_pawn_threatens():
    """
    test that a pawn will threaten the two positions diagonally ahead
    """
    b = Board()
    wp = Pawn("WHITE")
    wp.set_position(("A",5))
    b.pieces.append(wp)
    wp.find_positions_threatened(b)
    assert(len(wp.threatens)==1)
    assert(("B",6) in wp.threatens)
    bp = Pawn("BLACK")
    bp.set_position(("C",7))
    b.pieces.append(bp)
    bp.find_positions_threatened(b)
    assert(len(bp.threatens)==2)
    assert(("B",6) in bp.threatens)
    assert(("D",6) in bp.threatens)
