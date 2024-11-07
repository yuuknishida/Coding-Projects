from typing import override
from Config import *
from Pieces.Piece import Piece
from Pieces.Rook import Rook
import tkinter as tk
from PIL import Image, ImageTk
from Position import Position

class King(Piece):
    def __init__(self, color, position, canvas, image):
        self.kind = KING
        super().__init__(color, position, canvas, image)
        self.hasMoved = False

    @override
    def get_raw_moves(self, board):
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            x = self.position.x + dx 
            y = self.position.y + dy
            
            if not board.isPositionValid(Position(x, y)):
                continue

            target_piece = board.getPieceAtPosition(Position(x, y))
            if target_piece is None or target_piece.color != self.color:
                moves.append(Position(x, y))
        
        # Castling
        if not self.hasMoved:
            # Check for kingside castling
            if self.can_castle_king_side(board):
                moves.append(Position(self.position.x + 2, self.position.y))    # Kingside castling

            # Check for queenside castling
            if self.can_castle_queen_side(board):
                moves.append(Position(self.position.x - 2, self.position.y))    # Queenside castling

        # for move in moves:
        #     print(f"King Moves: ({move.x}, {move.y})")
        # print("Number of moves: ", len(moves))

        return moves

    def can_castle_king_side(self, board):
        if self.hasMoved:
            return False
        # Check if the rook has moved
        rook_position = Position(7, self.position.y)    # Rook is 3 squares away
        rook = board.getPieceAtPosition(rook_position)

        if rook is None or not isinstance(rook, Rook) or rook.hasMoved:
            return False
        
        # Check squares between king and rook
        for x in range(self.position.x + 1, 7):
            if board.getPieceAtPosition(Position(x, self.position.y)) is not None:
                return False
            
        return True

    def can_castle_queen_side(self, board):
        if self.hasMoved:
            return False
        # Check if the rook has moved
        rook_position = Position(0, self.position.y)    # Rook is 4 squares away
        rook = board.getPieceAtPosition(rook_position)
        if rook is None or not isinstance(rook, Rook) or rook.hasMoved:
            return False
        
        # Check squares between king and rook
        for x in range(1, self.position.x):
            if board.getPieceAtPosition(Position(x, self.position.y)) is not None:
                return False
        
        return True
        
    