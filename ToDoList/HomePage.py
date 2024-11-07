from BasePage import BasePage
import tkinter as tk
class HomePage(BasePage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Welcome message
        tk.Label(self,
                 text="Welcome to your ToDo App!",
                 font=("Arial", 20, "bold")
                 ).pack(pady=20)
        
        # Overview frame
        overview_frame = tk.Frame(self)
        overview_frame.pack(fill="both", 
                            expand=True, 
                            padx=20, pady=10)

        # Add some sample content
        tk.Label(overview_frame, 
                 text="Some sample content here...",
                 font=("Arial", 12, "bold")
                 ).pack(anchor="w")
        
        stats_frame = tk.Frame(overview_frame)
        stats_frame.pack(fill="x", 
                            expand=True, 
                            padx=20, pady=10)
        
        self.create_stat_box(stats_frame, "Tasks Due Today", "10")
        self.create_stat_box(stats_frame, "Completed Tasks", "5")
        self.create_stat_box(stats_frame, "Upcoming Events", "3")

    def create_stat_box(self, parent, title, value):
        frame = tk.Frame(parent, relief="raised", borderwidth=1)
        frame.pack(side="left", padx=10, pady=10, ipadx=20, ipady=10)

        tk.Label(frame, text=title, font=("Arial", 12, "bold")).pack()
        tk.Label(frame, text=value, font=("Arial", 24, "bold")).pack()