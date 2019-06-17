"""
Test that the points for individual moves are as expected
"""

import pytest
from Chess import Game
from Pieces import King, Queen, Rook, Pawn
from MoveChooser import BestNextPointsPlayer

def test_points_take_pawn():
    g=Game()
    g.clear()
    g.add_piece(Pawn("BLACK"),("C",3))
    g.add_piece(Queen("WHITE"),("C",1))
    assert(len(g.board.pieces)==2)
    g.update_all_pieces()
    player = BestNextPointsPlayer("WHITE")
    points = player.potential_points_for_move(g,"WHITE",(("C",1),("C",3)))
    assert(points==1)


def test_points_queen_escape():
    g=Game()
    g.clear()
    g.add_piece(Pawn("BLACK"),("C",3))
    g.add_piece(Queen("WHITE"),("B",2))
    assert(len(g.board.pieces)==2)
    g.update_all_pieces()
    player = BestNextPointsPlayer("WHITE")
    points = player.potential_points_for_move(g,"WHITE",(("B",2),("B",3)))
    assert(points==9)


def test_points_rook_threaten():
    g=Game()
    g.clear()
    g.add_piece(Pawn("WHITE"),("A",3))
    g.add_piece(Rook("BLACK"),("B",8))
    assert(len(g.board.pieces)==2)
    g.next_to_play = "BLACK"
    g.update_all_pieces()
    player = BestNextPointsPlayer("BLACK")
    points = player.potential_points_for_move(g,"BLACK",(("B",8),("B",4)))
    assert(points==-5)
