import tkinter as tk
from tkinter import messagebox
import order_gui
import favorites_gui
import json
import refund_gui  # Import the refund GUI module

def open_order():
    order_gui.OrderWindow()

def open_favorites():
    favorites_gui.FavoritesWindow()

def open_cancel_delivery():
    # ... existing cancel delivery logic ...
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
    root.title("Restaurant Ordering System")
    root.geometry("400x350")
    
    header = tk.Label(root, text="Restaurant Ordering System", font=("Arial", 16))
    header.pack(pady=20)
    
    btn_order = tk.Button(root, text="Make Order", width=25, command=open_order)
    btn_order.pack(pady=5)
    
    btn_faves = tk.Button(root, text="View Favorite Orders", width=25, command=open_favorites)
    btn_faves.pack(pady=5)
    
    btn_refund = tk.Button(root, text="Request Refund", width=25, command=open_refund)
    btn_refund.pack(pady=5)
    
    btn_cancel_delivery = tk.Button(root, text="Cancel Delivery", width=25, command=open_cancel_delivery)
    btn_cancel_delivery.pack(pady=5)
    
    btn_exit = tk.Button(root, text="Exit", width=25, command=root.destroy)
    btn_exit.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        messagebox.showinfo("Exit", "Exiting the application.")
