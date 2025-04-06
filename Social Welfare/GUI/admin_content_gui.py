#admin_content_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

class AdminContentWindow:
    def __init__(self, update_main_menu_callback, hours_label):
        self.update_main_menu_callback = update_main_menu_callback  # Callback function to update the main menu
        self.hours_label = hours_label  # Pass the label here to update it
        self.window = tk.Toplevel()
        self.window.title("Admin Content")
        self.window.geometry("800x600")
        
        # Notebook for two main tabs: Menu Items and Opening Hours
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True)
        
        self.create_menu_items_tab()
        self.create_opening_hours_tab()
        
        btn_close = tk.Button(self.window, text="Close", command=self.window.destroy, font=("Arial", 12))
        btn_close.pack(pady=10)
    
    def create_menu_items_tab(self):
        # Tab for editing CSV menu items
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Menu Items")
        
        # Create a sub-notebook to switch between Breakfast and Lunch
        self.menu_notebook = ttk.Notebook(frame)
        self.menu_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Breakfast CSV editor tab
        self.breakfast_frame = ttk.Frame(self.menu_notebook)
        self.menu_notebook.add(self.breakfast_frame, text="Breakfast Menu")
        self.breakfast_text = tk.Text(self.breakfast_frame, wrap="none", font=("Courier", 10))
        self.breakfast_text.pack(fill="both", expand=True, padx=5, pady=5)
        btn_save_breakfast = tk.Button(self.breakfast_frame, text="Save Breakfast Menu", command=self.save_breakfast_menu, font=("Arial", 12))
        btn_save_breakfast.pack(pady=5)
        
        # Lunch CSV editor tab
        self.lunch_frame = ttk.Frame(self.menu_notebook)
        self.menu_notebook.add(self.lunch_frame, text="Lunch Menu")
        self.lunch_text = tk.Text(self.lunch_frame, wrap="none", font=("Courier", 10))
        self.lunch_text.pack(fill="both", expand=True, padx=5, pady=5)
        btn_save_lunch = tk.Button(self.lunch_frame, text="Save Lunch Menu", command=self.save_lunch_menu, font=("Arial", 12))
        btn_save_lunch.pack(pady=5)
        
        # Load the initial CSV data into the text widgets.
        self.load_csv_data("ContentEditing/Breakfast.csv", self.breakfast_text)
        self.load_csv_data("ContentEditing/Lunch.csv", self.lunch_text)
    
    def load_csv_data(self, file_path, text_widget):
        """Load CSV file content into the provided text widget."""
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", newline="") as f:
                    content = f.read()
                text_widget.delete("1.0", tk.END)
                text_widget.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load {file_path}: {str(e)}")
        else:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, "")
    
    def save_csv_data(self, file_path, text_widget):
        """Save the content of the text widget to the specified CSV file."""
        content = text_widget.get("1.0", tk.END)
        try:
            with open(file_path, "w", newline="") as f:
                f.write(content)
            messagebox.showinfo("Success", f"Saved {file_path} successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save {file_path}: {str(e)}")
    
    def save_breakfast_menu(self):
        self.save_csv_data("ContentEditing/Breakfast.csv", self.breakfast_text)
    
    def save_lunch_menu(self):
        self.save_csv_data("ContentEditing/Lunch.csv", self.lunch_text)
    
    def create_opening_hours_tab(self):
        # Tab for editing opening hours
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Opening Hours")
        
        self.hours_entries = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Dropdown options for breakfast and lunch
        breakfast_options = [
            "8:00 AM - 11:30 AM", "7:00 AM - 11:00 AM", "7:30 AM - 12:00 PM", "Not set"
        ]
        lunch_options = [
            "11:30 AM - 6:00 PM", "12:00 PM - 6:30 PM", "Not set"
        ]
        
        # Load existing opening hours if available.
        hours = {}
        if os.path.exists("hours.json"):
            try:
                with open("hours.json", "r") as f:
                    hours = json.load(f)
            except json.JSONDecodeError:
                hours = {}
        
        row = 0
        for day in days:
            tk.Label(frame, text=day + ":", font=("Arial", 12)).grid(row=row, column=0, padx=10, pady=5, sticky="e")
            
            # Breakfast hours dropdown
            breakfast_combobox = ttk.Combobox(frame, values=breakfast_options, font=("Arial", 12), width=25)
            breakfast_combobox.set(hours.get(f"{day}_breakfast", "8:00 AM - 11:30 AM"))
            breakfast_combobox.grid(row=row, column=1, padx=10, pady=5)
            self.hours_entries[f"{day}_breakfast"] = breakfast_combobox
            
            # Lunch hours dropdown
            lunch_combobox = ttk.Combobox(frame, values=lunch_options, font=("Arial", 12), width=25)
            lunch_combobox.set(hours.get(f"{day}_lunch", "11:30 AM - 6:00 PM"))
            lunch_combobox.grid(row=row, column=2, padx=10, pady=5)
            self.hours_entries[f"{day}_lunch"] = lunch_combobox
            
            row += 1
        
        # Add instruction for time format
        instruction_label = tk.Label(frame, text="Select breakfast and lunch hours, respectively, for each day.", font=("Arial", 10), fg="gray")
        instruction_label.grid(row=row, column=0, columnspan=3, pady=10)

        btn_save_hours = tk.Button(frame, text="Save Opening Hours", command=self.save_opening_hours, font=("Arial", 12))
        btn_save_hours.grid(row=row+1, column=0, columnspan=3, pady=10)
    
    
    def save_opening_hours(self):
        """Collect data from the dropdowns and save it to hours.json."""
        hours = {}
        
        # Collect and save the selected breakfast and lunch hours for each day
        for day in self.hours_entries:
            hours[day] = self.hours_entries[day].get()
        
        try:
            with open("hours.json", "w") as f:
                json.dump(hours, f, indent=4)
            messagebox.showinfo("Success", "Opening hours updated successfully.")
            
            # After saving, update the main menu with the new hours
            self.update_main_menu_callback(self.hours_label)  # Pass the label to the update function
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save opening hours: {str(e)}")
