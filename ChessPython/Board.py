from Config import *
from Position import Position
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Queen import Queen
from Pieces.King import King
from Pieces.Piece import Piece

class Board:
    """
    Handles that chess board state and piece management"""

    def __init__(self, canvas):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.whiteKingLocation = Position(4, 7)
        self.blackKingLocation = Position(4, 0)
        self.canvas = canvas
        self.lastMove = None
        self.initializePieces()

    def initializePieces(self):
        # Setup pieces
        for x in range(BOARD_SIZE):
            self.board[x][0] = self.createPiece(pieces[x], BLACK, Position(x, 0), blackPieceImages[x])
            self.board[x][1] = self.createPiece(PAWN, BLACK, Position(x, 1), BLACK_PAWN_IMAGE)

            self.board[x][6] = self.createPiece(PAWN, WHITE, Position(x, 6), WHITE_PAWN_IMAGE)
            self.board[x][7] = self.createPiece(pieces[x], WHITE, Position(x, 7), whitePieceImages[x])

    def createPiece(self, kind, color, position, image):
        if kind == KING:
            return King(color, position, self.canvas, image)
        elif kind == QUEEN:
            return Queen(color, position, self.canvas, image)
        elif kind == BISHOP:
            return Bishop(color, position, self.canvas, image)
        elif kind == KNIGHT:
            return Knight(color, position, self.canvas, image)
        elif kind == ROOK:
            return Rook(color, position, self.canvas, image)
        elif kind == PAWN:
            return Pawn(color, position, self.canvas, image)
        return Piece(color, position, self.canvas, image)   

    def getPieceAtPosition(self, position):
        if self.isPositionValid(position):
            return self.board[position.x][position.y]
        return None

    def isPositionValid(self, position): 
        return 0 <= position.x < BOARD_SIZE and 0 <= position.y < BOARD_SIZE
    
    def movePiece(self, fromPos, toPos):
        piece = self.board[fromPos.x][fromPos.y]

        # Update board state
        self.board[fromPos.x][fromPos.y] = None
        piece.position = toPos
        self.board[toPos.x][toPos.y] = piece

        # Update piece state
        if (isinstance(piece, Pawn) or isinstance(piece, King) or isinstance(piece, Rook)) and not piece.hasMoved:
            piece.hasMoved = True
        if isinstance(piece, King):
            if piece.color == WHITE:
                self.whiteKingLocation = toPos
            else:
                self.blackKingLocation = toPos
        