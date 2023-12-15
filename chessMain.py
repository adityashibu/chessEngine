"""
This is the main Driver file. It will be responsible for handling user inputs and displaying the current GameState object
"""

import pygame as py
from chessEngine import GameState, Move

py.init() # Initialize pygame
WIDTH = HEIGHT = 512 # Define the window size for the pygame engine, 400 also looks good
DIMENSION = 8 # Define the dimensions of the chessboard (8 x 8)
SQ_SIZE = HEIGHT // DIMENSION # Define the variable to store the size of a single square in the chessboard
MAX_FPS = 15 # Set fps for animations
IMAGES = {} # Define the dictionary for storing the images of the pieces

'''
Initialize a global dictionary of images, This will be called exactly once to prevent any lags from processing images everytime,
This will be called in the main
'''
def loadImages():
    pieces = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
    for piece in pieces:
        # Transform.scale is used to scale the image such that it's height and width are in accordance with 
        # the square size
        IMAGES[piece] = py.transform.scale(py.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: We can access the images loaded in the dictionary by calling 'IMAGES["wP"]'
    
'''
This is the main driver for the code. This will handle the user input and update the graphics accordingly
'''
def main():
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    screen.fill(py.Color("white"))
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # Flag for indicating if the user has made a move
    
    
    loadImages() # Only run once before the while loop
    running = True
    sqSelected = () # Tuple to keep track of the square that has been selected/ ie the last click of the user, and is going to be a tuple of (row, column)
    playerClicks = [] # Keep track of the positions that the play wants to move from and to, basically 2 tuples, ie [(before), (after)], each tuple being a sqSelected
    
    
    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            # Mouse click handlers
            elif e.type == py.MOUSEBUTTONDOWN:
                location = py.mouse.get_pos() # Get the (x, y) coordinates of the mouse pointer
                column = location[0] // SQ_SIZE 
                row = location[1] // SQ_SIZE
                
                if sqSelected == (row, column): # Check if the user clicked on the same square twice
                    sqSelected = ()
                    playerClicks = [] # Clear the playerClicks
                else:
                    sqSelected = (row, column)
                    playerClicks.append(sqSelected) # Append the positions for both the first and the second click
                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () # Reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
                    
            # Key handlers
            elif e.type == py.KEYDOWN:
                if e.key == py.K_z: # Undo when the Z key is pressed
                    gs.undo()
                    moveMade = True # So that when the player undo's a move, it generates the possible moves after undoing the move
                    
        # If a valid move was made then generate all the possible moves for the new gameState
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        py.display.flip()
        
'''
Responsible for rendering all the graphics at the current given gameState
'''
def drawGameState(screen, gs):
    drawBoard(screen) # Draw the squares on the board
    drawPieces(screen, gs.board) # Draw pieces on top of those squares
    
'''
Draw the squares on the given board
'''
def drawBoard(screen):
    colors = [py.Color("white"), py.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            py.draw.rect(screen, color, py.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
'''
Draw the pieces on the board
'''
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--": # This is to check if there is a piece at the given location 
                screen.blit(IMAGES[piece], py.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    
if __name__ == "__main__":
    main()