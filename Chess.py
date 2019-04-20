"""
AI chess program.
"""
import random
from Board import Board, COLNAMES
from Pieces import *


class Game(object):
    """
    One game of chess.
    """
    def __init__(self):
        self.board = Board()
        self.history = []
        self.snapshot = None
        self.reset()

    def add_piece(self, piece, position):
        piece.current_position = position
        self.board.pieces.append(piece)

    def clear(self):
        """
        Clear the board completely
        """
        self.board.pieces = []

    def reset(self):
        """
        Start a new game
        """
        self.board.pieces = []
        for i in range(8):
            self.add_piece(Pawn("WHITE"),(COLNAMES[i], 2))
            self.add_piece(Pawn("BLACK"),(COLNAMES[i], 7))
        row_dict = {"WHITE":1, "BLACK":8 }
        for colour, row in row_dict.items():
            self.add_piece(King(colour),("E",row))
            self.add_piece(Queen(colour),("D",row))
            for col in ["A","H"]:
                self.add_piece(Rook(colour),(col,row))
            for col in ["B","G"]:
                self.add_piece(Knight(colour),(col,row))
            for col in ["C","F"]:
                self.add_piece(Bishop(colour),(col,row))
        self.next_to_play = "WHITE"
        self.update_all_pieces()



    def is_check(self, colour):
        """
        See if the king of selected colour is in check
        """
        king_pos = None
        threatened_positions = []
        for p in self.board.pieces:
            if p.colour == colour and p.piece_type == "King":
                king_pos = p.current_position
                break
        if not king_pos:
            raise Exception("No {} king found!".format(colour))
        if self.board.is_threatened(king_pos, colour):
            return True
        return False


    def is_checkmate(self, colour):
        """
        See if the selected colour king is in check, and 
        if so, are there any moves that would get it out.
        """
        if self.next_to_play != colour:
            return False
        if not self.is_check(colour):
            return False
        ## next player to play is in check.
        ## can they get out?
        possible_moves = []
        for p in self.board.pieces:
            if p.colour == colour:
                for move in p.available_moves:
                    possible_moves.append((p.current_position, move))
                    pass
                pass
            pass
        self.board.save_snapshot()
        for m in possible_moves:
            self.move(m[0], m[1], trial_move=True)
            if not self.is_check(colour):
                print("Can escape check with move {} to {}"\
                      .format(m[0], m[1]))
                self.board.load_snapshot()
                return False
            self.board.load_snapshot()
                    
        ## we have been through all possible moves, and
        ## the king would be in check after all of them
        return True
                

    def is_legal_move(self, colour, start_pos, end_pos):
        """
        determine whether a move is legal.
        """
        if not colour == self.next_to_play:
            print("It is {}'s turn to play".format(self.next_to_play))
            return False
        if self.board.is_empty(start_pos) or \
           self.board.piece_at(start_pos).colour != colour:
            print("{} does not have a piece at {}".format(colour, start_pos))
            return False
        p = self.board.piece_at(start_pos)
        if not end_pos in p.available_moves:
            print("Piece at {} cannot move to {}".format(start_pos,end_pos))
        self.board.save_snapshot()
        ## try the move and see if we would be in check afterwards
        self.move(start_pos, end_pos, trial_move=True)
        if self.is_check(colour):
            print("Cannot move there - king would be in check")
            return False
        

    def move(self, start_pos, end_pos, trial_move=False):
        """
        move a piece on the board, taking the piece
        at the end position if applicable
        """
        if not self.board.is_empty(end_pos):
            self.board.pieces.remove(self.board.piece_at(end_pos))
        p = self.board.piece_at(start_pos)
        p.current_position = end_pos
        self.update_all_pieces()
        p.has_moved = True
        if not trial_move:
            self.next_player_turn()            
        return True


    def update_all_pieces(self):
        for p in self.board.pieces:
            p.find_available_moves(self.board)
            p.find_positions_threatened()


    def next_player_turn(self):
        if self.next_to_play == "WHITE":
            self.next_to_play = "BLACK"
        else:
            self.next_to_play = "WHITE"



class Player(object):
    def __init__(self, colour, is_AI, game):
        self.colour = colour
        self.is_AI = is_AI
        self.game = game

    def move(self, start_pos, end_pos):
        if self.game.is_legal_move(self.colour, start_pos, end_pos):
            moved_ok = game.move(start_pos, end_pos)
            return moved_ok
        else:
            return False

    def choose_move(self):
        all_possible_moves = []
        for p in self.game.board.pieces:
            if p.colour == self.colour:
                for m in p.available_moves:
                    all_possible_moves.append((p.current_position,m))
        moved = False
        while not moved:
            print("Have {} moves to choose from".format(len(all_possible_moves)))
            index = random.randint(0,len(all_possible_moves))
            start,end = all_possible_moves[index]
            moved = self.move(start,end)
            
