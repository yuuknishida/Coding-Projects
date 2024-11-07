import tkinter as tk
from tkinter import ttk
from BasePage import BasePage

class TaskForm(BasePage):
    def __init__(self, parent, controller, task_db):
        super().__init__(parent, controller)
        self.task_db = task_db
        self.form_frame = None
        self.name_entry = None
        self.priority_entry = None
        self.status_entry = None
        self.due_date_entry = None

        self.title_label = tk.Label(
            self,
            text="Task Form",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        self.show_task_form()

    def show_task_form(self):
        self.form_frame = tk.Frame(self)
        self.form_frame.pack(side="left", fill="y", padx=20)

        # Name
        self.name_label = tk.Label(self.form_frame, text="Name:")
        self.name_label.pack(anchor="w", pady=5)
        self.name_entry = tk.Entry(self.form_frame)
        self.name_entry.pack(fill="x",pady=5)

        # Priority
        self.priority_label = tk.Label(self.form_frame, text="Priority:")
        self.priority_label.pack(anchor="w", pady=5)
        self.priority_entry = ttk.Combobox(self.form_frame, values=["Low", "Medium", "High"])
        self.priority_entry.pack(fill="x", pady=5)

        # Status
        self.status_label = tk.Label(self.form_frame, text="Status:")
        self.status_label.pack(anchor="w", pady=5)
        self.status_entry = ttk.Combobox(self.form_frame, values=["Not Started", "In Progress", "Completed"])
        self.status_entry.pack(fill="x", pady=5)

        # Due Date
        self.due_date_label = tk.Label(self.form_frame, text="Due Date:")
        self.due_date_label.pack(anchor="w", pady=5)
        self.due_date_entry = tk.Entry(self.form_frame)
        self.due_date_entry.pack(fill="x", pady=5)

        # Add Task Button
        self.add_task_button = tk.Button(
            self.form_frame,
            text="Add Task",
            command=self.add_task
        )
        self.add_task_button.pack(pady=10)

    def add_task(self):
        title = self.name_entry.get()
        priority = self.priority_entry.get()
        status = self.status_entry.get()
        due_date = self.due_date_entry.get()

        self.task_db.add_task(title, priority, status, due_date)
        self.controller.pages["tasks"].load_tasks()
        self.form_frame.destroy()
        self.controller.show_page("tasks")