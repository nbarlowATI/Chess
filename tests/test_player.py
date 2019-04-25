
import pytest

from Chess import Game, Player

def test_player_legal_move():
    g=Game()
    pw = Player("WHITE",is_AI=False)
    moved = pw.move(g,("A",2),("A",3))
    assert(moved)
    assert(g.board.is_empty(("A",2)))
    assert(g.board.piece_at(("A",3)).piece_type=="Pawn")
    assert(g.board.piece_at(("A",3)).colour=="WHITE")
    assert(g.next_to_play=="BLACK")


def test_player_illegal_move():
    g=Game()
    pw = Player("WHITE",is_AI=False)
    moved = pw.move(g,("A",1),("F",3))
    assert(not moved)
    assert(g.board.is_empty(("F",3)))
    assert(g.board.piece_at(("A",1)).colour=="WHITE")
    assert(g.board.piece_at(("A",1)).piece_type=="Rook")
    assert(g.next_to_play=="WHITE")
