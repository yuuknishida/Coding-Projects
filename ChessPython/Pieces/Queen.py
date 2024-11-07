from typing import override
from Pieces.Piece import Piece
import tkinter as tk
from PIL import Image, ImageTk
from Config import *
from Position import Position
class Queen(Piece):
    def __init__(self, color, position, canvas, image):
        self.kind = QUEEN
        super().__init__(color, position, canvas, image)
    
    @override
    def get_raw_moves(self, board):
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            x = self.position.x
            y = self.position.y
            while True:
                x += dx
                y += dy
                if not board.isPositionValid(Position(x, y)):
                    break

                target_piece = board.getPieceAtPosition(Position(x, y))
                if target_piece is None:
                    moves.append(Position(x, y))
                elif target_piece.color != self.color:
                    moves.append(Position(x, y))
                    break
                else:
                    break
        # for move in moves:
        #     print(f"Queen Moves: ({move.x}, {move.y})")
        # print("Number of moves: ", len(moves))
        
        return moves