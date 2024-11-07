from BasePage import BasePage
import tkinter as tk

class CalendarPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(self,
                 text="Calendar Page",
                 font=("Arial", 20, "bold")
                 ).pack(pady=20)
        
        options_frame = tk.Frame(self)
        options_frame.pack(fill="x", 
                           expand=True, 
                           padx=20, pady=10)
        
        tk.Button(options_frame,
                  text="Add Event",
                  font=("Arial", 12, "bold"),
                  padx=20,
                  pady=5
                  ).pack(side="left", padx=10)
        
        tk.Button(options_frame,
                  text="Delete Event",
                  font=("Arial", 12, "bold"),
                  padx=20,
                  pady=5
                  ).pack(side="left", padx=10)
        
        tk.Button(options_frame,
                  text="Edit Event",
                  font=("Arial", 12, "bold"),
                  padx=20,
                  pady=5
                  ).pack(side="left", padx=10)
        
        calendar_frame = tk.Frame(self, relief="solid", borderwidth=1)
        calendar_frame.pack(fill="both", 
                           expand=True, 
                           padx=20, pady=10)
        
        tk.Label(calendar_frame,
                 text="Calendar view coming soon",
                 font=("Arial", 12, "bold")
                 ).pack(expand=True)
        