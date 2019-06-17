"""
Different methods for the AI to choose the next move.
"""
import random
import operator

COLOURS = ["WHITE","BLACK"]

def other_colour(my_colour):
    """
    Get the other colour.
    """
    my_colour_index = COLOURS.index(my_colour)
    other_colour_index = (my_colour_index + 1) % 2
    other_colour = COLOURS[other_colour_index]
    return other_colour

class RandomMovePlayer(object):
    """
    Choose a move randomly
    """
    def __init__(self, colour):
        self.colour = colour
        print("{} will choose moves randomly.".format(colour))

    def choose_move(self, game):
        all_possible_moves = []
        for p in game.board.pieces:
            if p.colour == self.colour:
                for m in p.available_moves:
                    if game.is_legal_move(self.colour, p.current_position, m):
                        all_possible_moves.append((p.current_position,m))
        move_index = random.randint(0,len(all_possible_moves)-1)
        start, end = all_possible_moves[move_index]
        return start, end


class BestNextPointsPlayer(object):
    """
    Evaluate points for takes and losses for next move
    """
    def __init__(self, colour):
        self.colour = colour
        print("{} will choose moves according to simple points total for the next move.".format(colour))

    def choose_move(self, game):
        all_possible_moves = []
        for p in game.board.pieces:
            start_pos = p.current_position
            if p.colour == self.colour:
                for m in p.available_moves:
                    if game.is_legal_move(self.colour, start_pos, m):
                        all_possible_moves.append((start_pos,m))
        best_points = -999
        best_moves = []
        print(game.board)
        for move in all_possible_moves:
            points = self.potential_points_for_move(game, self.colour, move)
            if points > best_points:
                best_points = points
                best_moves = [move]
            elif points == best_points:
                best_moves.append(move)
        ## we now have a list best_moves which contains the one
        ## or more top-scoring possible moves.  Pick one at random.
        start,end = best_moves[random.randint(0,len(best_moves)-1)]
        print(game.board)
        return start, end

    def potential_points_for_move(self, game, colour, move):
        """
        return a points value based on:
          (value of any piece taken at end_pos)
        - (value of this piece if threatened at end_pos)
        + (value of this piece if threatened at start_pos)
        """
        points = 0
        start_pos, end_pos = move
        this_piece_value = game.board.piece_at(start_pos).value
        if not game.board.is_empty(end_pos):
            points += game.board.piece_at(end_pos).value
        for p in game.board.pieces:
            if p.colour == colour:
                continue
            if start_pos in p.threatens:
                points += this_piece_value
            if end_pos in p.threatens:
                points -= this_piece_value
        return points


class MinimaxPlayer(object):
    """
    Use minimax algorithm to choose moves.
    """
    def __init__(self, colour, depth=3):
        self.colour = colour
        self.depth = depth
        print("{} will use minimax algorithm to choose moves.".format(colour))

    def get_points_for_position(self, game):
        """"
        points for pieces, and heuristics for position
        """
        points = 0.
        next_to_play = game.next_to_play
        centre_squares = {
            "WHITE": [("D",5),("E",5)],
            "BLACK": [("D",4),("E",4)]
        }
        if game.is_checkmate(next_to_play):
            points = 1000. if self.colour == next_to_play else -1000.
            return points
        for p in game.board.pieces:
            sign = 1 if p.colour == self.colour else -1
            points += sign * p.value
            points += sign * 0.005 * len(p.available_moves)
            if p.piece_type == "King" and p.has_castled:
                points += sign * 0.2
            for cs in centre_squares[self.colour]:
                if cs in p.threatens:
                    points += sign * 0.1
        return points


    def minimax(self, game, depth, maximizingPlayer, move_str):
        game.board.save_snapshot(move_str)
        if depth == 0:
            return self.get_points_for_position(game), move_str
        next_depth = depth - 1
        best_move_str = None
        if maximizingPlayer:
            game.next_to_play = self.colour
            best_value = -999.
            for move in game.get_all_possible_moves(self.colour):
                game.board.load_snapshot(move_str)
                game.move(move[0],move[1])
                new_move_str = "{}{}{}{}{}".format(move_str,
                                                   move[0][0],
                                                   move[0][1],
                                                   move[1][0],
                                                   move[1][1])

                value = self.minimax(game, next_depth, False, new_move_str)[0]
                if value > best_value:
                    best_value = value
                    best_move_str = new_move_str
            return best_value, best_move_str
        else:
            game.next_to_play = other_colour(self.colour)
            best_value = 999.
            for move in game.get_all_possible_moves(other_colour(self.colour)):
                game.board.load_snapshot(move_str)
                game.move(move[0], move[1])
                new_move_str = "{}{}{}{}{}".format(move_str,
                                                   move[0][0],
                                                   move[0][1],
                                                   move[1][0],
                                                   move[1][1])
                value = self.minimax(game, next_depth, True, new_move_str)[0]
                if value < best_value:
                    best_value = value
                    best_move_str = new_move_str
        return best_value, best_move_str


    def alphabeta(self, game, depth, alpha, beta, maximizingPlayer, move_str):
        game.board.save_snapshot(move_str)
        if depth == 0:
            return self.get_points_for_position(game), move_str
        next_depth = depth - 1
        best_move_str = None
        if maximizingPlayer:
            game.next_to_play = self.colour
            best_value = -9999.
            for move in game.get_all_possible_moves(self.colour):
                game.board.load_snapshot(move_str)
                game.move(move[0],move[1])
                new_move_str = "{}{}{}{}{}".format(move_str,
                                                   move[0][0],
                                                   move[0][1],
                                                   move[1][0],
                                                   move[1][1])

                value = self.alphabeta(game, next_depth, alpha, beta, False, new_move_str)[0]
                if value > best_value:
                    best_value = value
                    best_move_str = new_move_str
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break
            return best_value, best_move_str
        else:
            game.next_to_play = other_colour(self.colour)
            best_value = 9999.
            for move in game.get_all_possible_moves(other_colour(self.colour)):
                game.board.load_snapshot(move_str)
                game.move(move[0], move[1])
                new_move_str = "{}{}{}{}{}".format(move_str,
                                                   move[0][0],
                                                   move[0][1],
                                                   move[1][0],
                                                   move[1][1])
                value = self.alphabeta(game, next_depth, alpha, beta, True, new_move_str)[0]
                if value < best_value:
                    best_value = value
                    best_move_str = new_move_str
                beta = min(beta, best_value)
                if beta < alpha:
                    break
        return best_value, best_move_str


    def choose_move(self, game):
        """
        Return start and end position based on minimax
        """
        game_history = game.get_history_str()
        game.save_snapshot()
        move_str = self.alphabeta(game, self.depth, -9999., 9999.,True, game_history)[1]
        game.load_snapshot(game_history)
        start = (move_str[-4],int(move_str[-3]))
        end = (move_str[-2], int(move_str[-1]))
        return start, end


methods = {"Random": RandomMovePlayer,
           "BestNextPoints" : BestNextPointsPlayer,
           "Minimax": MinimaxPlayer
           }
