"""
AI chess program.
"""
import os
import random
import copy
from datetime import datetime
from Board import Board, COLNAMES
from Pieces import Pawn, Bishop, Knight, Rook, Queen, King
from Spinner import wait_symbol
from Player import Player


DEFAULT_HISTORY_DIR = "/tmp/"

class Game(object):
    """
    One game of chess.
    """
    def __init__(self, verbose=False):
        self.board = Board()
        self.history = []
        self.snapshot = None
        self.reset()
        self.players = {
            "WHITE": None,
            "BLACK": None
        }
        self.snapshots = {}
        self.verbose = verbose
        

    def init_players(self):
        for colour in self.players.keys():
            hum = input("Hello, human!  Would you like to play as {} (y/n)?"\
                        .format(colour))
            if hum == "y":
                self.players[colour] = Player(colour, False)
            else:
                self.players[colour] = Player(colour, True)


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
        self.history = []
        self.update_all_pieces()


    def get_history(self):
        return self.history

    def get_history_str(self):
        history_str = ""
        for move in self.history:
            history_str += "{}{}{}{}".format(move[0][0],
                                             move[0][1],
                                             move[1][0],
                                             move[1][1])
        return history_str
        
    def save_snapshot(self):
        """
        save a snapshot of both the board and the history, and whose turn it is
        """
        snapshot = {
            "next_to_play": self.next_to_play,
            "history": copy.deepcopy(self.history)
        }
        self.board.save_snapshot(self.get_history_str())
        self.snapshots[self.get_history_str()] = snapshot

    def load_snapshot(self, history_str):
        """
        load a snapshot from the history str
        """
        if not history_str in self.snapshots.keys():
            raise RuntimeError("No snapshot {} found".format(history_str))
        self.next_to_play = self.snapshots[history_str]["next_to_play"]
        self.history = self.snapshots[history_str]["history"]
        self.board.load_snapshot(history_str)


    def write_history(self, filename):
        """
        Write out the sequence of moves to a file.
        """
        with open(filename, "w") as outfile:
            for m in self.history:
                outfile.write("{}\n".format(m))

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
        self.update_all_pieces()
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
                if self.verbose:
                    print("Can escape check with move {} to {}"\
                          .format(m[0], m[1]))
                self.board.load_snapshot()
                return False
            self.board.load_snapshot()
        ## we have been through all possible moves, and
        ## the king would be in check after all of them
        return True


    def is_stalemate(self, colour):
        """
        See if the selected colour king is in check, and
        if so, are there any moves that would get it out.
        """
        if self.next_to_play != colour:
            return False
        if self.is_check(colour):
            return False
        ## next player to play is NOT in check.
        ## do they have any legal moves?
        self.update_all_pieces()
        possible_moves = []
        for p in self.board.pieces:
            if p.colour == colour:
                for move in p.available_moves:
                    possible_moves.append((p.current_position, move))
                    pass
                pass
            pass
        if len(possible_moves) == 0:
            return True
        self.board.save_snapshot()
        for m in possible_moves:
            self.move(m[0], m[1], trial_move=True)
            if not self.is_check(colour):
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
            return False
        self.board.save_snapshot()
        ## try the move and see if we would be in check afterwards
        self.move(start_pos, end_pos, trial_move=True)
        if self.is_check(colour):
            if self.verbose:
                print("Cannot move there - king would be in check")
            self.board.load_snapshot()
            return False
        self.board.load_snapshot()
        self.update_all_pieces()
        return True


    def is_castling_move(self, start_pos, end_pos):
        """
        Return True if the piece at start_pos is a king, and
        end_pos is more than one row away.
        """
        if self.board.is_empty(start_pos):
            return False
        if not self.board.piece_at(start_pos).piece_type == "King":
            return False
        start_colnum = COLNAMES.index(start_pos[0])
        end_colnum = COLNAMES.index(end_pos[0])
        is_castling = abs(start_colnum - end_colnum) > 1
        return is_castling


    def castle(self, start_pos, end_pos):
        """
        User castles by moving the king, the rook is then moved
        automatically.
        Assume we've already checked this is a legal move (i.e.
        neither rook nor king have moved before, there's nothing
        in the way).
        """
        if self.board.is_empty(start_pos):
            return False
        k = self.board.piece_at(start_pos)
        k.current_position = end_pos
        ## define a dict so we can get start+finish columns
        ## for the rook, keyed on which column the king will
        ## end up in.
        castling_columns = { "G": ["H","F"],
                             "C": ["A","D"] }
        rook_start = (castling_columns[end_pos[0]][0],end_pos[1])
        rook_end = (castling_columns[end_pos[0]][1],end_pos[1])
        ## now move the rook.
        if self.board.is_empty(rook_start):
            return False
        r = self.board.piece_at((rook_start))
        r.current_position = (rook_end)
        r.has_moved = True
        k.has_moved = True
        return True


    def is_promotion_move(self, start_pos, end_pos):
        """
        Figure out if the requested move would promote a pawn.
        """
        if self.board.is_empty(start_pos):
            return False
        p = self.board.piece_at(start_pos)
        if p.piece_type != "Pawn":
            return False
        return (p.colour=="WHITE" and end_pos[1]==8) \
            or (p.colour=="BLACK" and end_pos[1]==1)


    def promote(self, start_pos, end_pos):
        """
        Replace a pawn by a queen.
        Assume we have already checked it is a legal move.
        """
        if self.board.is_empty(start_pos):
            return False
        pawn = self.board.piece_at(start_pos)
        colour = pawn.colour
        self.board.pieces.remove(pawn)
        self.add_piece(Queen(colour), end_pos)
        return True


    def move(self, start_pos, end_pos, trial_move=False):
        """
        move a piece on the board, taking the piece
        at the end position if applicable
        """
        if self.is_castling_move(start_pos, end_pos):
            castled_ok = self.castle(start_pos, end_pos)
            if not castled_ok:
                return False
        elif self.is_promotion_move(start_pos, end_pos):
            promoted_ok = self.promote(start_pos, end_pos)
            if not promoted_ok:
                return False
        else:
            if not self.board.is_empty(end_pos):
                self.board.pieces.remove(self.board.piece_at(end_pos))
            p = self.board.piece_at(start_pos)
            p.current_position = end_pos
            p.has_moved = True
        self.update_all_pieces()
        if not trial_move:
            self.next_player_turn()
            self.history.append((start_pos, end_pos))
        return True


    def get_all_possible_moves(self, colour):
        """
        Loop through all pieces of specified colour and return 
        list of all legal moves.
        """
        self.update_all_pieces()
        potential_moves = []
        moves = []
        for p in self.board.pieces:
            if p.colour != colour:
                continue
            start_pos = p.current_position
            for end_pos in p.available_moves:
                potential_moves.append((start_pos, end_pos))
        ## now loop through potential moves to see which are legal
        for move in potential_moves:
            if self.is_legal_move(colour, move[0],move[1]):
                moves.append(move)
        return moves
        

    def update_all_pieces(self):
        for p in self.board.pieces:
            p.find_available_moves(self.board)
            p.find_positions_threatened(self.board)


    def next_player_turn(self):
        if self.next_to_play == "WHITE":
            self.next_to_play = "BLACK"
        else:
            self.next_to_play = "WHITE"


    def play(self):
        self.init_players()
        while not ( self.is_checkmate(self.next_to_play) or \
                    self.is_stalemate(self.next_to_play) ):
            print("{} to play..".format(self.next_to_play))
            if self.players[self.next_to_play].is_AI:
                wait_symbol()
                move = self.players[self.next_to_play].choose_move(self)
                print("{}{} to {}{}".format(
                    move[0][0],move[0][1],move[1][0],move[1][1]))
            else:
                self.players[self.next_to_play].input_move(self)
        self.update_all_pieces()
        print("Checkmate!! {} loses.".format(self.next_to_play))
        timestamp = datetime.now().isoformat().replace(":","-")
        history_filename = os.path.join(DEFAULT_HISTORY_DIR,
                                        "match_{}".format(timestamp))
        self.write_history(history_filename)


if __name__ == "__main__":
    g = Game()
    g.play()
