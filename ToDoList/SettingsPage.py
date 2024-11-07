from BasePage import BasePage
import tkinter as tk

class SettingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(
            self,
            text="Settings",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # Settings sections
        self.create_settings_section("General Settings")
        self.create_settings_section("Notifications")
        self.create_settings_section("Theme")
        self.create_settings_section("Account")
        
    def create_settings_section(self, title):
        section = tk.LabelFrame(self, text=title, font=("arial", 12, "bold"), padx=20, pady=10)
        section.pack(fill="x", padx=20, pady=10)

        tk.Checkbutton(section,
                       text="Enable Notifications").pack(anchor="w")
        
        tk.Checkbutton(section,
                       text="Dark Mode").pack(anchor="w")