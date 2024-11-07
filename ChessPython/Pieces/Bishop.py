from typing import override
from Pieces.Piece import Piece
import tkinter as tk
from PIL import Image, ImageTk
from Config import *
from Position import Position

class Bishop(Piece):
    def __init__(self, color, position, canvas, image):
        self.kind = BISHOP
        super().__init__(color, position, canvas, image)
        

    @override
    def get_raw_moves(self, board):
        moves = []
        directions = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            x = self.position.x
            y = self.position.y
            while True:
                x += dx
                y += dy
                if not board.isPositionValid(Position(x, y)):
                    break
                if board.getPieceAtPosition(Position(x, y)) is None:
                    moves.append(Position(x, y))
                elif board.getPieceAtPosition(Position(x, y)).color != self.color:
                    moves.append(Position(x, y))
                    break
                else:
                    break
        # for move in moves:
        #     print(f"Bishop Moves: ({move.x}, {move.y})")
        # print("Number of moves: ", len(moves))

        return moves
    