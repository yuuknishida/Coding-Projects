from Config import *

class GUIRenderer:
    """
    This class is used to handle all GUI rendering
    """
    def __init__(self, canvas, board):
        self.canvas = canvas
        self.board = board
        self.drawBoard()
        self.drawPieces()

    def drawBoard(self):
        self.canvas.delete("all")
        colors = ["white", "gray"]

        for i in range(BOARD_SIZE):
            # Draw rank numbers (1-8)
            self.canvas.create_text(5, i * SQUARE_SIZE + SQUARE_SIZE/2, text=str(8-i), anchor="w")
            # Draw file letters(a-h)
            self.canvas.create_text(i * SQUARE_SIZE + SQUARE_SIZE/2, BOARD_SIZE * SQUARE_SIZE - 5, text=chr(97 + i), anchor="s")
            for j in range(BOARD_SIZE):
                color = colors[(i + j) % 2]
                square = self.canvas.create_rectangle(j * SQUARE_SIZE, i * SQUARE_SIZE, (j + 1) * SQUARE_SIZE, (i + 1) * SQUARE_SIZE, fill=color)
    def drawPieces(self):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                piece = self.board.board[x][y]
                if piece:
                    piece.draw()
    def highlightSquare(self, position, color="yellow"):
        x1 = position.x * SQUARE_SIZE
        y1 = position.y * SQUARE_SIZE
        x2 = (position.x + 1) * SQUARE_SIZE
        y2 = (position.y + 1) * SQUARE_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, stipple="gray50", tags="highlight")
    def highlightLastMove(self):
        if self.board.lastMove:
            start, end = self.board.lastMove
            for pos in [start, end]:
                self.highlightSquare(pos, "light green")
    def clearHighlights(self):
        self.canvas.delete("highlight")
        self.selectedPiece = None
        self.moveTo = None
    def update(self):
        self.drawBoard()
        self.drawPieces()
        self.highlightLastMove()
