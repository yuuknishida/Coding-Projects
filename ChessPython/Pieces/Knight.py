from typing import override
from Pieces.Piece import Piece
from Position import Position
import tkinter as tk
from PIL import Image, ImageTk
from Config import *

class Knight(Piece):
    def __init__(self, color, position, canvas, image):        
        self.kind = KNIGHT
        super().__init__(color, position, canvas, image)
        
    @override
    def get_raw_moves(self, board):
        moves = []
        directions = [(2, 1), (2, -1), (-2, -1), (-2, 1),
                      (1, -2), (-1, -2), (1, 2), (-1, 2)]

        for dx, dy in directions:
            x = self.position.x + dx
            y = self.position.y + dy
            
            if not board.isPositionValid(Position(x, y )):    # if position is outside of board break
                # print("No in bounds")
                continue
            target_piece = board.getPieceAtPosition(Position(x,y))
            if target_piece is None or target_piece.color != self.color:
                moves.append(Position(x, y))
        
        # for move in moves:
        #     print(f"Knight Moves: ({move.x}, {move.y})")
        # print("Number of moves: ", len(moves))

        return moves
    