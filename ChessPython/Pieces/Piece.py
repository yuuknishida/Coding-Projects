from Config import *
import tkinter as tk
from PIL import Image, ImageTk
class Piece:
    def __init__(self, color, position, canvas, image):
        self.color = color
        self.position = position
        self.canvas = canvas
        self.image = self.loadImage(image)
    
    def loadImage(self, image):    # meant to be overwritten
        """Load the image of the piece"""
        try: 
            if image is None:
                return None
            open = Image.open(image).resize((SQUARE_SIZE, SQUARE_SIZE))
            return ImageTk.PhotoImage(open)
        except Exception as e:
            print(f"Error loading image for {self.kind} : {e}")
            return None 
        
    def draw(self):
        x, y = self.position.x * SQUARE_SIZE, self.position.y * SQUARE_SIZE
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.image)
    
    def get_raw_moves(self, board):
        """Get potential moves without check validation"""
        raise NotImplementedError("This method should be implemented by subclasses")

    def get_color(self):
        return self.color

    def get_position(self):
        return self.position