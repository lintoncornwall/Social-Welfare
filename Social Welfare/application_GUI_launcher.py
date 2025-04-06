# application_GUI_launcher.py
import tkinter as tk
from tkinter import messagebox
import json
import GUI.order_gui as order_gui
import GUI.favorites_gui as favorites_gui
import GUI.refund_gui as refund_gui  # Import the refund GUI module

# Helper functions to load opening hours from file or use defaults.
def load_opening_hours():
    default_breakfast = "8:00 AM - 11:30 AM"
    default_lunch = "11:30 AM - 6:00 PM"
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule = {}
    try:
        with open("hours.json", "r") as f:
            schedule = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        schedule = {}

    # Build a display string. The admin may have stored a custom string per day.
    hours_text = "Opening Hours:\n"
    for day in days:
        # Retrieve stored times (or use defaults)
        breakfast_val = schedule.get(f"{day}_breakfast", default_breakfast)
        lunch_val = schedule.get(f"{day}_lunch", default_lunch)

        # Ensure we include the labels "Breakfast:" and "Lunch:"
        if not breakfast_val.lower().startswith("breakfast:"):
            breakfast_val = "Breakfast: " + breakfast_val
        if not lunch_val.lower().startswith("lunch:"):
            lunch_val = "Lunch: " + lunch_val

        # Combine and display
        day_hours = f"{breakfast_val} | {lunch_val}"
        hours_text += f"{day}: {day_hours}\n"

    return hours_text

def update_hours_display(label):
    label.config(text=load_opening_hours())

def open_admin_content(hours_label):
    # Create a login window
    login_win = tk.Toplevel()
    login_win.title("Admin Login")
    login_win.geometry("300x200")
    
    tk.Label(login_win, text="Username:", font=("Arial", 12)).pack(pady=5)
    username_entry = tk.Entry(login_win, font=("Arial", 12))
    username_entry.pack(pady=5)
    
    tk.Label(login_win, text="Password:", font=("Arial", 12)).pack(pady=5)
    password_entry = tk.Entry(login_win, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)
    
    def verify_credentials():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if username.lower() == "admin" and password == "12345":
            login_win.destroy()
            import GUI.admin_content_gui as admin_content_gui  # Ensure this module is in your PYTHONPATH or same directory
            admin_content_gui.AdminContentWindow(update_hours_display, hours_label)  # Open admin content
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
    
    tk.Button(login_win, text="Login", command=verify_credentials, font=("Arial", 12)).pack(pady=10)

def open_order():
    order_gui.OrderWindow()

def open_favorites():
    favorites_gui.FavoritesWindow()

def open_cancel_delivery():
    cancel_win = tk.Toplevel()
    cancel_win.title("Cancel Delivery")
    cancel_win.geometry("400x200")
    
    tk.Label(cancel_win, text="Enter Receipt Number to Cancel:", font=("Arial", 12)).pack(pady=10)
    receipt_entry = tk.Entry(cancel_win, font=("Arial", 12))
    receipt_entry.pack(pady=5)
    
    def perform_cancellation():
        receipt_number = receipt_entry.get().strip()
        if not receipt_number:
            messagebox.showerror("Error", "Please enter a receipt number.")
            return
        
        cancelled = False
        
        # Remove from receipts.json
        try:
            with open("receipts.json", "r") as f:
                receipts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            receipts = []
        
        initial_count = len(receipts)
        receipts = [r for r in receipts if r.get("receipt_number") != receipt_number]
        if len(receipts) < initial_count:
            cancelled = True
            with open("receipts.json", "w") as f:
                json.dump(receipts, f, indent=4)
        
        # Remove from delivery_requests.json
        try:
            with open("delivery_requests.json", "r") as f:
                deliveries = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            deliveries = []
        
        initial_count = len(deliveries)
        deliveries = [d for d in deliveries if d.get("receipt_number") != receipt_number]
        if len(deliveries) < initial_count:
            cancelled = True
            with open("delivery_requests.json", "w") as f:
                json.dump(deliveries, f, indent=4)
        
        if cancelled:
            messagebox.showinfo("Cancellation", f"Delivery for receipt {receipt_number} has been canceled.")
        else:
            messagebox.showerror("Cancellation", f"No delivery found for receipt {receipt_number}.")
        cancel_win.destroy()
    
    tk.Button(cancel_win, text="Cancel Delivery", command=perform_cancellation, font=("Arial", 12)).pack(pady=20)

def open_refund():
    refund_gui.RefundWindow()

def main_menu():
    root = tk.Tk()
    root.title("Social Welfare Ordering System")
    root.geometry("400x450")
    
    header = tk.Label(root, text="Social Welfare Ordering System", font=("Arial", 16))
    header.pack(pady=10)
    
    # Opening Hours Display Section
    hours_frame = tk.Frame(root)
    hours_frame.pack(pady=5)
    
    # Define the hours_label here before passing it
    hours_label = tk.Label(hours_frame, text=load_opening_hours(), font=("Arial", 10), justify="left")
    hours_label.pack()
    
    btn_refresh = tk.Button(hours_frame, text="Refresh Hours", command=lambda: update_hours_display(hours_label), font=("Arial", 10))
    btn_refresh.pack(pady=5)
    
    # Main Menu Buttons
    btn_order = tk.Button(root, text="Make Order", width=25, command=open_order)
    btn_order.pack(pady=5)
    
    btn_faves = tk.Button(root, text="View Favorite Orders", width=25, command=open_favorites)
    btn_faves.pack(pady=5)
    
    btn_refund = tk.Button(root, text="Request Refund", width=25, command=open_refund)
    btn_refund.pack(pady=5)
    
    btn_cancel_delivery = tk.Button(root, text="Cancel Delivery", width=25, command=open_cancel_delivery)
    btn_cancel_delivery.pack(pady=5)
    
    btn_admin = tk.Button(root, text="Admin Content", width=25, command=lambda: open_admin_content(hours_label))
    btn_admin.pack(pady=5)
    
    btn_exit = tk.Button(root, text="Exit", width=25, command=root.destroy)
    btn_exit.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        messagebox.showinfo("Exit", "Exiting the application.")
