from Board import Board
from MoveValidator import MoveValidator
from SpecialMoveHandler import SpecialMoveHandler
from GameState import GameState
from GUIRenderer import GUIRenderer
import tkinter as tk
from Config import *
from Position import Position
from Pieces.King import King
from Pieces.Pawn import Pawn
class ChessController:
    """
    Main controller that coordinates all components
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x800")
        self.root.title("Chess")

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.board = Board(self.canvas)
        self.renderer = GUIRenderer(self.canvas, self.board)
        self.gameState = GameState(self.board)
        self.moveValidator = MoveValidator(self.board, self.gameState)
        self.specialMovesHandler = SpecialMoveHandler(self.board, self.moveValidator)
        
        self.selectedPiece = None
        self.moveTo = None

        self.canvas.bind("<Button-1>", self.whenPlayerClicksSquare)
    def whenPlayerClicksSquare(self, event):
        if self.gameState.game_over:
            return
        
        x = event.x // SQUARE_SIZE
        y = event.y // SQUARE_SIZE
        clickedPos = Position(x,y)
        clickedPiece = self.board.getPieceAtPosition(clickedPos)

        # First click - Select a piece
        if self.selectedPiece is None:
            if clickedPiece is not None and clickedPiece.color == (WHITE if self.gameState.whiteToMove else BLACK):
                self.selectedPiece = clickedPiece
                self.showPossibleMoves()
                return
                
        # Second click - Try to move the selected piece
        if self.selectedPiece:
            # clicking the same piece again - deselect
            if clickedPiece and clickedPiece == self.selectedPiece:
                self.selectedPiece = None
                self.renderer.clearHighlights()
                print("piece deselected")
                return
            if clickedPiece is not None:
                if clickedPiece.color == (WHITE if self.gameState.whiteToMove else BLACK):
                    self.renderer.clearHighlights()
                    self.selectedPiece = clickedPiece
                    self.showPossibleMoves()
                    return
            if self.executeMove(clickedPos):
                self.renderer.clearHighlights()
                self.selectedPiece = None
                self.moveTo = None
                self.moveValidator.isItMate(self.gameState.whiteToMove)
                return
    def executeMove(self, toPos):
        piece = self.selectedPiece
        self.moveTo = toPos
        if not piece or not self.moveValidator.isValidMove(piece, piece.position, toPos):
            return False
        
        # Store original position for move highlighting
        fromPos = Position(piece.position.x, piece.position.y)

        # Handle special moves
        specialMove = None
        capturedPiece = self.specialMovesHandler.handleCapture(fromPos, toPos)

        # Execute the move
        self.board.movePiece(fromPos, toPos)

        if isinstance(piece, Pawn):
            if self.specialMovesHandler.handleEnPassant(piece, fromPos, toPos):
                specialMove = "En Passant"
            elif self.specialMovesHandler.handlePromotion(piece, toPos):
                specialMove = "Promotion"

        elif isinstance(piece, King):
            if abs(toPos.x - fromPos.x) == 2:
                self.specialMovesHandler.handleCastling(fromPos, toPos)
                specialMove = "Castling"

        # Record the move
        self.gameState.recordMove(piece, fromPos, toPos, capturedPiece, specialMove)
        self.board.lastMove = (fromPos, toPos)

        # Update pawn flags
        # Reset all pawns' just_made_double_move flags
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if isinstance(self.board.board[x][y], Pawn):
                    self.board.board[x][y].just_made_double_move = False

        # Set the just_made_double_move flag for the moved pawn
        if isinstance(piece, Pawn) and abs(fromPos.y - toPos.y) == 2:
            piece.just_made_double_move = True

        if self.moveValidator.isGameDraw():
            print("The game is a draw!")
            self.gameState.game_over = True
        elif self.moveValidator.isKingInCheck(self.selectedPiece.color):
            self.gameState.inCheck = True
            if self.moveValidator.isItMate():
                print(f"Checkmate! {'Black' if self.gameState.whiteToMove else 'White'} wins!")
        else:
            pass

        self.update()    
        return True
    def showPossibleMoves(self):
        """Show valid moves for the selected piece when king is in check."""
        if not self.selectedPiece:
            print("No piece selected")
            return
        
        valid_moves = []
        original_pos = self.selectedPiece.position

        # Get all possible moves for the selected piece
        potential_moves = self.selectedPiece.get_raw_moves(self.board)

        # Test each move to see if it gets us out of check
        for move in potential_moves:
            captured_piece = self.board.board[move.x][move.y]
            self.board.board[move.x][move.y] = self.selectedPiece
            self.board.board[original_pos.x][original_pos.y] = None

            # Update king position if moving king
            original_king_pos = None
            if isinstance(self.selectedPiece, King):
                original_king_pos = self.board.whiteKingLocation if self.gameState.whiteToMove else self.board.blackKingLocation
                if self.gameState.whiteToMove:
                    self.board.whiteKingLocation = move
                else:
                    self.board.blackKingLocation = move
            
            # Check if this move gets us out of check
            if not self.moveValidator.isKingInCheck(self.selectedPiece.color):
                valid_moves.append(move)

                # Highlight valid move
                x1 = move.x * SQUARE_SIZE
                y1 = move.y * SQUARE_SIZE
                x2 = (move.x + 1) * SQUARE_SIZE
                y2 = (move.y + 1) * SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="light blue", stipple="gray50", tags="highlight")
            else:
                print("Move is not valid due to check")
            
            # Restore the board state
            self.board.board[original_pos.x][original_pos.y] = self.selectedPiece
            self.board.board[move.x][move.y] = captured_piece

            # Restore king position if we moved it
            if isinstance(self.selectedPiece, King) and original_king_pos:
                if self.gameState.whiteToMove:
                    self.board.whiteKingLocation = original_king_pos
                else:
                    self.board.blackKingLocation = original_king_pos

        return valid_moves
    def update(self):
        self.renderer.update()
        self.gameState.switchTurn()
if __name__ == "__main__":
    game = ChessController()
    game.root.mainloop()