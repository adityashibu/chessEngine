"""
This class is responsible for storing all the information about the current state of the chess game.
This will also be responsible for determining the valid moves at the current state, while also keeping a move log,
allowing for undo, redo etc.
"""

class GameState:
    def __init__(self):
        # The board is a standard 8x8 2 diamensional array, Each element of the list has 2 characters,
        # The first letter represents the color of the piece, and the second character represents the type of piece
        # "--" represents an empty space, ie there are no pieces there
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True;
        self.moveLog = []