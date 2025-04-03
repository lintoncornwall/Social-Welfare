
import tkinter as tk
from tkinter import ttk, messagebox

# Dummy pricing data
PRICING = {
    "Kidney": 700.00,
    "Stewed Chicken": 650.00,
    "Callaloo & Saltfish": 600.00,
    "Ackee & Saltfish": 680.00,
    "Daily Special": 500.00,
    "Soda": 150.00,
    "Fruit Juice": 250.00,
    "Iced Tea": 200.00,
    "Water": 100.00
}

# Main Application GUI
class OnlineOrderingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Ordering System")
        self.geometry("800x600")
        self.show_main_menu()
    
    def show_main_menu(self):
        self.clear_window()
        
        tk.Label(self, text="Welcome to Our Online Ordering System", font=("Arial", 18)).pack(pady=20)
        
        # Main menu options
        make_order_button = tk.Button(self, text="Make Order", font=("Arial", 14), command=self.launch_order_wizard)
        make_order_button.pack(pady=5)
        
        fav_orders_button = tk.Button(self, text="View Favorite Orders", font=("Arial", 14), command=self.view_favorite_orders)
        fav_orders_button.pack(pady=5)
        
        refund_button = tk.Button(self, text="Request Refund", font=("Arial", 14), command=self.request_refund)
        refund_button.pack(pady=5)
        
        cancel_delivery_button = tk.Button(self, text="Cancel Delivery", font=("Arial", 14), command=self.cancel_delivery)
        cancel_delivery_button.pack(pady=5)
        
        edit_content_button = tk.Button(self, text="Edit Content", font=("Arial", 14), command=self.open_content_editor)
        edit_content_button.pack(pady=5)
        
        exit_button = tk.Button(self, text="Exit", font=("Arial", 14), command=self.quit)
        exit_button.pack(pady=5)
    
    def launch_order_wizard(self):
        self.clear_window()
        self.order_wizard = OrderWizard(self, self.show_main_menu)
        self.order_wizard.pack(expand=True, fill='both')
    
    def view_favorite_orders(self):
        messagebox.showinfo("Favorites", "This feature is not implemented yet.")
    
    def request_refund(self):
        messagebox.showinfo("Refund", "Refund request has been submitted.")
    
    def cancel_delivery(self):
        messagebox.showinfo("Cancel Delivery", "Your delivery has been cancelled.")
    
    def open_content_editor(self):
        editor = tk.Toplevel(self)
        editor.title("Content Editor")
        tk.Label(editor, text="Content Editor (Admin)", font=("Arial", 16)).pack(padx=10, pady=10)
        tk.Button(editor, text="Close", command=editor.destroy).pack(pady=5)
    
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

# OrderWizard is a multi-step ordering process.
class OrderWizard(tk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master)
        self.return_callback = return_callback
        self.order_data = {}  # Store choices here
        self.current_step = 0
        self.steps = [
            self.step_order_count,
            self.step_order_size,
            self.step_main_course,
            self.step_side_dish,
            self.step_daily_special,
            self.step_customize,
            self.step_beverage,
            self.step_order_summary,
            self.step_order_confirmation,
            self.step_favorites,
            self.step_delivery_option,
            self.step_receipt
        ]
        self.setup_step_container()
        self.show_current_step()
    
    def setup_step_container(self):
        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill='both')
    
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()
    
    def show_current_step(self):
        self.clear_container()
        # Call the current step method
        self.steps[self.current_step]()
    
    def next_step(self):
        self.current_step += 1
        if self.current_step < len(self.steps):
            self.show_current_step()
        else:
            # Finished the wizard, return to main menu.
            self.return_callback()
    
    def step_order_count(self):
        # Step: Ask how many lunch orders (for now, we assume 1 order)
        tk.Label(self.container, text="It's lunch time!\nHow many lunch orders would you like?", font=("Arial", 16)).pack(pady=20)
        self.order_count_entry = tk.Entry(self.container, font=("Arial", 14))
        self.order_count_entry.pack(pady=10)
        self.order_count_entry.insert(0, "1")
        tk.Button(self.container, text="Next", font=("Arial", 14), command=self.handle_order_count).pack(pady=10)
    
    def handle_order_count(self):
        try:
            count = int(self.order_count_entry.get())
            if count < 1:
                raise ValueError
            self.order_data["order_count"] = count
            # For simplicity, we'll handle one order only.
            self.order_data["current_order"] = 1
            self.next_step()
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number (>=1).")
    
    def step_order_size(self):
        tk.Label(self.container, text="Order #1:\nChoose size (SML/MED/LRG):", font=("Arial", 16)).pack(pady=20)
        self.size_var = tk.StringVar(value="SML")
        sizes = [("SML", "SML"), ("MED", "MED"), ("LRG", "LRG")]
        for text, mode in sizes:
            tk.Radiobutton(self.container, text=text, variable=self.size_var, value=mode, font=("Arial", 14)).pack(pady=5)
        tk.Button(self.container, text="Next", font=("Arial", 14), command=self.handle_order_size).pack(pady=10)
    
    def handle_order_size(self):
        self.order_data["size"] = self.size_var.get()
        self.next_step()
    
    def step_main_course(self):
        tk.Label(self.container, text="Available meals for Wednesday:\nMain options:", font=("Arial", 16)).pack(pady=20)
        self.main_options = ["Kidney", "Stewed Chicken", "Callaloo & Saltfish", "Ackee & Saltfish"]
        self.main_var = tk.StringVar(value=self.main_options[0])
        for idx, meal in enumerate(self.main_options, start=1):
            tk.Radiobutton(self.container, text=f"{idx}. {meal}", variable=self.main_var, value=meal, font=("Arial", 14)).pack(pady=2)
        tk.Button(self.container, text="Next", font=("Arial", 14), command=self.handle_main_course).pack(pady=10)
    
    def handle_main_course(self):
        self.order_data["main_course"] = self.main_var.get()
        self.next_step()
    
    def step_side_dish(self):
        tk.Label(self.container, text="Side options:", font=("Arial", 16)).pack(pady=20)
        self.side_options = ["Boiled food", "Fried Dumplings", "Breadfruit & Plantain"]
        self.side_var = tk.StringVar(value=self.side_options[0])
        for idx, side in enumerate(self.side_options, start=1):
            tk.Radiobutton(self.container, text=f"{idx}. {side}", variable=self.side_var, value=side, font=("Arial", 14)).pack(pady=2)
        tk.Button(self.container, text="Next", font=("Arial", 14), command=self.handle_side_dish).pack(pady=10)
    
    def handle_side_dish(self):
        self.order_data["side_dish"] = self.side_var.get()
        self.next_step()
    
    def step_daily_special(self):
        tk.Label(self.container, text="Would you like the Daily Special: Oatmeal porridge?", font=("Arial", 16)).pack(pady=20)
        self.daily_special_var = tk.StringVar(value="y")
        options = [("Yes", "y"), ("No", "n")]
        for text, value in options:
            tk.Radiobutton(self.container, text=text, variable=self.daily_special_var, value=value, font=("Arial", 14)).pack(pady=5)
        tk.Button(self.container, text="Next", font=("Arial", 14), command=self.handle_daily_special).pack(pady=10)
    
    def handle_daily_special(self):
        self.order_data["daily_special"] = "Oatmeal porridge" if self.daily_special_var.get() == "y" else "None"
        self.next_step()
    
    def step_customize(self):
        # Ask for customization only if main course is Kidney
        if self.order_data.get("main_course") == "Kidney":
            tk.Label(self.container, text="Do you want to customize your Kidney meal?", font=("Arial", 16)).pack(pady=20)
            self.customize_var = tk.StringVar(value="n")
            options = [("Yes", "y"), ("No", "n")]
            for text, value in options:
                tk.Radiobutton(self.container, text=text, variable=self.customize_var, value=value, font=("Arial", 14)).pack(pady=5)
            tk.Button(self.container, text="Next", font=("Arial", 14), command=self.handle_customize).pack(pady=10)
        else:
            self.order_data["customization"] = "No customization"
            self.next_step()
    
    def handle_customize(self):
        self.order_data["customization"] = "Customized" if self.customize_var.get() == "y" else "No customization"
        self.next_step()
    
    def step_beverage(self):
        tk.Label(self.container, text="Available Beverages:", font=("Arial", 16)).pack(pady=20)
        self.beverages = [("1. Soda - $150", "Soda"),
                          ("2. Fruit Juice - $250", "Fruit Juice"),
                          ("3. Iced Tea - $200", "Iced Tea"),
                          ("4. Water - $100", "Water"),
                          ("0. None", "None")]
        self.beverage_var = tk.StringVar(value="None")
        for text, bev in self.beverages:
            tk.Radiobutton(self.container, text=text, variable=self.beverage_var, value=bev, font=("Arial", 14)).pack(pady=2)
        tk.Button(self.container, text="Next", font=("Arial", 14), command=self.handle_beverage).pack(pady=10)
    
    def handle_beverage(self):
        self.order_data["beverage"] = self.beverage_var.get()
        self.next_step()
    
    def step_order_summary(self):
        # Build summary text from order_data
        summary = f"Your order details:\n\n"
        summary += f"Main Course: {self.order_data.get('main_course')}\n"
        summary += f"Side Dish: {self.order_data.get('side_dish')}\n"
        summary += f"Daily Special: {self.order_data.get('daily_special')}\n"
        summary += f"Customization: {self.order_data.get('customization', 'No customization')}\n"
        summary += f"Beverage: {self.order_data.get('beverage')}\n\n"
        tk.Label(self.container, text=summary, font=("Arial", 14), justify="left").pack(pady=20)
        tk.Label(self.container, text="Is your order correct? (y/n)", font=("Arial", 16)).pack(pady=10)
        self.correct_var = tk.StringVar(value="y")
        options = [("Yes", "y"), ("No", "n")]
        for text, value in options:
            tk.Radiobutton(self.container, text=text, variable=self.correct_var, value=value, font=("Arial", 14)).pack(pady=2)
        tk.Button(self.container, text="Next", font=("Arial", 14), command=self.handle_order_summary).pack(pady=10)
    
    def handle_order_summary(self):
        if self.correct_var.get() != "y":
            messagebox.showinfo("Order", "Please restart the order process to make changes.")
            self.return_callback()
        else:
            self.next_step()
    
    def step_order_confirmation(self):
        tk.Label(self.container, text="Do you want to confirm this order? (y/n)", font=("Arial", 16)).pack(pady=20)
        self.confirm_var = tk.StringVar(value="y")
        options = [("Yes", "y"), ("No", "n")]
        for text, value in options:
            tk.Radiobutton(self.container, text=text, variable=self.confirm_var, value=value, font=("Arial", 14)).pack(pady=5)
        tk.Button(self.container, text="Next", font=("Arial", 14), command=self.handle_order_confirmation).pack(pady=10)
    
    def handle_order_confirmation(self):
        if self.confirm_var.get() != "y":
            messagebox.showinfo("Order", "Order not confirmed. Returning to main menu.")
            self.return_callback()
        else:
            self.next_step()
    
    def step_favorites(self):
        tk.Label(self.container, text="Would you like to add this order to your favorites? (y/n)", font=("Arial", 16)).pack(pady=20)
        self.fav_var = tk.StringVar(value="n")
        options = [("Yes", "y"), ("No", "n")]
        for text, value in options:
            tk.Radiobutton(self.container, text=text, variable=self.fav_var, value=value, font=("Arial", 14)).pack(pady=5)
        tk.Button(self.container, text="Next", font=("Arial", 14), command=self.handle_favorites).pack(pady=10)
    
    def handle_favorites(self):
        self.order_data["favorite"] = "Yes" if self.fav_var.get() == "y" else "No"
        self.next_step()
    
    def step_delivery_option(self):
        tk.Label(self.container, text="Would you like delivery or pickup?", font=("Arial", 16)).pack(pady=20)
        self.delivery_var = tk.StringVar(value="pickup")
        options = [("Delivery", "delivery"), ("Pickup", "pickup")]
        for text, value in options:
            tk.Radiobutton(self.container, text=text, variable=self.delivery_var, value=value, font=("Arial", 14)).pack(pady=5)
        tk.Button(self.container, text="Next", font=("Arial", 14), command=self.handle_delivery_option).pack(pady=10)
    
    def handle_delivery_option(self):
        self.order_data["delivery_option"] = self.delivery_var.get()
        self.next_step()
    
    def step_receipt(self):
        # Calculate prices
        main_price = PRICING.get(self.order_data.get("main_course"), 0)
        daily_price = PRICING["Daily Special"] if self.order_data.get("daily_special") != "None" else 0
        beverage_choice = self.order_data.get("beverage")
        bev_price = PRICING.get(beverage_choice, 0) if beverage_choice != "None" else 0
        total = main_price + daily_price + bev_price  # Side dish and customization assumed free
        
        receipt_text = "---- Order Receipt ----\n"
        receipt_text += "Receipt Number: 00000006\n\n"
        receipt_text += "Order #1:\n"
        receipt_text += f"Main Course ({self.order_data.get('size')}): {self.order_data.get('main_course'):20} ${main_price:7.2f}\n"
        receipt_text += f"Side Dish: {self.order_data.get('side_dish'):30} $0.00\n"
        receipt_text += f"Daily Special: {self.order_data.get('daily_special'):20} ${daily_price:7.2f}\n"
        receipt_text += f"Customization: {self.order_data.get('customization'):20} $0.00\n"
        receipt_text += f"Beverage: {beverage_choice:25} ${bev_price:7.2f}\n"
        receipt_text += f"Order Total: {'':35} ${total:7.2f}\n\n"
        receipt_text += "--------------------------------------------------\n"
        receipt_text += f"{'Total:':35} ${total:7.2f}\n"
        receipt_text += "--------------------------------------------------\n\n"
        receipt_text += "---- Thank You! ----"
        
        self.clear_container()
        tk.Label(self.container, text=receipt_text, font=("Courier", 12), justify="left").pack(pady=20)
        tk.Button(self.container, text="Finish", font=("Arial", 14), command=self.return_callback).pack(pady=10)

if __name__ == "__main__":
    app = OnlineOrderingApp()
    app.mainloop()
