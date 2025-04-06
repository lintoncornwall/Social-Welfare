import tkinter as tk
from tkinter import messagebox
import json
import os
from RefundManagement.refund_manager import RefundManager

# Import pricing functions
from OrderPlacement.prices import get_size_price, get_side_price, get_special_cost, get_beverage_price

class RefundWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Request Refund")
        self.geometry("500x400")
        self.refund_manager = RefundManager()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Enter Receipt Number for Refund:", font=("Arial", 12)).pack(pady=10)
        self.receipt_entry = tk.Entry(self, font=("Arial", 12))
        self.receipt_entry.pack(pady=5)
        tk.Button(self, text="Submit", font=("Arial", 12), command=self.lookup_receipt).pack(pady=10)
        tk.Button(self, text="Cancel", font=("Arial", 12), command=self.destroy).pack(pady=5)

    def lookup_receipt(self):
        receipt_number = self.receipt_entry.get().strip()
        if not receipt_number:
            messagebox.showerror("Error", "Please enter a receipt number.")
            return

        receipts = self.refund_manager.load_cashed_receipts()
        matched_receipt = None
        for receipt in receipts:
            if receipt.get("receipt_number") == receipt_number:
                matched_receipt = receipt
                break

        if not matched_receipt:
            messagebox.showerror("Error", "Receipt number not found.")
            return

        details = self.format_receipt_details(matched_receipt)
        confirm = messagebox.askyesno("Confirm Refund", f"Order Details:\n\n{details}\n\nDo you want to request a refund for this order?")
        if confirm:
            transaction_id = self.refund_manager.generate_transaction_reference()
            self.refund_manager.log_refund(matched_receipt, transaction_id)
            receipts.remove(matched_receipt)
            self.refund_manager.save_cashed_receipts(receipts)
            messagebox.showinfo("Refund Processed", f"Refund processed successfully!\nTransaction Reference:\n{transaction_id}")
            self.destroy()
        else:
            messagebox.showinfo("Refund Cancelled", "Refund request cancelled.")
            self.destroy()

    def format_receipt_details(self, receipt):
        # Retrieve the meal type stored with the receipt
        meal_type = receipt.get('meal_type', 'lunch')  # default to 'lunch' if missing
        details = f"Receipt Number: {receipt.get('receipt_number')}\n"
        details += "Orders:\n"
        for idx, order in enumerate(receipt.get("orders", []), 1):
            details += f"\nOrder {idx}:\n"
            # Recalculate or fallback to stored values if missing
            main_price = order.get('main_price')
            if main_price is None:
                main_price = get_size_price(meal_type, order.get('size'))
            side_price = order.get('side_price')
            if side_price is None:
                side_price = get_side_price()
            
            # Handle daily special price
            special = order.get('special')
            if special:
                special_price = order.get('special_cost')
                if special_price is None:
                    special_price = get_special_cost(meal_type)
            else:
                special = 'None'
                special_price = 0.00

            # Handle beverage price
            beverage = order.get('beverage')
            if beverage:
                beverage_price = order.get('beverage_price')
                if beverage_price is None:
                    beverage_price = get_beverage_price(meal_type, beverage)
            else:
                beverage = 'None'
                beverage_price = 0.00
                
            details += f"  Main: {order.get('main')} ({order.get('size')}) - ${main_price:.2f}\n"
            details += f"  Side: {order.get('side')} - ${side_price:.2f}\n"
            details += f"  Daily Special: {special} - ${special_price:.2f}\n"
            details += f"  Customization: {order.get('customization')}\n"
            details += f"  Beverage: {beverage} - ${beverage_price:.2f}\n"
        details += f"\nTotal Cost: ${receipt.get('total_cost'):.2f}\n"
        return details

