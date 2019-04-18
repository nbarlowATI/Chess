"""
AI chess program.
"""

from Board import Board, COLNAMES
from Pieces import *


class Game(object):
    """
    One game of chess.
    """
    def __init__(self):
        self.board = Board()
        self.reset()

    def reset(self):
        """
        Start a new game
        """
        for i in range(8):
            wp = Pawn("WHITE")
            wp.set_position((COLNAMES[i], 2))
            self.board.pieces.append(wp)
            bp = Pawn("BLACK")
            bp.set_position((COLNAMES[i], 7))
            self.board.pieces.append(bp)
        wk = King("WHITE")
        wk.set_position(("E",1))
        bk = King("BLACK")
        bk.set_position(("E",8))
        self.board.pieces.append(wk)
        self.board.pieces.append(bk)
        for i in ["A","H"]:
            wr = Rook("WHITE")
            wr.set_position((i,1))
            self.board.pieces.append(wr)
            br = Rook("BLACK")
            br.set_position((i,8))
            self.board.pieces.append(br)


        self.next_to_play = "WHITE"



    def move_piece(self, piece, position):
        """
        place a piece on the board.
        """
        pass
