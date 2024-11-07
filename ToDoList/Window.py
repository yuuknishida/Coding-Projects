import tkinter as tk
from Sidebar import Sidebar
from HomePage import HomePage
from CalendarPage import CalendarPage
from TasksPage import TasksPage
from SettingsPage import SettingsPage
from TaskForm import TaskForm

class Window(tk.Tk):
    """Represents the window of the application"""
    def __init__(self):
        super().__init__()

        # Screen width and height of display
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        self.geometry("%dx%d" % (self.width, self.height))
        self.title("ToDoList App")
        label = tk.Label(self, text="Welcome to your ToDoList!", font=("Arial", 20))
        label.pack()

        # Create a container for all pages
        self.container = tk.Frame(self)
        self.container.pack(side="right", fill="both", expand=True)

        # Dictionary to store all pages
        self.pages = {}

        # Create the sidebar
        self.sidebar = Sidebar(self)
        self.bind_buttons()

        # Initialize all pages
        self.setup_pages()

        # Show default page
        self.show_page("home")

    def bind_buttons(self):
        """Bind the sidebar buttons to their respective pages"""
        button_commands = {
            "Home": lambda: self.show_page("home"),
            "Tasks": lambda: self.show_page("tasks"),
            "Calendar": lambda: self.show_page("calendar"),
            "Settings": lambda: self.show_page("settings"),
            "Add Task Form": lambda: self.show_page("task_form")
        }

        for button, text, _ in self.sidebar.buttons:
            button.configure(command=button_commands[text])

    def setup_pages(self):
        """Initialize all application pages"""
        # Home page
        home = HomePage(self.container, self)
        self.pages["home"] = home

        # Tasks page
        tasks = TasksPage(self.container, self)
        self.pages["tasks"] = tasks

        # Calendar page
        calendar = CalendarPage(self.container, self)
        self.pages["calendar"] = calendar

        # Settings page
        settings = SettingsPage(self.container, self)
        self.pages["settings"] = settings

        # Add task form 
        task_form = TaskForm(self.container, self, tasks.task_db)
        self.pages["task_form"] = task_form

    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()

        self.pages[page_name].pack(fill="both", expand=True)