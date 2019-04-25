"""
Test that the Game class works as expected
"""

import pytest
from Chess import Game
from Pieces import King, Queen, Rook

def test_initial_setup():
    g = Game()
    assert(len(g.board.pieces)==32)
    for p in g.board.pieces:
        assert(p.has_moved==False)


def test_white_pawn_move():
    g=Game()
    g.move(("A",2),("A",4))
    assert(g.board.is_empty(("A",2)))
    assert(g.board.piece_at(("A",4)).has_moved==True)
    assert(g.next_to_play=="BLACK")

def test_black_pawn_move():
    g=Game()
    assert(not g.is_legal_move("BLACK",("A",7),("A",5)))
           

def test_take():
    g = Game()
    g.move(("A",2),("A",7))
    assert(len(g.board.pieces)==31)
    assert(g.board.piece_at(("A",7)).colour=="WHITE")

def test_check():
    g=Game()
    g.move(("A",2),("D",7))
    assert(g.is_check("BLACK"))


def test_checkmate():
    g=Game()
    g.clear()
    g.add_piece(King("BLACK"),("H",8))
    g.add_piece(Queen("WHITE"),("G",7))
    g.add_piece(Rook("WHITE"),("G",6))
    assert(len(g.board.pieces)==3)
    g.update_all_pieces()
    g.next_player_turn()
    assert(g.is_check("BLACK"))
    assert(g.is_checkmate("BLACK"))
