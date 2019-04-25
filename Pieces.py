"""
Classes representing the different chess pieces.
All pieces generate and hold:
* A list of squares they can legally move into
* A list of squares they are currently threatening (i.e. able to take
  an opposing piece in that square).
(The latter is useful for calculating if a king is (or would be) in 'check'.)
"""

from Board import Board, COLNAMES, PieceBase


class Pawn(PieceBase):
    def __init__(self, colour):
        super().__init__(colour, "Pawn")


    def find_potential_positions(self):
        """
        Get all the positions one-square ahead,
        two-squares ahead, and diagonally ahead
        of the current position.
        """
        current_col = self.current_position[0]
        take_col_indices = [
            COLNAMES.index(current_col) - 1,
            COLNAMES.index(current_col) + 1
        ]
        if self.colour == "WHITE":
            direction = 1
        else:
            direction = -1

        pos_one_ahead = (self.current_position[0],
                         self.current_position[1]+direction)
        pos_two_ahead = (self.current_position[0],
                         self.current_position[1]+2*direction)
        pos_takes = []
        for i in take_col_indices:
            if i in range(8):
                pos_takes.append((COLNAMES[i],
                                  self.current_position[1]+direction))
                pass
            pass

        return pos_one_ahead, pos_two_ahead, pos_takes


    def find_available_moves(self, board):
        self.available_moves = []
        one_ahead, two_ahead, takes = self.find_potential_positions()
        if board.is_empty(one_ahead):
            self.available_moves.append(one_ahead)
            if not self.has_moved and board.is_empty(two_ahead):
                self.available_moves.append(two_ahead)
        for pt in takes:
            if not board.is_empty(pt) and \
               board.piece_at(pt).colour != self.colour:
                self.available_moves.append(pt)
                pass
            pass
        pass


    def find_positions_threatened(self):
        """
        Return the squares that this pawn is
        currently threatening.
        """
        self.threatens = self.find_potential_positions()[2]


class King(PieceBase):

    def __init__(self, colour):
        super().__init__(colour, "King")
        self.has_castled = False

    def find_potential_positions(self):
        """
        Find all the squares one around the
        current position, plus the endpoints of
        castling.
        """
        adjacent_positions = []
        current_colnum = COLNAMES.index(self.current_position[0])
        for row_move in range(-1,2):
            new_row = self.current_position[1] + row_move
            if new_row not in range(1,9):
                continue
            for col_move in range(-1,2):
                if row_move==0 and col_move==0:
                    continue
                new_colnum = current_colnum + col_move
                if new_colnum not in range(8):
                    continue
                adjacent_positions.append((COLNAMES[new_colnum],
                                           new_row))
        ## we will deal with castling separately
        if self.colour == "WHITE":
            castling_positions = [("C",1),("G",1)]
        else:
            castling_positions = [("C",8),("G",8)]
        return adjacent_positions, castling_positions


    def find_available_moves(self, board):
        self.available_moves = []
        adj_pos, castle_pos = self.find_potential_positions()
        # test whether we can move to adjacent square
        for pos in adj_pos:
            if board.is_threatened(pos, self.colour):
                continue
            if board.is_empty(pos):
                self.available_moves.append(pos)
            elif board.piece_at(pos).colour != self.colour:
                self.available_moves.append(pos)
                pass
            pass
        # test whether we can castle
        for pos in castle_pos:
            if self.can_castle(board, pos):
                self.available_moves.append(pos)
                pass
            pass
        pass


    def can_castle(self, board, pos):
        """
        Can we castle to given position?
        """
        if self.has_moved:
            return False

        row = 1 if self.colour=="WHITE" else 8
        current_colnum = COLNAMES.index(self.current_position[0])
        target_colnum = COLNAMES.index(pos[0])
        if target_colnum < current_colnum:
            direction = -1
            rook_column = "A"
        else:
            direction = 1
            rook_column = "H"
        ## check if the rook is there and hasn't moved
        if board.is_empty((rook_column, row)):
            return False
        else:
            p =  board.piece_at((rook_column,row))
            if p.piece_type != "Rook" or p.has_moved:
                return False
        ## now check if the coast is clear to the target square
        ## (no other pieces, not going through check.
        for colnum in range(current_colnum,
                            target_colnum+direction,
                            direction):
            col = COLNAMES[colnum]
            if board.is_threatened((col, row), self.colour):
                return False
            if colnum != current_colnum and not board.is_empty((col,row)):
                return False


    def find_positions_threatened(self):
        """
        Return the squares that this King is
        currently threatening, i.e. all adjacent squares.
        """
        self.threatens = self.find_potential_positions()[0]



class Rook(PieceBase):
    def __init__(self, colour):
        super().__init__(colour, "Rook")


    def find_available_moves(self, board):
        self.available_moves = []
        current_col = self.current_position[0]
        current_row = self.current_position[1]
        current_colnum = COLNAMES.index(current_col)
        loop_configs = {"left":  range(current_colnum-1,-1,-1),
                        "right": range(current_colnum+1,8),
                        "up": range(current_row+1,9),
                        "down": range(current_row-1,0,-1)
                        }
        ## go as far as we can in each direction
        for direction, loop in loop_configs.items():
            for i in loop:
                if direction == "left" or direction == "right":
                    pos = (COLNAMES[i], current_row)
                else:
                    pos = (COLNAMES[current_colnum], i)
                if board.is_empty(pos):
                    self.available_moves.append(pos)
                elif board.piece_at(pos).colour != self.colour:
                    ## opposite colour piece - can take,
                    ## but can't move beyond
                    self.available_moves.append(pos)
                    break
                else:
                    ## same colour piece - can't go there or beyond
                    break


    def find_positions_threatened(self):
        """
        Return the squares that this rook is
        currently threatening.  In practice, this is the same as
        the list of available moves
        """
        self.threatens = self.available_moves


class Bishop(PieceBase):

    def __init__(self, colour):
        super().__init__(colour, "Bishop")

    def find_available_moves(self, board):
        self.available_moves = []
        starting_row = self.current_position[1]
        starting_colnum = COLNAMES.index(self.current_position[0])
        step_directions = [(1,1),(1,-1),(-1,1),(-1,-1)]
        for direction in step_directions:
            colnum = starting_colnum + direction[0]
            row = starting_row + direction[1]
            while colnum in range(8) and row in range(1,9):
                pos = (COLNAMES[colnum],row)
                if board.is_empty(pos):
                    self.available_moves.append(pos)
                elif board.piece_at(pos).colour != self.colour:
                    self.available_moves.append(pos)
                    break
                else:
                    break
                colnum += direction[0]
                row += direction[1]

    def find_positions_threatened(self):
        self.threatens = self.available_moves


class Queen(PieceBase):

    def __init__(self, colour):
        super().__init__(colour, "Queen")

    def find_available_moves(self, board):
        self.available_moves = []
        starting_row = self.current_position[1]
        starting_colnum = COLNAMES.index(self.current_position[0])
        step_directions = [
            (1,0),(0,1),(-1,0),(0,-1),
            (1,1),(1,-1),(-1,1),(-1,-1)
        ]
        for direction in step_directions:
            colnum = starting_colnum + direction[0]
            row = starting_row + direction[1]
            while colnum in range(8) and row in range(1,9):
                pos = (COLNAMES[colnum],row)
                if board.is_empty(pos):
                    self.available_moves.append(pos)
                elif board.piece_at(pos).colour != self.colour:
                    self.available_moves.append(pos)
                    break
                else:
                    break
                colnum += direction[0]
                row += direction[1]

    def find_positions_threatened(self):
        self.threatens = self.available_moves


class Knight(PieceBase):

    def __init__(self, colour):
        super().__init__(colour, "Knight")

    def find_available_moves(self, board):
        self.available_moves = []
        starting_row = self.current_position[1]
        starting_colnum = COLNAMES.index(self.current_position[0])
        steps = [
            (1,2),(2,1),(-1,2),(2,-1),
            (1,-2),(-2,-1),(-2,1),(-1,-2)
        ]
        for step in steps:
            colnum = starting_colnum + step[0]
            row = starting_row + step[1]
            if not (row in range(1,9) and colnum in range(8)):
                continue
            pos = (COLNAMES[colnum],row)
            if board.is_empty(pos):
                self.available_moves.append(pos)
            elif board.piece_at(pos).colour != self.colour:
                self.available_moves.append(pos)


    def find_positions_threatened(self):
        self.threatens = self.available_moves




