import tkinter as tk
from tkinter import messagebox
class PromotionDialog(tk.Toplevel):
    def __init__(self, master, on_select):
        super().__init__(master)
        self.title("Promote Pawn")
        self.on_select = on_select

        # Make dialog modal
        self.transient(master)
        self.grab_set()

        # Remove the close button from the window manager
        self.protocol("WM_DELETE_WINDOW", self.disable_close)

        # Center the dialog on the screen
        self.geometry("200x200")
        self.resizable(False, False)

        # Configure the dialog
        self.configure(bg="white")

        self.label = tk.Label(self, 
                              text="Pawn Promotion\nSelect a piece to promote to:",
                              bg="white",
                              font=("Arial", 16),
                              pady=10)
        self.label.pack()

        # Create a frame for the buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        button_style = {
            "width": 10,
            "font": ("Arial", 12),
            "relief": tk.RAISED,
            "pady": 5
        }

        self.pieces = ["Queen", "Rook", "Bishop", "Knight"]
        for piece in self.pieces:
            button = tk.Button(button_frame, text=piece, command=lambda piece=piece: self.select_piece(piece), **button_style)
            button.pack(pady=2)
    def disable_close(self):
        """Prevent the user from closing the dialog with the x button"""
        messagebox.showinfo("Promotion Required",
                            "You must select a piece for pawn promotion.\nPromotion is mandatory in chess.",
                            parent=self)
        
    def select_piece(self, piece):
        self.on_select(piece)
        self.destroy()