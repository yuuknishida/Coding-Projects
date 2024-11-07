from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Queen import Queen
from Pieces.King import King
from Pieces.Piece import Piece
from Config import *
from Position import Position
from GameState import GameState
class MoveValidator:
    """
    Handles move validation and chess rules
    """
    def __init__(self, board, game_state):
        self.board = board
        self.game_state = game_state

    def isKingInCheck(self, color):
        """Check if the current player's king is in check."""
        king = self.board.whiteKingLocation if color == WHITE else self.board.blackKingLocation
        enemy_color = BLACK if color == WHITE else WHITE
        print(f"king position: {king.x}, {king.y}")
        print(f"enemy color: {enemy_color}")

        # Check for any pawns that's checking the king
        pawns_move = ([-1, -1], [1, -1]) if color == WHITE else ([1, 1], [-1, 1])
        for dx, dy in pawns_move:
            check_pos = Position(king.x + dx, king.y + dy)
            if self.board.isPositionValid(check_pos):
                piece = self.board.getPieceAtPosition(check_pos)
                if piece and isinstance(piece, Pawn) and piece.color == enemy_color:
                    print(f"check_pos: {check_pos.x}, {check_pos.y}")
                    return True

        # Check for any knights that's checking the king
        knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for dx, dy in knight_moves:
            check_pos = Position(king.x + dx, king.y + dy)
            if self.board.isPositionValid(check_pos):
                piece = self.board.getPieceAtPosition(check_pos)
                if piece and isinstance(piece, Knight) and piece.color == enemy_color:
                    print("check_pos: ", check_pos.x, check_pos.y)
                    return True
                
        # Check for any sliding pieces (rooks, bishops, queens)
        sliding_directions = {
            Rook: [(1, 0), (0, 1), (-1, 0), (0, -1)],
            Bishop: [(1, 1), (1, -1), (-1, 1), (-1, -1)],
            Queen: [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        }
        # check for any sliding pieces that's checking the king
        for piece_type, directions in sliding_directions.items():  
            for dx, dy in directions:
                x, y = king.x, king.y
                while self.board.isPositionValid(Position(x, y)):
                    x += dx
                    y += dy
                    piece = self.board.getPieceAtPosition(Position(x, y))
                    if piece:
                        if isinstance(piece, piece_type) and piece.color == enemy_color:
                            print(f"check_pos: {x}, {y}")
                            return True
                        break
        print(f"King at {king} is not in check")
        return False   
    def isValidMove(self, piece, fromPos, toPos):
        """Validate move considering check and other chess rules"""
        if not self.board.isPositionValid(toPos):
            print(f"Target position ({toPos.x}, {toPos.y}) is not valid.")
            return False
        # Verify it's the correct player's turn
        # if (piece.color == WHITE) != self.whiteToMove:
        #     print(f"It's not {piece.color} turn.")
        #     return False
        
        # Check if target square has a piece of same color
        target_piece = self.board.board[toPos.x][toPos.y]
        if target_piece and target_piece.color == piece.color:
            print(f"Target square ({toPos.x}, {toPos.y}) is occupied by {piece.color}.")
            return False
        
        # Get raw moves and check if target is in them
        raw_moves = piece.get_raw_moves(self.board)
        if not any(move.x == toPos.x and move.y == toPos.y for move in raw_moves):
            print(f"Target position ({toPos.x}, {toPos.y}) is not in the piece's raw moves.")
            return False
        
        # Temporarily make the move
        # original_pos = piece.position
        # original_king_pos = None

        # If moving the king, store the original king position
        # if isinstance(piece, King):
        #     original_king_pos = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
        #     if self.whiteToMove:
        #         self.whiteKingLocation = toPos
        #     else:
        #         self.blackKingLocation = toPos

        # make temporary move
        # self.board[original_pos.x][original_pos.y] = None
        # self.board[toPos.x][toPos.y] = piece
        # piece.position = toPos
        capturedPiece = self.board.getPieceAtPosition(toPos)
        self.board.movePiece(fromPos, toPos)

        # Check if the king is still in check after the move
        in_check = self.isKingInCheck(piece.color)

        # Restore the original state
        # piece.position = original_pos
        # self.board[original_pos.x][original_pos.y] = piece
        # self.board[toPos.x][toPos.y] = target_piece
        self.board.movePiece(toPos, fromPos)
        if capturedPiece:
            self.board.board[toPos.x][toPos.y] = capturedPiece
        # if original_king_pos:
        #     if self.whiteToMove:
        #         self.whiteKingLocation = original_king_pos
        #     else:
        #         self.blackKingLocation = original_king_pos

        print(f"King in check: {in_check}")  # Print the value of in_check
        return not in_check
    
    def isItMate(self, color):
        """Check if the current player's king is in checkmate.
        Returns:
            - True if checkmate
            - False if not checkmate
            Sets self.checkmate or self.stalemate"""
        # 1) The king is threatened with capture
        # 2) The player can't the threatening piece
        # 3) The player can't block the threatening piece with another piece
        # 4) The player can't move the king to a square that is attacked by the opponent

        # If the king is not in check, it can't be checkmate
        if not self.isKingInCheck(color):
            # Check for stalemate - if no legal mvoes but not in check
            if not self.hasAnyLegalMoves():
                self.stalemate = True
                self.game_over = True
                return False
            return False
        
        # If in check, see if there are any legal moves that escape check
        if self.hasAnyLegalMoves():
            return False
        
        # If we're in check and have no legal moves, it's checkmate
        self.checkmate = True
        self.game_over = True
        return True
    def hasAnyLegalMoves(self):
        """
        Check if the current player has any legal moves available.
        Returns True if at least one legal move exists, False otherwise.
        """
        currentColor = WHITE if self.game_state.whiteToMove else BLACK

        #Check all pieces of the current player
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                piece = self.board.board[x][y]
                if piece and piece.color == currentColor:
                    # Get all potential moves for this piece
                    potential_moves = piece.get_raw_moves(self.board)

                    # Test each move
                    for move in potential_moves:
                        # Save the current board state
                        original_pos = piece.position
                        capturedPiece = self.board.getPieceAtPosition(move)

                        # Temporarily make the move
                        self.board.movePiece(original_pos, move)

                        # Check if this move is legal (doesn't leave/put king in check)
                        inCheck = self.isKingInCheck(self.game_state.whiteToMove)

                        # Restore the board state
                        piece.position = original_pos
                        self.board.board[original_pos.x][original_pos.y] = piece
                        self.board.board[move.x][move.y] = capturedPiece

                        # Check if this move leaves the king in check
                        if not self.isKingInCheck(currentColor):
                            # Restore the board state
                            piece.position = original_pos
                            self.board.board[original_pos.x][original_pos.y] = piece
                            if capturedPiece:
                                self.board.board[move.x][move.y] = capturedPiece
                            return True
                        
                        # Restore the board state
                        piece.position = original_pos
                        self.board.board[original_pos.x][original_pos.y] = piece
                        if capturedPiece:
                            self.board.board[move.x][move.y] = capturedPiece

        # No legal moves
        return False

    def threeFoldRepetitionRule(self):
        """Check if the current position has occurred three times, resulting in a draw."""
        pass

    def fiftyMoveRule(self):
        """Check for fifty-move rule."""

        no_pawn_move_or_capture = 0
        for move in reversed(self.game_state.moveLog):
            if isinstance(move['piece'], Pawn) or move['captured']:
                break
            no_pawn_move_or_capture += 1
        return no_pawn_move_or_capture >= 50

    def inSufficientMaterial(self):
        """Check for insufficient material."""
        white_pieces = 0
        black_pieces = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                piece = self.board.board[x][y]
                if piece:
                    if piece.color == WHITE:
                        white_pieces += 1
                    elif piece.color == BLACK:
                        black_pieces += 1

        if white_pieces == 1 or black_pieces == 1:
            return True
        if (white_pieces == 1 and black_pieces == 2 and 
            all(isinstance(self.board.board[x][y], (Knight, Bishop)) for x, y in ((0, 0), (0, 7), (7, 0), (7, 7)))):
            return True
        if (black_pieces == 1 and white_pieces == 2 and
            all(isinstance(self.board.board[x][y], (Knight, Bishop)) for x, y in ((0, 0), (0, 7), (7, 0), (7, 7)))):
            return True
        return False    

    def isGameDraw(self):
        """Check if the game is a draw."""
        return self.threeFoldRepetitionRule() or self.fiftyMoveRule() or self.inSufficientMaterial()
