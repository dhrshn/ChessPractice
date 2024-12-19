import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import chessengine as ChessEngine

BOARD_WIDTH = BOARD_HEIGHT = 512
DIMENSION = 9
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
IMAGES = {}

def loadImages():
    """
    Initialize a global dictionary of images.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        img = Image.open(f"/home/dhrshn/Documents/GitHub/ChessPractice/index/images/{piece}.png")
        img = img.resize((SQUARE_SIZE, SQUARE_SIZE), Image.Resampling.LANCZOS)

        IMAGES[piece] = ImageTk.PhotoImage(img)

def drawBoard(canvas):
    """
    Draw the chessboard on the canvas.
    """
    colors = ["#f0d9b5", "#b58863"]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            canvas.create_rectangle(
                col * SQUARE_SIZE, row * SQUARE_SIZE,
                (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                fill=color
            )

def drawPieces(canvas, board):
    """
    Draw the chess pieces on the board.
    """
    canvas.delete("pieces")  # Remove previous pieces
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                canvas.create_image(
                    col * SQUARE_SIZE, row * SQUARE_SIZE,
                    image=IMAGES[piece],
                    anchor="nw",
                    tags="pieces"
                )

def onSquareClick(event, canvas, game_state, valid_moves, state):
    """
    Handle clicks on the chessboard.
    """
    col = event.x // SQUARE_SIZE
    row = event.y // SQUARE_SIZE
    square = (row, col)

    if state["selected"] == square:  # Deselect if clicked twice
        state["selected"] = ()
        state["clicks"] = []
    else:
        state["selected"] = square
        state["clicks"].append(square)

    if len(state["clicks"]) == 2:  # Process move
        move = ChessEngine.Move(state["clicks"][0], state["clicks"][1], game_state.board)
        if move in valid_moves:
            game_state.makeMove(move)
            state["selected"] = ()
            state["clicks"] = []
            valid_moves[:] = game_state.getValidMoves()
        else:
            state["clicks"] = [square]

    drawBoard(canvas)
    highlightSquares(canvas, game_state, valid_moves, state["selected"])
    drawPieces(canvas, game_state.board)

def highlightSquares(canvas, game_state, valid_moves, selected_square):
    """
    Highlight selected squares and valid moves.
    """
    if selected_square:
        row, col = selected_square
        if game_state.board[row][col][0] == ('w' if game_state.white_to_move else 'b'):
            # Highlight selected square
            canvas.create_rectangle(
                col * SQUARE_SIZE, row * SQUARE_SIZE,
                (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                outline="blue", width=2
            )
            # Highlight valid moves
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    canvas.create_rectangle(
                        move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE,
                        (move.end_col + 1) * SQUARE_SIZE, (move.end_row + 1) * SQUARE_SIZE,
                        outline="yellow", width=2
                    )

def main():
    root = tk.Tk()
    root.title("Tkinter Chess")
    
    # Initialize game state
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    state = {"selected": (), "clicks": []}

    # Create canvas
    canvas = tk.Canvas(root, width=BOARD_WIDTH, height=BOARD_HEIGHT)
    canvas.pack()

    loadImages()
    drawBoard(canvas)
    drawPieces(canvas, game_state.board)

    canvas.bind("<Button-1>", lambda event: onSquareClick(event, canvas, game_state, valid_moves, state))

    root.mainloop()

if __name__ == "__main__":
    main()
