from Pieces.Rook import Rook
from Pieces.Pawn import Pawn
from Position import Position
from Config import *
from PromotionPanel import PromotionDialog

class SpecialMoveHandler:
    """
    SpecialMoveHandler is a class that handles special moves
    
    Attributes:
    Methods:
    """
    def __init__(self, board, moveValidator):
        self.board = board
        self.moveValidator = moveValidator
    def handleCastling(self, fromPos, toPos):
        """Handle castling for the king"""
        if abs(toPos.x - fromPos.x) == 2:  # if king is traveling two squares in any direction 
            is_kingside = toPos.x > fromPos.x
            rook_start_x = 7 if is_kingside else 0
            rook_end_x = 5 if is_kingside else 3

            rook = self.board.board[rook_start_x][fromPos.y] # get the rook
            if rook and isinstance(rook, Rook): # check if it's a rook
                self.board.movePiece(
                    Position(rook_start_x, fromPos.y),
                    Position(rook_end_x, fromPos.y)
                )
    def handleEnPassant(self, pawn, fromPos, toPos):
        """
        Handle en passant capture (En Passant move handled in Pawn class)
        Returns True if en passant capture occurred, Flase otherwise
        """
        if abs(toPos.x - fromPos.x) == 1:
            captured_pawn_pos = Position(toPos.x, fromPos.y)
            captured_pawn = self.board.getPieceAtPosition(captured_pawn_pos)

            # Verify the conditions for en passant:
            # 1. There must be a pawn in the captured  position
            # 2. That pawn must be of opposite color
            # 3. That pawn must have just made a double move
            if(isinstance(captured_pawn, Pawn) and
            captured_pawn.color != pawn.color and
            captured_pawn.just_made_double_move):
            # Remove the captured pawn
                self.board.board[captured_pawn_pos.x][captured_pawn_pos.y] = None
                return True
        return False
    def handlePromotion(self, pawn, toPos):
        if ((pawn.color == WHITE and toPos.y == 0) or 
            (pawn.color == BLACK and toPos.y == 7)):
            def onPieceSelected(pieceName):
                pieceMap = {
                "Queen": (QUEEN, WHITE_QUEEN_IMAGE if pawn.color == WHITE else BLACK_QUEEN_IMAGE),
                "Rook": (ROOK, WHITE_ROOK_IMAGE if pawn.color == WHITE else BLACK_ROOK_IMAGE),
                "Bishop": (BISHOP, WHITE_BISHOP_IMAGE if pawn.color == WHITE else BLACK_BISHOP_IMAGE),
                "Knight": (KNIGHT, WHITE_KNIGHT_IMAGE if pawn.color == WHITE else BLACK_KNIGHT_IMAGE)
            }
                
                # Clear the pawn from the board immediately
                self.board.canvas(pawn.image)
                self.board.board[pawn.position.x][pawn.position.y] = None

                # Create and place the new piece
                pieceType, pieceImage = pieceMap[pieceName]
                newPiece = self.createPiece(pieceType, pawn.color, pawn.position, pieceImage)
                self.board.board[pawn.position.x][pawn.position.y] = newPiece

                # Redraw the entire board to ensure clean visualization
                self.board.drawBoard()
                self.board.drawPieces()

                # Update the display immediately
                self.update_idletasks()

            # Show the promotion dialog
            dialog = PromotionDialog(self, onPieceSelected)
            self.wait_window(dialog)
        return False
    
    def handleCapture(self, fromPos, toPos):
        attackingPiece = self.board.getPieceAtPosition(fromPos)
        targetPiece = self.board.getPieceAtPosition(toPos)
        if targetPiece:
            if targetPiece.color != attackingPiece.color:
                if isinstance(targetPiece, Pawn) and targetPiece.just_made_double_move:
                    targetPiece.just_made_double_move = False
                self.board.board[toPos.x][toPos.y] = None
            else: return None
        return targetPiece