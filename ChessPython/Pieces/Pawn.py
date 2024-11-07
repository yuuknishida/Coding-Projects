from typing import override
from Position import Position
from Config import *
from Pieces.Piece import Piece
from Pieces.Queen import Queen
import tkinter as tk
from PIL import Image, ImageTk

class Pawn(Piece):
    def __init__(self, color, position, canvas, image):
        self.kind = PAWN 
        super().__init__(color, position, canvas, image)
        self.hasMoved = False
        self.just_made_double_move = False 

    @override
    def get_raw_moves(self, board):
        moves = []
        direction = -1 if self.color == WHITE else 1

        # Forward move
        forward = Position(self.position.x, self.position.y + direction)
        if board.isPositionValid(forward) and board.getPieceAtPosition(forward) is None:   # forward move
            moves.append(forward)
            # print("pawn moved forward")

            # First - can move two squares
            if not self.hasMoved:
                double = Position(self.position.x, self.position.y + (direction * 2))
                if board.isPositionValid(double) and board.getPieceAtPosition(double) is None:     # double move
                    moves.append(double)
                    self.just_made_double_move = True
                    # print("pawn moved double forward")

        # Capture moves        
        for dx in [-1, 1]:
            capture_pos = Position(self.position.x + dx, self.position.y + direction)
            if board.isPositionValid(capture_pos):
                target_piece = board.getPieceAtPosition(capture_pos)
                if target_piece and target_piece.color != self.color:
                    moves.append(capture_pos)

        # En Passant
        if ((self.color == WHITE and self.position.y == 3) or
            (self.color == BLACK and self.position.y == 4)):
            for dx in [-1, 1]:
                adjacent_pos = Position(self.position.x + dx, self.position.y)
                if board.isPositionValid(adjacent_pos):
                    adjacent_piece = board.getPieceAtPosition(adjacent_pos)
                    if(isinstance(adjacent_piece, Pawn) and
                       adjacent_piece.color != self.color and
                       adjacent_piece.just_made_double_move):
                        moves.append(Position(adjacent_pos.x, self.position.y + direction))
        return moves