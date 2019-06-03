"""
Different methods for the AI to choose the next move.
"""
import random
import operator

COLOURS = ["WHITE","BLACK"]

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
                    print("Can piece at {} move to {}?".format(p.current_position, m))
                    if game.is_legal_move(self.colour, p.current_position, m):
                        all_possible_moves.append((p.current_position,m))
        print("Number of possible moves is {}".format(len(all_possible_moves)))
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
        print("Trying move {} to {}".format(start,end))
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
    def __init__(self, colour):
        self.colour = colour


    def get_points_for_position(self, game, colour):
        """"
        points for pieces, and heuristics for position
        """
        points = 0.
        centre_squares = {
            "WHITE": [("D",5),("E",5)],
            "BLACK": [("D",4),("E",4)]
        }
        for p in game.board.pieces:
            sign = 1 if p.colour == colour else -1
            points += sign * p.value
            points += sign * 0.01 * len(p.available_moves)
            if p.piece_type == "King" and p.has_castled:
                points += sign * 0.2
            for cs in centre_squares[self.colour]:
                if cs in p.threatens:
                    points += sign * 0.1
        return points

    def explore_tree(self, game, current_depth, max_depth, history_str, points_dict):
        """
        function to be called recursively.
        """
        game.board.save_snapshot(history_str)
        col_to_move = game.next_to_play
        min_points = 999.
        min_points_move = ""
        for p in game.board.pieces:
   #         print("{} {}".format(current_depth, p.current_position))
            game.board.load_snapshot(history_str)
            start_pos = p.current_position
            for m in p.available_moves:
                if game.is_legal_move(col_to_move, start_pos, m):
  #                  print(" MOVING {}{}".format(start_pos, m))
                    game.move(start_pos, m)
                    move_str = "{}{}{}{}{}".format(
                        history_str,
                        start_pos[0],
                        start_pos[1],
                        m[0],
                        m[1]
                    )
                    points = self.get_points_for_position(game, self.colour)
 #                   print(" COLS {} {}".format(col_to_move, self.colour))
                    if col_to_move == self.colour:
                        points_dict[move_str] = points
                        if current_depth < max_depth :
                            self.explore_tree(game, current_depth+1, max_depth, 
                                              move_str, points_dict)
                    else:
                        if points < min_points:
                            min_points = points
                            min_points_move = (start_pos, m)
                            min_points_move_str = move_str
                    game.next_to_play = col_to_move
        if current_depth % 2 == 1: ## take minimum
#            print(" COLS2 {} {}".format(col_to_move, self.colour))
            game.board.load_snapshot(history_str)
            game.move(min_points_move[0],min_points_move[1])
            if current_depth < max_depth :
                self.explore_tree(game, current_depth+1, max_depth, 
                                  min_points_move_str, points_dict)
            game.next_to_play = col_to_move

        return points_dict


    def minimax(self, game, depth=2):
        """
        work out the best sequence of the next *depth* moves.
        """
        game.board.save_snapshot("")
        points_dict = self.explore_tree(game, 0, depth, "", {})
        points_sorted = sorted(points_dict.items(), key=operator.itemgetter(1))
        return points_sorted[0][0]


    def choose_move(self, game):
        """
        Return start and end position based on minimax
        """
        move_str = self.minimax(game)
        start = (move_str[0],move_str[1])
        end = (move_str[2], move_str[3])
        return start, end

methods = {"Random": RandomMovePlayer,
           "BestNextPoints" : BestNextPointsPlayer,
           "Minimax": MinimaxPlayer
           }
