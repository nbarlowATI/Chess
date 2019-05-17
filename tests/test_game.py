"""
Test that the Game class works as expected
"""

import pytest
from Chess import Game
from Pieces import King, Queen, Rook, Pawn

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



def test_castling_king_side():
    g=Game()
    g.move(("G",1),("H",3))
    g.move(("G",8),("H",6))
    g.move(("E",2),("D",3))
    g.move(("E",7),("D",6))
    g.move(("F",1),("E",2))
    g.move(("F",8),("E",7))
    g.update_all_pieces()
    assert(g.is_legal_move("WHITE",("E",1),("G",1)))
    g.move(("E",1),("G",1))
    assert(not g.board.is_empty(("G",1)))
    assert(g.board.piece_at(("G",1)).piece_type == "King")
    assert(not g.board.is_empty(("F",1)))
    assert(g.board.piece_at(("F",1)).piece_type == "Rook")
    ## Now have black do the same
    assert(g.is_legal_move("BLACK",("E",8),("G",8)))
    g.move(("E",8),("G",8))
    assert(not g.board.is_empty(("G",8)))
    assert(g.board.piece_at(("G",8)).piece_type == "King")
    assert(not g.board.is_empty(("F",8)))
    assert(g.board.piece_at(("F",8)).piece_type == "Rook")



def test_points_take_pawn():
    g=Game()
    g.clear()
    g.add_piece(Pawn("BLACK"),("C",3))
    g.add_piece(Queen("WHITE"),("C",1))
    assert(len(g.board.pieces)==2)
    g.update_all_pieces()
    points = g.potential_points_for_move("WHITE",("C",1),("C",3))
    assert(points==1)


def test_points_queen_escape():
    g=Game()
    g.clear()
    g.add_piece(Pawn("BLACK"),("C",3))
    g.add_piece(Queen("WHITE"),("B",2))
    assert(len(g.board.pieces)==2)
    g.update_all_pieces()
    points = g.potential_points_for_move("WHITE",("B",2),("B",3))
    assert(points==9)


def test_points_rook_threaten():
    g=Game()
    g.clear()
    g.add_piece(Pawn("WHITE"),("A",3))
    g.add_piece(Rook("BLACK"),("B",8))
    assert(len(g.board.pieces)==2)
    g.next_to_play = "BLACK"
    g.update_all_pieces()
    points = g.potential_points_for_move("BLACK",("B",8),("B",4))
    assert(points==-5)
