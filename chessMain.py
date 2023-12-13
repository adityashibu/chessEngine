"""
This is the main Driver file. It will be responsible for handling user inputs and displaying the current GameState object
"""

import pygame as py
from chessEngine import GameState

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
        IMAGES[piece] = py.transform.scale(py.image.load("images/" + piece + ".png")), (SQ_SIZE, SQ_SIZE)
    # Note: We can access the images loaded in the dictionary by calling 'IMAGES["wP"]'
    
'''
This is the main driver for the code. This will handle the user input and update the graphics accordingly
'''
def main():
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    screen.fill(py.Color("white"))
    gs = GameState()
    print(gs.board)
    
main()