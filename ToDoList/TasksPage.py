from BasePage import BasePage
import tkinter as tk
from tkinter import ttk
from TaskDatabase import TaskDatabase
from TaskForm import TaskForm

class TasksPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.task_db = TaskDatabase()
        self.task_form_page = TaskForm(self, self.controller, self.task_db)

        header_frame = tk.Frame(self)
        header_frame.pack(side="top", fill="x", pady=10)

        self.title_label =tk.Label(
            header_frame, 
            text="Tasks Page", 
            font=("Arial", 20, "bold")
        )
        self.title_label.pack()

        self.add_task_button = tk.Button(
                  header_frame,
                  text="+ Add New Task",
                  font=("Arial", 12, "bold"),
                  padx=20,
                  command=self.show_task_form
        )
        self.add_task_button.pack(side="right", padx=20)

        self.tasks_frame = tk.Frame(self)
        self.tasks_frame.pack(side="top",fill="both", expand=True)

        self.table = ttk.Treeview(self.tasks_frame)
        self.table["columns"] = ("id", "name", "priority", "status", "due_date")
        self.table["show"] = "headings"

        # Define column with row alignment
        self.table.column("id", anchor="center", width=1)
        self.table.column("name", anchor="center", width=200)
        self.table.column("priority", anchor="center", width=100)
        self.table.column("status", anchor="center", width=100)
        self.table.column("due_date", anchor="center", width=100)

        self.table.heading("id", text="Id", anchor="center")
        self.table.heading("name", text="Name", anchor="center")
        self.table.heading("priority", text="Priority", anchor="center")
        self.table.heading("status", text="Status", anchor="center")
        self.table.heading("due_date", text="Due Date", anchor="center")

        self.table.bind("<ButtonRelease-1>", self.on_item_click)

        self.table.pack(side="top", fill="x", anchor="n")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="gray", borderwidth=1, relief="flat")

        self.table.tag_configure("red", foreground="red")
        self.table.tag_configure("bold", font=("Arial", 16, "bold"))
        self.table.tag_configure("italic", font=("Arial", 16, "italic"))
        self.table.tag_configure("row", font=("Arial", 12))
        self.load_tasks()
    
    def show_task_form(self):
        self.controller.show_page("task_form")

    def load_tasks(self):
        self.table.delete(*self.table.get_children())

        tasks = self.task_db.get_all_tasks()
        for task in tasks:
            self.add_task_to_table(task)

    def add_task_to_table(self, task):
        task_id, name, priority, status, due_date = task

        self.table.insert("", 
                          "end", 
                          text=status,
                          values=(task_id, name, priority, status, due_date),
                          tags="row")
        
    def add_task(self):
        self.form_frame.destroy()
        title = self.name_entry.get()
        priority = self.priority_entry.get()
        status = self.status_entry.get()
        due_date = self.due_date_entry.get()

        self.task_db.add_task(title, priority, status, due_date)
        self.load_tasks()

    def on_item_click(self, event):
        selected_item = self.table.selection()
        if not selected_item:
            return
        item = selected_item[0]
        column = self.table.identify_column(event.x)

        column_index = int(column.strip('#')) - 1
        if column_index in [2,3,4]:
            self.edit_cell(item, column_index)

    def edit_cell(self, item, column_index):
        column_name = self.table["columns"][column_index]
        current_value = self.table.item(item, "values")[column_index]

        if column_name == "status":
            options = ["Not Started", "In Progress", "Completed"]
            self.edit_widget = ttk.Combobox(self, values=options, state="normal", width=15)
            self.edit_widget.set(current_value)
            self.edit_widget.place(x=100, y=100)
            self.edit_widget.bind("<FocusOut>", lambda e: self.save_edit(item, column_index, self.edit_widget.get()))
            self.edit_widget.bind("<Return>", lambda e: self.save_edit(item, column_index, self.edit_widget.get()))
            self.edit_widget.focus_set()

        elif column_name == "priority":
            options = ["Low", "Medium", "High"]
            self.edit_widget = ttk.Combobox(self, values=options, state="normal", width=15)
            self.edit_widget.set(current_value)
            self.edit_widget.place(x=100, y=100)
            self.edit_widget.bind("<FocusOut>", lambda e: self.save_edit(item, column_index, self.edit_widget.get()))
            self.edit_widget.bind("<Return>", lambda e: self.save_edit(item, column_index, self.edit_widget.get()))
            self.edit_widget.focus_set()

        elif column_name == "due_date":
            self.edit_widget = tk.Entry(self, width=15)
            self.edit_widget.insert(0, current_value)
            self.edit_widget.place(x=100, y=100)
            self.edit_widget.bind("<FocusOut>", lambda e: self.save_edit(item, column_index, self.edit_widget.get()))
            self.edit_widget.bind("<Return>", lambda e: self.save_edit(item, column_index, self.edit_widget.get()))
            self.edit_widget.focus_set()

    def save_edit(self, item, column_index, new_value):
        values = list(self.table.item(item, "values"))
        values[column_index] = new_value
        self.table.item(item, values=values)

        task_id = values[0]
        name = values[1]
        priority = values[2]
        status = values[3]
        due_date = values[4]
        self.task_db.update_task(task_id, name, priority, status, due_date)
        
        if hasattr(self, "edit_widget"):
            self.edit_widget.destroy()
            del self.edit_widget