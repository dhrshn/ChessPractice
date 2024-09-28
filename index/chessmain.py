"""
This is our main driver file. It will be responsible for handling user
input and displaying the current GameState Object!!
"""
import pygame as p 
import chessengine


WIDTH = HEIGHT = 512
DIMENSION = 8 # 8X8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 10
IMAGES = {}


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("index/images/"+piece+".png"), (SQ_SIZE, SQ_SIZE))
    # Note: we can access an image by saying 'IMAGES['wp']'
'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = chessengine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #Flag Variaable
    loadImages() #Only do this once, before the while loop
    running = True
    sqSelected = ()# No of squares selected, keep track of the last click of the user (tuple: (row,col))
    playerClicks = []# keep track of players clicks [two tuples: (6,4), (4,4)]
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:# Location of mouse
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col): # the user clicked the same square twice
                    sqSelected = () #deselects the sq
                    playerClicks = [] #clears players clicks
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
                if len(playerClicks) == 2: #after the second click
                    move = chessengine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move) 
                        moveMade = True
                    sqSelected = () # reset the user clicks
                    playerClicks = []
            elif e.type == p.KEYDOWN:#Undo Key
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False 
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
'''
Main driver for our code. This will handle user input and updating the graphics
'''  


def drawGameState(screen,gs):
    drawBoard(screen) #Draw squres on the board
    #Adding in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) #Draw pieces on top of those squares
'''
Responsible for all the graphics within the current game state
'''


def drawBoard(screen):
    colors = [p.Color('light gray'),p.Color('dark gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
'''
Draw the squares on the board. The top left square is always light.
'''


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
'''
Draw pieces on the board using the current GameSate.board
'''
 
if __name__ == "__main__":  
    main()