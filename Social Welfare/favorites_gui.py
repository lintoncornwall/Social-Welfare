#favorites_gui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

from delivery_gui import DeliveryWindow
from OrderPlacement.receipt import format_receipt, calculateTotal

class ReceiptWindow:
    def __init__(self, receipt_text):
        self.window = tk.Toplevel()  # New window for the receipt
        self.window.title("Receipt")
        self.window.geometry("600x600")  # Size for receipt display
        
        receipt_label = tk.Label(self.window, text="---- Order Receipt ----", font=("Arial", 16))
        receipt_label.pack(pady=10)
        
        receipt_text_widget = tk.Text(self.window, wrap="word", font=("Courier", 10))
        receipt_text_widget.insert("1.0", receipt_text)
        receipt_text_widget.config(state="disabled")
        receipt_text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        
        back_button = tk.Button(self.window, text="Back to Main Menu", command=self.close_receipt_window, font=("Arial", 12))
        back_button.pack(pady=10)

    def close_receipt_window(self):
        self.window.destroy()  # Close the receipt window
        # Optionally, you can add logic to return to the favorites menu or the main app window here.

class FavoritesWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Favorite Orders")
        self.window.geometry("600x600")  # Increased size for receipt display
        
        # These will be set when an order is started
        self.selected_favorite = None
        self.meal_type = None
        
        tk.Label(self.window, text="Favorite Orders", font=("Arial", 16)).pack(pady=10)
        
        # Listbox to show favorites
        self.favorites_listbox = tk.Listbox(self.window, width=60, height=10)
        self.favorites_listbox.pack(pady=10)
        self.load_favorites()
        
        # Buttons to order or delete a favorite
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Order Selected", command=self.order_selected).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Close", command=self.window.destroy).grid(row=0, column=2, padx=5)
        
        # Frame for displaying the receipt (Initially hidden)
        self.receipt_frame = tk.Frame(self.window)
    
    def load_favorites(self):
        self.favorites = []
        if os.path.exists("favorites.json"):
            try:
                with open("favorites.json", "r") as f:
                    self.favorites = json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Error reading favorites file.")
        
        self.favorites_listbox.delete(0, tk.END)
        for idx, fav in enumerate(self.favorites, start=1):
            item_text = f"{idx}. {fav.get('main', 'N/A')} with {fav.get('side', 'N/A')}"
            self.favorites_listbox.insert(tk.END, item_text)
    
    def order_selected(self):
        # 1) Select a favorite
        sel = self.favorites_listbox.curselection()
        if not sel:
            messagebox.showwarning("Selection", "Please select a favorite order.")
            return
        fav = self.favorites[sel[0]]

        # 2) Initial confirmation
        if not messagebox.askyesno("Confirm Order",
                                f"Place order for {fav.get('main')} with {fav.get('side')}?"):
            return

        # 3) Meal type
        mt = simpledialog.askstring("Meal Type", "Enter meal type (breakfast/lunch):")
        if not mt or mt.strip().lower() not in ("breakfast", "lunch"):
            messagebox.showerror("Invalid Input", "You must enter 'breakfast' or 'lunch'.")
            return
        self.meal_type = mt.strip().lower()

        # 4) Delivery vs. Pickup
        dt = simpledialog.askstring("Delivery or Pickup", "Enter 'delivery' or 'pickup':")
        if not dt or dt.strip().lower() not in ("delivery", "pickup"):
            messagebox.showerror("Invalid Input", "You must enter 'delivery' or 'pickup'.")
            return
        dt = dt.strip().lower()
        fav['order_type'] = dt

        # Save for payment
        self.selected_favorite = fav

        # 5) If delivery, hand off to your delivery GUI
        if dt == 'delivery':
            DeliveryWindow(self)
        else:
            # Pickup goes straight to payment
            self.show_payment_view()

    def show_payment_view(self):
        """
        Called by order_selected (for pickup) or by DeliveryWindow.confirm_delivery
        once address/phone/email have been captured.
        """
        # 6) Choose payment method
        method = simpledialog.askinteger(
            "Payment Method",
            "Select payment method:\n1. Credit Card\n2. PayPal"
        )
        if method not in (1, 2):
            messagebox.showerror("Invalid Input", "Please enter 1 or 2.")
            return

        # 7) Collect payment details
        if method == 1:
            card = simpledialog.askstring("Credit Card", "Enter card number:")
            exp  = simpledialog.askstring("Expiry Date", "Enter expiry (MM/YY):")
            cvv  = simpledialog.askstring("CVV", "Enter CVV:")
            if not all([card, exp, cvv]):
                messagebox.showerror("Payment Error", "All credit card fields are required.")
                return
        else:
            email = simpledialog.askstring("PayPal", "Enter your PayPal email:")
            if not email or "@" not in email:
                messagebox.showerror("Payment Error", "Please enter a valid email.")
                return

        # 8) Final confirmation
        total = calculateTotal([self.selected_favorite], self.meal_type)
        if not messagebox.askyesno("Confirm Payment", f"Confirm payment of ${total:.2f}?"):
            messagebox.showinfo("Order", "Payment cancelled; order not placed.")
            return

        # 9) Generate, save & display receipt
        receipt_text = format_receipt([self.selected_favorite], self.meal_type)

        # 10) Open the receipt window
        ReceiptWindow(receipt_text)
    
    def show_receipt(self, receipt_text):
        # Clear the page before showing the receipt
        for widget in self.window.winfo_children():
            widget.grid_forget()  # Remove current widgets (e.g., buttons, listbox)
        
        # Display receipt in the same window
        receipt_label = tk.Label(self.receipt_frame, text="---- Order Receipt ----", font=("Arial", 16))
        receipt_label.pack(pady=10)
        
        receipt_text_widget = tk.Text(self.receipt_frame, wrap="word", font=("Courier", 10))
        receipt_text_widget.insert("1.0", receipt_text)
        receipt_text_widget.config(state="disabled")
        receipt_text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        
        back_button = tk.Button(self.receipt_frame, text="Back to Main Menu", command=self.show_main_menu, font=("Arial", 12))
        back_button.pack(pady=10)
        
        self.receipt_frame.pack(fill="both", expand=True)

    def show_main_menu(self):
        """Show the main menu again after receipt."""
        self.receipt_frame.pack_forget()
        self.load_favorites()  # Reload the favorites and main menu buttons

    def delete_selected(self):
        sel = self.favorites_listbox.curselection()
        if not sel:
            messagebox.showwarning("Selection", "Select a favorite order to delete.")
            return
        idx = sel[0]
        if messagebox.askyesno("Delete", "Are you sure you want to delete this favorite?"):
            del self.favorites[idx]
            with open("favorites.json", "w") as f:
                json.dump(self.favorites, f, indent=4)
            self.load_favorites()
            messagebox.showinfo("Deleted", "Favorite removed.")
