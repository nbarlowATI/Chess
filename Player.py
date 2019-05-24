"""
A player - could be AI or human.
"""

from MoveChooser import methods


class Player(object):
    def __init__(self, colour, is_AI):
        self.colour = colour
        self.is_AI = is_AI
        if self.is_AI:
            methods_choice = enumerate(methods.keys())
            possible_methods_str = ""
            methods_index_dict = {}
            for i, meth in methods_choice:
                methods_index_dict[str(i)] = meth
                possible_methods_str += " enter {} for {} \n".format(i,meth)
            method_index = input("Choose method for AI: \n"\
                                 + possible_methods_str)
            self.AI_method = methods[methods_index_dict[method_index]](colour)

    def move(self, game, start_pos, end_pos):
        if game.is_legal_move(self.colour, start_pos, end_pos):
            moved_ok = game.move(start_pos, end_pos)
            print("Moved_OK")
            print(game.board)
            return moved_ok
        else:
            print("Didn't move")
            return False

    def choose_move(self, game):
        """
        If we are an AI player, use the chosen class' choose_move method.
        """
        moved_ok = False
        while not moved_ok:
            start_pos, end_pos =  self.AI_method.choose_move(game)
            self.move(game, start_pos, end_pos)
        return start_pos, end_pos

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
