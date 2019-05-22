"""
Utility functions for an ascii representation of a chess board.
"""


empty_board = """
    A   B   C   D   E   F   G   H
  |---|---|---|---|---|---|---|---|
8 |   |   |   |   |   |   |   |   |
  |---|---|---|---|---|---|---|---|
7 |   |   |   |   |   |   |   |   |
  |---|---|---|---|---|---|---|---|
6 |   |   |   |   |   |   |   |   |
  |---|---|---|---|---|---|---|---|
5 |   |   |   |   |   |   |   |   |
  |---|---|---|---|---|---|---|---|
4 |   |   |   |   |   |   |   |   |
  |---|---|---|---|---|---|---|---|
3 |   |   |   |   |   |   |   |   |
  |---|---|---|---|---|---|---|---|
2 |   |   |   |   |   |   |   |   |
  |---|---|---|---|---|---|---|---|
1 |   |   |   |   |   |   |   |   |
  |---|---|---|---|---|---|---|---|
"""

def find_index(col,row):
    rows = empty_board.split("\n")
    row_number = 3+(8-int(row))*2
    col_number = 'ABCDEFGH'.index(col)
    col_number = 3 + 4*col_number
    index = 0
    for row in rows[:row_number]:
        index += len(row)+1
    index += col_number
    return index

def update_board(board, index, piece_str):
    """
    Replace an empty square on the board string with a one-letter
    string representing colour and type of a piece.
    """
    new_string = board[:index]
    new_string += piece_str
    new_string += board[index+1:]
    return new_string


def print_board(list_of_pieces):
    """
    Loop through a list of pieces, get their positions and
    the two-letter colour-and-type, and update the board with
    each one.
    """
    board = empty_board
    for piece in list_of_pieces:
        position = find_index(piece.current_position[0],
                              piece.current_position[1])
        board = update_board(board, position, str(piece))
    return board
