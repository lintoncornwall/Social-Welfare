#order_gui.py
import tkinter as tk
from tkinter import messagebox
import json
import datetime
# Import business logic and pricing functions.
from OrderPlacement.order import process_order_data
from OrderPlacement.prices import get_size_price, get_side_price, get_special_cost, get_beverage_price
from OrderPlacement.receipt import format_receipt
from OrderPlacement.menu import load_menu  # New import for loading CSV menus
from GUI.delivery_gui import DeliveryWindow  # Ensure this matches the path to your delivery_gui.py file

class OrderWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Make Order")
        self.window.geometry("600x700")
        
        # Determine meal type and load corresponding menu based on current time.
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        if "00:00" <= current_time <= "11:30":
            self.meal_type = 'breakfast'
            self.menu = load_menu('ContentEditing/Breakfast.csv')
        elif "11:30" < current_time <= "23:59":
            self.meal_type = 'lunch'
            self.menu = load_menu('ContentEditing/Lunch.csv')
        else:
            messagebox.showerror("Ordering Time Error", "Ordering is only available between 8:00AM and 6:00PM.")
            self.window.destroy()
            return
        
        # Get today's menu based on day name.
        day = now.strftime("%A")
        self.day_menu = self.menu.get(day, {})

        # Initialize orders list and current order counter.
        self.all_orders = []
        self.num_orders = 0
        self.current_order_index = 1
        
        # Start with the quantity selection frame.
        self.quantity_frame = tk.Frame(self.window)
        self.quantity_frame.pack(fill="both", expand=True)
        self.create_quantity_form(self.quantity_frame)
    
    def create_quantity_form(self, parent):
        # Update label based on meal type.
        meal_label = "breakfasts" if self.meal_type == 'breakfast' else "lunch orders"
        tk.Label(parent, text=f"How many {meal_label} would you like to order?", font=("Arial", 16)).pack(pady=20)
        self.quantity_entry = tk.Entry(parent, font=("Arial", 14))
        self.quantity_entry.pack(pady=10)
        tk.Button(parent, text="Next", command=self.start_orders, font=("Arial", 12)).pack(pady=10)
    
    def start_orders(self):
        try:
            self.num_orders = int(self.quantity_entry.get())
            if self.num_orders <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive integer for the number of orders.")
            return
        self.quantity_frame.pack_forget()
        self.create_order_form()  # Start with order #1
    
    def create_order_form(self):
        # If an order frame exists already, destroy it.
        if hasattr(self, 'order_frame'):
            self.order_frame.destroy()
        self.order_frame = tk.Frame(self.window)
        self.order_frame.pack(fill="both", expand=True)
        
        # Display current order number.
        header_text = f"Order #{self.current_order_index} of {self.num_orders}"
        tk.Label(self.order_frame, text=header_text, font=("Arial", 16)).pack(pady=10)
        
        form_frame = tk.Frame(self.order_frame)
        form_frame.pack(pady=10)
        
        # Order Size
        tk.Label(form_frame, text="Choose size (SML/MED/LRG):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.size_var = tk.StringVar(value="SML")
        sizes = ["SML", "MED", "LRG"]
        tk.OptionMenu(form_frame, self.size_var, *sizes).grid(row=0, column=1, padx=5, pady=5)
        
        # Dynamically generate Main Course options from today's menu.
        main_options = []
        # For breakfast, check Main 1-4; for lunch, Main 1-5.
        max_main = 4 if self.meal_type == 'breakfast' else 5
        for i in range(1, max_main + 1):
            option = self.day_menu.get(f"Main {i}")
            if option:
                main_options.append(option)
        if not main_options:
            main_options = ["No main options available"]
        tk.Label(form_frame, text="Select Main Course:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.main_var = tk.StringVar(value=main_options[0])
        tk.OptionMenu(form_frame, self.main_var, *main_options).grid(row=1, column=1, padx=5, pady=5)
        
        # Dynamically generate Side Dish options from today's menu.
        side_options = []
        max_side = 3 if self.meal_type == 'breakfast' else 5
        for i in range(1, max_side + 1):
            option = self.day_menu.get(f"Side {i}")
            if option:
                side_options.append(option)
        if not side_options:
            side_options = ["No side options available"]
        tk.Label(form_frame, text="Select Side Dish:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.side_var = tk.StringVar(value=side_options[0])
        tk.OptionMenu(form_frame, self.side_var, *side_options).grid(row=2, column=1, padx=5, pady=5)
        
        # Daily Special option text from today's menu.
        daily_special = self.day_menu.get("Daily Special", "No Daily Special")
        self.special_var = tk.IntVar()
        tk.Checkbutton(form_frame, text=f"Add Daily Special: {daily_special}", variable=self.special_var).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Customization entry
        tk.Label(form_frame, text="Customization:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.customization_entry = tk.Entry(form_frame)
        self.customization_entry.insert(0, "No customization")
        self.customization_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Dynamically generate Beverage options from today's menu.
        beverage_options = ["None"]
        max_beverage = 4  # Both meal types have 4 beverage columns
        for i in range(1, max_beverage + 1):
            bev = self.day_menu.get(f"Beverage {i}")
            if bev:
                beverage_options.append(bev)
        tk.Label(form_frame, text="Select Beverage:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.beverage_var = tk.StringVar(value=beverage_options[0] if beverage_options else "None")
        tk.OptionMenu(form_frame, self.beverage_var, *beverage_options).grid(row=5, column=1, padx=5, pady=5)
        
        # Add to favorites option
        self.add_to_favorites = tk.IntVar()
        tk.Checkbutton(form_frame, text="Add this order to favorites", variable=self.add_to_favorites).grid(row=6, column=0, columnspan=2, pady=5)
        
        # Confirm Order button
        tk.Button(self.order_frame, text="Confirm Order", command=self.confirm_order, font=("Arial", 12)).pack(pady=20)
    
    def confirm_order(self):
        # Collect order details.
        size = self.size_var.get().upper()
        main_course = self.main_var.get()
        side = self.side_var.get()
        daily_special = bool(self.special_var.get())
        customization = self.customization_entry.get()
        beverage = self.beverage_var.get() if self.beverage_var.get() != "None" else None
        
        # Use the dynamic daily special text if selected.
        special_text = self.day_menu.get("Daily Special") if daily_special else None
        
        order = {
            'size': size,
            'main': main_course,
            'side': side,
            'special': special_text,
            'customization': customization,
            'beverage': beverage,
            'add_to_favorites': bool(self.add_to_favorites.get())
        }
        self.all_orders.append(order)
        
        # Move to next order or summary.
        if self.current_order_index < self.num_orders:
            self.current_order_index += 1
            self.order_frame.destroy()
            self.create_order_form()
        else:
            self.order_frame.destroy()
            self.show_summary_view()
    
    def calculate_order_total(self, order):
        # Use pricing functions to calculate order total.
        main_cost = get_size_price(self.meal_type, order['size'])
        side_cost = get_side_price()
        special_cost = get_special_cost(self.meal_type) if order.get('special') else 0
        beverage_cost = get_beverage_price(self.meal_type, order['beverage']) if order.get('beverage') else 0
        return main_cost + side_cost + special_cost + beverage_cost
    
    def show_summary_view(self):
        self.summary_frame = tk.Frame(self.window)
        self.summary_frame.pack(fill="both", expand=True)
        
        summary_text = "-- Order Summary (Preview) --\n\n"
        overall_total = 0
        
        # Iterate over each order to show the details
        for idx, order in enumerate(self.all_orders, start=1):
            # Calculate individual item prices
            main_price = get_size_price(self.meal_type, order['size'])
            side_price = get_side_price()
            special_price = get_special_cost(self.meal_type) if order.get('special') else 0
            beverage_price = get_beverage_price(self.meal_type, order['beverage']) if order.get('beverage') else 0
            
            # Calculate subtotal
            subtotal = main_price + side_price + special_price + beverage_price
            overall_total += subtotal

            # Add order details to the summary text
            summary_text += f"Order #{idx}:\n"
            summary_text += f"  Main: {order['main']} ({order['size']}) - ${main_price:.2f}\n"
            summary_text += f"  Side: {order['side']} - ${side_price:.2f}\n"
            summary_text += f"  Daily Special: {order.get('special', 'None')} - ${special_price:.2f}\n"
            summary_text += f"  Customization: {order.get('customization', 'No customization')} - $0.00\n"
            summary_text += f"  Beverage: {order.get('beverage') or 'None'} - ${beverage_price:.2f}\n"
            summary_text += f"  -> Subtotal: ${subtotal:.2f}\n\n"
        
        summary_text += f"Overall Total: ${overall_total:.2f}\n"
        summary_text += "-- End of Summary --"
        
        # Display the summary
        tk.Label(self.summary_frame, text="Please review your order:", font=("Arial", 14)).pack(pady=10)
        text_box = tk.Text(self.summary_frame, wrap="word", font=("Arial", 12), height=15)
        text_box.insert("1.0", summary_text)
        text_box.config(state="disabled")
        text_box.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Buttons for proceeding with delivery or canceling the order
        btn_frame = tk.Frame(self.summary_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Proceed to Delivery/Pickup", command=self.show_delivery_options, font=("Arial", 12)).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Cancel Order", command=self.cancel_order, font=("Arial", 12)).grid(row=0, column=1, padx=10)
        
        # Save the overall total for payment processing.
        self.overall_total = overall_total


    # New method to show the delivery or pickup option.
    def show_delivery_options(self):
        # Ask the user for pickup or delivery choice.
        response = messagebox.askquestion("Delivery or Pickup", "Do you want delivery? (Yes for delivery, No for pickup)")
        
        if response == 'yes':
            # Open the delivery GUI window if the user chooses delivery.
            DeliveryWindow(self)
            
            # Set order_type to "delivery" for each order.
            for order in self.all_orders:
                order['order_type'] = 'delivery'
            
        else:
            # Directly move to payment if pickup is chosen.
            for order in self.all_orders:
                order['order_type'] = 'pickup'
            self.show_payment_view()

    def show_payment_view(self):
        self.summary_frame.pack_forget()
        self.payment_frame = tk.Frame(self.window)
        self.payment_frame.pack(fill="both", expand=True)
        
        tk.Label(self.payment_frame, text="Payment Options", font=("Arial", 16)).pack(pady=10)
        
        # Payment method selection.
        self.payment_method = tk.StringVar(value="Credit Card")
        method_frame = tk.Frame(self.payment_frame)
        method_frame.pack(pady=10)
        tk.Label(method_frame, text="Select Payment Method:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        tk.Radiobutton(method_frame, text="Credit Card", variable=self.payment_method, value="Credit Card", command=self.show_payment_fields, font=("Arial", 12)).grid(row=0, column=1, padx=5)
        tk.Radiobutton(method_frame, text="PayPal", variable=self.payment_method, value="PayPal", command=self.show_payment_fields, font=("Arial", 12)).grid(row=0, column=2, padx=5)
        
        # Container for payment details fields.
        self.payment_fields_frame = tk.Frame(self.payment_frame)
        self.payment_fields_frame.pack(pady=10)
        self.show_payment_fields()  # Display fields for default method.
        
        btn_frame = tk.Frame(self.payment_frame)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Confirm Payment", command=self.confirm_payment, font=("Arial", 12)).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Back", command=self.back_to_summary, font=("Arial", 12)).grid(row=0, column=1, padx=10)
    
    def show_payment_fields(self):
        for widget in self.payment_fields_frame.winfo_children():
            widget.destroy()
        method = self.payment_method.get()
        if method == "Credit Card":
            tk.Label(self.payment_fields_frame, text="Card Number:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
            self.card_number_entry = tk.Entry(self.payment_fields_frame, font=("Arial", 12))
            self.card_number_entry.grid(row=0, column=1, padx=5, pady=5)
            
            tk.Label(self.payment_fields_frame, text="Expiry (MM/YY):", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
            self.expiry_entry = tk.Entry(self.payment_fields_frame, font=("Arial", 12))
            self.expiry_entry.grid(row=1, column=1, padx=5, pady=5)
            
            tk.Label(self.payment_fields_frame, text="CVV:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
            self.cvv_entry = tk.Entry(self.payment_fields_frame, show="*", font=("Arial", 12))
            self.cvv_entry.grid(row=2, column=1, padx=5, pady=5)
        else:
            tk.Label(self.payment_fields_frame, text="PayPal Email:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
            self.paypal_email_entry = tk.Entry(self.payment_fields_frame, font=("Arial", 12))
            self.paypal_email_entry.grid(row=0, column=1, padx=5, pady=5)
    
    def confirm_payment(self):
        # Define a payment processor that uses fields from the payment view.
        def gui_payment_processor(total_cost):
            method = self.payment_method.get()
            if method == "Credit Card":
                card_number = self.card_number_entry.get()
                expiry = self.expiry_entry.get()
                cvv = self.cvv_entry.get()
                if not (card_number and expiry and cvv):
                    messagebox.showerror("Payment Error", "Please fill in all credit card details.")
                    return False
                return True
            else:
                paypal_email = self.paypal_email_entry.get()
                if not paypal_email:
                    messagebox.showerror("Payment Error", "Please enter your PayPal email.")
                    return False
                return True

        # Define a receipt callback to display the receipt on the GUI.
        def display_receipt(receipt_text):
            # Add orders marked for favorites.
            from OrderPlacement.favorites import addOrderToFaves
            for order in self.all_orders:
                if order.get('add_to_favorites'):
                    addOrderToFaves(order)

            self.payment_frame.pack_forget()
            self.receipt_frame = tk.Frame(self.window)
            self.receipt_frame.pack(fill="both", expand=True)
            tk.Label(self.receipt_frame, text="Receipt", font=("Arial", 16)).pack(pady=10)
            receipt_box = tk.Text(self.receipt_frame, wrap="word", font=("Courier", 10))
            receipt_box.insert("1.0", receipt_text)
            receipt_box.config(state="disabled")
            receipt_box.pack(fill="both", expand=True, padx=20, pady=20)
            tk.Button(self.receipt_frame, text="Back to Main Page", command=self.window.destroy, font=("Arial", 12)).pack(pady=10)

        success = gui_payment_processor(self.overall_total)
        if success:
            # Generate and display detailed receipt using receipt.py
            receipt_details = format_receipt(self.all_orders, self.meal_type)
            display_receipt(receipt_details)
        else:
            messagebox.showerror("Order", "Payment failed or order canceled.")
            self.window.destroy()
    
    def back_to_summary(self):
        self.payment_frame.pack_forget()
        self.summary_frame.pack(fill="both", expand=True)
    
    def cancel_order(self):
        messagebox.showinfo("Order", "Order canceled.")
        self.window.destroy()
