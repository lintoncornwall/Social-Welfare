# delivery_gui.py
import tkinter as tk
from tkinter import messagebox
import json
import datetime
from OrderPlacement.receipt import load_receipt_number  # Adjust the import path as needed

class DeliveryWindow:
    def __init__(self, order_window):
        self.order_window = order_window
        self.window = tk.Toplevel()
        self.window.title("Delivery Details")
        self.window.geometry("400x350")  # Increased height to fit extra button
        
        # Frame for delivery details
        self.delivery_frame = tk.Frame(self.window)
        self.delivery_frame.pack(fill="both", expand=True)
        
        # Ask for delivery option (address, phone, email)
        tk.Label(self.delivery_frame, text="Enter your delivery address:").pack(pady=5)
        self.address_entry = tk.Entry(self.delivery_frame)
        self.address_entry.pack(pady=5)
        
        tk.Label(self.delivery_frame, text="Enter your phone number:").pack(pady=5)
        self.phone_entry = tk.Entry(self.delivery_frame)
        self.phone_entry.pack(pady=5)
        
        tk.Label(self.delivery_frame, text="Enter your email address:").pack(pady=5)
        self.email_entry = tk.Entry(self.delivery_frame)
        self.email_entry.pack(pady=5)
        
        # Button to confirm delivery details
        tk.Button(self.delivery_frame, text="Confirm Delivery", command=self.confirm_delivery).pack(pady=10)
        
        # Button to cancel an existing delivery
        tk.Button(self.delivery_frame, text="Cancel Delivery", command=self.open_cancel_window).pack(pady=10)

    def confirm_delivery(self):
        address = self.address_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not address or not phone or not email:
            messagebox.showerror("Invalid Input", "Please fill in all fields.")
            return
        
        # Get current timestamp for the delivery request time
        order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Retrieve the receipt number from the receipt module (formatted as 8 digits)
        receipt_number = f"{load_receipt_number():08d}"
        
        # Store delivery info with the receipt number
        self.order_window.delivery_details = {
            "receipt_number": receipt_number,  # Added receipt number
            "address": address,
            "phone": phone,
            "email": email,
            "order_time": order_time
        }
        
        # Save the delivery details to delivery_requests.json
        self.save_delivery_details(self.order_window.delivery_details)
        
        messagebox.showinfo("Delivery Confirmed", "Your delivery details have been confirmed.")
        self.window.destroy()
        
        # Proceed to payment view
        self.order_window.show_payment_view()

    def save_delivery_details(self, details):
        """Function to save delivery details to delivery_requests.json"""
        try:
            # Load existing data from the JSON file, if available.
            try:
                with open("delivery_requests.json", "r") as file:
                    delivery_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                delivery_data = []  # If the file is empty or doesn't exist, start with an empty list
            
            # Append new delivery details to the list
            delivery_data.append(details)
            
            # Save back the updated data to the file
            with open("delivery_requests.json", "w") as file:
                json.dump(delivery_data, file, indent=4)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save delivery details: {str(e)}")
    
    def open_cancel_window(self):
        """Open a new window to cancel the delivery window by simply closing it."""
        cancel_win = tk.Toplevel(self.window)
        cancel_win.title("Cancel Delivery")
        cancel_win.geometry("400x200")
        
        tk.Label(cancel_win, text="Are you sure you want to cancel the delivery?", font=("Arial", 12)).pack(pady=10)

        def cancel_delivery_window():
            cancel_win.destroy()  # Close the cancel window
            self.window.destroy()  # Close the main delivery window
        
        tk.Button(cancel_win, text="Cancel Delivery", command=cancel_delivery_window, font=("Arial", 12)).pack(pady=20)
