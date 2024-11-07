import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

class Sidebar(tk.Frame):
    """Sidebar for the application"""
    def __init__(self, parent, expanded_width=200, collapsed_width=70):
        super().__init__(parent)
        self.parent = parent
        self.canvas = tk.Canvas()
        self.expanded_width = expanded_width
        self.collapsed_width = collapsed_width
        self.is_expanded = False
        self.is_animating = False

        self.animation_duration = 300
        self.animation_steps = 30
        self.current_step = 0

        self.config(bg='#2c3e50', # Dark blue bakcground
                    width=self.collapsed_width,
                    height=parent.winfo_height()
        )
        self.pack_propagate(False)
        self.pack(side='left', fill='y')

        self.content_frame = tk.Frame(self, bg='#2c3e50')
        self.content_frame.pack(side='top', fill="both", expand=True)

        # Add buttons
        self.icons = {
            'home': self.load_icon('icons/home.png'),
            'tasks': self.load_icon('icons/task.png'),
            'calendar': self.load_icon('icons/calendar.png'),
            'settings': self.load_icon('icons/settings.png'),
        }

        self.buttons = []
        button_data = [
            ("Home", 'home'),
            ("Tasks", 'tasks'),
            ("Calendar", 'calendar'),
            ("Settings", 'settings')
        ]

        # Create a button for demonstration
        for index, (text, icon_key) in enumerate(button_data):
            btn_frame = tk.Frame(self.content_frame, bg='#34495e')
            btn_frame.pack(fill="x", pady=10)

            btn = tk.Button(
                btn_frame,
                bg='#34495e',
                fg='white',
                relief='flat',
                compound='left',
                font=('Arial', 12),
                image=self.icons[icon_key]
            )
            btn.pack(fill='x')
            self.buttons.append((btn, text, icon_key))

            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#3498db'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg='#34495e'))
            btn_frame.bind('<Enter>', lambda e, b=btn: b.configure(bg='#3498db'))
            btn_frame.bind('<Leave>', lambda e, b=btn: b.configure(bg='#34495e'))

        spacer = tk.Frame(self, bg='#2c3e50')
        spacer.pack(fill="both", expand=True)

        # Bind to the frame
        self.bind('<Enter>', self.expand)
        self.bind('<Leave>', self.collapse)

        self.collapse_instant()
    
    def load_icon(self, icon_path):
        try:
            image = Image.open(icon_path)
            image = image.resize((50, 50), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading icon: {e}")
            return self.create_default_icon()
    
    def create_default_icon(self):
        img = Image.new('RGBA', (50, 50), color='white')
        return ImageTk.PhotoImage(img)

    def ease_in_out_cubic(self, t):
        if t < 0.5:
            return 4 * t * t * t
        p = 2 * t - 2
        return 0.5 * p * p * p + 1
    
    def expand(self, event):
        if not self.is_expanded and not self.is_animating:
            self.is_animating = True
            self.is_expanded = True
            self.current_step = 0
            self.start_width = self.winfo_width()
            self.width_diff = self.expanded_width - self.start_width
            self.animate()
            for btn, text, icon in self.buttons:
                btn.configure(image=self.icons[icon], text=f"{text}", anchor='w', padx=10)

    def collapse(self, event):
        if self.is_expanded and not self.is_animating:
            self.is_animating = True
            self.is_expanded = False
            self.current_step = 0
            self.start_width = self.winfo_width()
            self.width_diff = self.collapsed_width - self.start_width

            for btn, text, icon in self.buttons:
                btn.configure(image=self.icons[icon], text='', anchor='center', padx=0)

            self. animate()

    def animate(self):
        if self.current_step <= self.animation_steps:
            progress = self.ease_in_out_cubic(self.current_step / self.animation_steps)

            new_width = int(self.start_width + (self.width_diff * progress))
            self.configure(width=new_width)

            self.current_step += 1
            step_duration = self.animation_duration // self.animation_steps
            self.after(step_duration, self.animate)
        else:
            self.is_animating = False

    def collapse_instant(self):
        self.is_expanded = False
        self.configure(width=self.collapsed_width)
        for btn, text, icon in self.buttons:
            btn.configure(image=self.icons[icon], anchor='center', padx=0)