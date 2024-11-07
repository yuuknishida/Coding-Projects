class Task:
    def __init__(self, title, priority, status, due_date):
        self.title = title
        self.priority = priority
        self.status = status
        self.due_date = due_date
    
    def assign_id(self):
        """Assigns a unique ID to the task."""
        self.id = len(self.title)

