"""
The Board class holds a list of PieceBases, all of which
have a position.
Positions are always represented as a tuple (col, row) with column
in the range A-H and row in the range 1-8, with WHITE starting on
rows 1 and 2 (i.e. the bottom of the board as usually represented).

"""

import copy
import BoardPrinter

COLNAMES = 'ABCDEFGH'
PIECENAMES = {
    "BLACK": {
        "King": u"\u265a",
        "Queen": u"\u265b",
        "Bishop": u"\u265d",
        "Rook": u"\u265c",
        "Knight": u"\u265e",
        "Pawn": u"\u265f"
    },
    "WHITE": {
        "King": u"\u2654",
        "Queen": u"\u2655",
        "Bishop": u"\u2657",
        "Rook": u"\u2656",
        "Knight": u"\u2658",
        "Pawn": u"\u2659"
        }
    }


class PieceBase(object):
    """
    base class for all pieces.
    """
    def __init__(self, colour, piece_type):
        self.colour = colour
        self.piece_type = piece_type
        self.value = 0
        self.active = True
        self.has_moved = False # useful for castling, and pawns.
        self.current_position = None
        self.available_moves = []
        self.threatens = []

    def __repr__(self):
        return  PIECENAMES[self.colour][self.piece_type]

    def set_position(self, pos):
        self.current_position = pos

    def find_available_moves(self, board):
        return []

    def find_positions_threatened(self):
        return []


class Board(object):
    """
    Class representing the chess board.
    Holds a list of pieces that it can interrogate for
    position, and for what squares they are threatening.
    """
    def __init__(self):
        self.pieces = []
        self.snapshot = []
        pass

    def __repr__(self):
        return BoardPrinter.print_board(self.pieces)

    def in_bounds(self, pos):
        """
        Check the position is inside the board boundaries.
        """
        return pos[0] in COLNAMES and pos[1] in list(range(1,9))


    def is_empty(self, pos):
        """
        See if anything is occupying a square.
        """
        for p in self.pieces:
            if p.current_position == pos:
                return False
        return True


    def is_threatened(self, pos, colour):
        """
        See if a piece of the opposing colour is threatening that
        square.
        """
        for p in self.pieces:
            if p.colour == colour:
                continue
            if pos in p.threatens:
                return True


    def piece_at(self, pos):
        """
        return the piece at a specified position.
        """
        for p in self.pieces:
            if p.current_position == pos:
                return p
        return None


    def save_snapshot(self):
        """
        save the current state of the board
        """
        self.snapshot = []
        for p in self.pieces:
            self.snapshot.append(copy.deepcopy(p))


    def load_snapshot(self):
        """
        load the board from a snapshot
        """
        self.pieces = []
        for p in self.snapshot:
            self.pieces.append(copy.deepcopy(p))
