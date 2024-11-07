class GameState:
    """
    Manages game state and turn management
    """
    def __init__(self, board):
        self.board = board
        self.whiteToMove = True
        self.moveLog = []
        self.game_over = False
        self.checkmate = False
        self.stalemate = False
        self.halfmove_clock = 0 # To track the fifty-move rule
        self.position_history = []  # To track positions for threefold repetition
    def switchTurn(self):
        self.whiteToMove = not self.whiteToMove
        self.halfmove_clock += 1
    def recordMove(self, piece, fromPos, toPos, capturedPiece=None, specialMove=None):
        move_info = {
            'piece': piece,
            'from': fromPos,
            'to': toPos,
            'captured': capturedPiece,
            'special': specialMove
        }
        self.moveLog.append(move_info)
        self.position_history.append(self.get_position_string()) # Track the position
    def get_position_string(self):
        """Generate a string representation of the current board position."""
        return ''.join(
            [str(piece) if piece else '.' for row in self.board.board for piece in row]
        )
    