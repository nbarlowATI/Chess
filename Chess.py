"""
AI chess program.
"""
import random
from Board import Board, COLNAMES
from Pieces import Pawn, Bishop, Knight, Rook, Queen, King
from Spinner import wait_symbol

class Game(object):
    """
    One game of chess.
    """
    def __init__(self):
        self.board = Board()
        self.history = []
        self.snapshot = None
        self.reset()
        self.players = {
            "WHITE": None,
            "BLACK": None
        }


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

    def potential_points_for_move(self, colour, start_pos, end_pos):
        """
        return a points value based on:
          (value of any piece taken at end_pos)
        - (value of this piece if threatened at end_pos)
        + (value of this piece if threatened at start_pos)
        """
        points = 0
        this_piece_value = self.board.piece_at(start_pos).value
        if not self.board.is_empty(end_pos):
            points += self.board.piece_at(end_pos).value
        for p in self.board.pieces:
            if p.colour == colour:
                continue
            if start_pos in p.threatens:
                points += this_piece_value
            if end_pos in p.threatens:
                points -= this_piece_value
        return points


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
            print("Cannot move there - king would be in check")
            self.board.load_snapshot()
            return False
        self.board.load_snapshot()
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
        return True


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
        while not self.is_checkmate(self.next_to_play):
            print("{} to play..".format(self.next_to_play))
            if self.players[self.next_to_play].is_AI:
                wait_symbol()
                move = self.players[self.next_to_play].choose_move(self)
                print("{}{} to {}{}".format(
                    move[0][0],move[0][1],move[1][0],move[1][1]))
            else:
                self.players[self.next_to_play].input_move(self)
        print(self.board)
        print("Checkmate!! {} loses.".format(self.next_to_play))




class Player(object):
    def __init__(self, colour, is_AI):
        self.colour = colour
        self.is_AI = is_AI

    def move(self, game, start_pos, end_pos):
        if game.is_legal_move(self.colour, start_pos, end_pos):
            moved_ok = game.move(start_pos, end_pos)
            print("Moved_OK")
            return moved_ok
        else:
            print("Didn't move")
            return False

    def choose_move(self, game):
        all_possible_moves = []
        for p in game.board.pieces:
            if p.colour == self.colour:
                for m in p.available_moves:
                    all_possible_moves.append((p.current_position,m))
        moved = False
        best_points = -999
        best_moves = []
        while not moved:
            for move in all_possible_moves:
                points = game.potential_points_for_move(self.colour,move[0],move[1])
                if points > best_points:
                    best_points = points
                    best_moves = [move]
                elif points == best_points:
                    best_moves.append(move)
            ## we now have a list best_moves which contains the one
            ## or more top-scoring possible moves.  Pick one at random.
            start,end = best_moves[random.randint(0,len(best_moves)-1)]
            print(game.board)
            print("Trying move {} to {}".format(start,end))

            moved = self.move(game, start,end)
            if not moved:
                all_possible_moves.remove(best_move)
                best_points = -999
        return start, end

    def input_move(self, game):
        moved_ok = False
        while not moved_ok:
            print(game.board)
            piece_to_move = input("Please select a {} piece to move:"\
                                  .format(self.colour))
            start_pos = (piece_to_move[0],
                         int(piece_to_move[1]))
            destination = input("Please select square to move to:")
            end_pos = (destination[0],int(destination[1]))
            moved_ok = self.move(game, start_pos, end_pos)
            if not moved_ok:
                print("Illegal move - please try again")


if __name__ == "__main__":
    g = Game()
    g.play()
