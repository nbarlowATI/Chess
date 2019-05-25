"""
Different methods for the AI to choose the next move.
"""
import random


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
                    if game.is_legal_move(self.colour, m[0], m[1]):
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
        return start, end


class MinimaxPlayer(object):
    """
    Use minimax algorithm to choose moves.
    """
    def __init__(self, colour):
        self.colour = colour



methods = {"Random": RandomMovePlayer,
           "BestNextPoints" : BestNextPointsPlayer,
           "Minimax": MinimaxPlayer
           }
