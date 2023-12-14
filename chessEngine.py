"""
This class is responsible for storing all the information about the current state of the chess game.
This will also be responsible for determining the valid moves at the current state, while also keeping a move log,
allowing for undo, redo etc.
"""

class GameState():
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
            ["--", "--", "--", "bP", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True;
        self.moveLog = []
        
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Add the move made to the move log so it can be manipulated later on
        self.whiteToMove = not self.whiteToMove # Swap the playing team, ie switch between black and white
        
    '''
    Undo the last move performed
    '''
    def undo(self):
        if len(self.moveLog) != 0: # Make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # Switch the turns back
            
    '''
    Generate all moves considering given checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()
    
    '''
    Generate all moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        # Nested for loop to traverse every element in the 2D list
        for row in range(len(self.board)): # Number of rows on the board
            for column in range(len(self.board[row])): # Number of columns in the given row 
                turn = self.board[row][column][0] # As the first character of a piece denotes the color thats currently playing
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][column][1]
                    if piece == 'P':
                        # print("Debug statement")
                        self.getPawnMoves(row, column, moves)
                    elif piece == 'R':
                        self.getRookMoves(row, column, moves)
        return moves
                        
    '''
    Get all the possible Pawn moves located at the given row and column and add them to the moves list
    '''
    # White pawns are on row 6 and black pawns are on row 1
    def getPawnMoves(self, row, column, moves):
        if self.whiteToMove: # White pawn will move
            if self.board[row - 1][column] == "--": # If the square infront of the pawn is empty then it's a valid move
                moves.append(Move((row, column), (row - 1, column), self.board))
                if row == 6 and self.board[row - 2][column] == "--": # Check if two squares infront of the given pawn is empty
                    moves.append(Move((row, column), (row - 2, column), self.board))
            if column - 1 >= 0: # To make sure that capturing the piece using a pawn towards the left doesn't move it out of the board
                if self.board[row - 1][column - 1][0] == 'b': # There is an enemy piece to capture
                    moves.append(Move((row, column), (row - 1, column - 1), self.board))
            if column + 1 <= 7: # To make sure that capturing the piece using a pawn towards the right doesn't move it out of the board
                if self.board[row - 1][column + 1][0] == 'b': # There is an enemy piece to capture
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))
    
    '''
    Get all the possible Rook moves located at the given row and column and add them to the moves list
    '''
    def getRookMoves(self, row, column, moves):
        pass
        
         
class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v : k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v : k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol # Generate a unique move ID for every move
        print(self.moveID)
        
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
        
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    def getRankFile(self, row, column):
        return self.colsToFiles[column] + self.rowsToRanks[row]