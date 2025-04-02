import tkinter as tk
from tkinter import ttk, messagebox

class OnlineOrderingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Ordering System")
        self.geometry("800x600")
        self.show_main_menu()
    
    def show_main_menu(self):
        self.clear_window()
        
        tk.Label(self, text="Welcome to Our Online Ordering System", font=("Arial", 18)).pack(pady=20)
        
        start_order_button = tk.Button(self, text="Start Order", font=("Arial", 14), command=self.show_ordering_interface)
        start_order_button.pack(pady=10)
        
        admin_panel_button = tk.Button(self, text="Admin Panel", font=("Arial", 14), command=self.open_content_editor)
        admin_panel_button.pack(pady=10)
        
        exit_button = tk.Button(self, text="Exit", font=("Arial", 14), command=self.quit)
        exit_button.pack(pady=10)
    
    def show_ordering_interface(self):
        self.clear_window()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')
        
        self.create_menu_tab()
        self.create_favorites_tab()
        self.create_order_tab()
        self.create_delivery_tab()
        self.create_receipt_tab()
        
        back_button = tk.Button(self, text="Back to Main Menu", command=self.show_main_menu)
        back_button.pack(pady=10)
    
    def create_menu_tab(self):
        menu_frame = ttk.Frame(self.notebook)
        self.notebook.add(menu_frame, text="Menu")
        tk.Label(menu_frame, text="Available Menu Items", font=("Arial", 16)).pack(pady=10)
    
    def create_favorites_tab(self):
        fav_frame = ttk.Frame(self.notebook)
        self.notebook.add(fav_frame, text="Favorites")
        tk.Label(fav_frame, text="Favorite Items", font=("Arial", 16)).pack(pady=10)
    
    def create_order_tab(self):
        order_frame = ttk.Frame(self.notebook)
        self.notebook.add(order_frame, text="Order")
        tk.Label(order_frame, text="Your Order", font=("Arial", 16)).pack(pady=10)
    
    def create_delivery_tab(self):
        delivery_frame = ttk.Frame(self.notebook)
        self.notebook.add(delivery_frame, text="Delivery")
        tk.Label(delivery_frame, text="Enter Delivery Information", font=("Arial", 16)).pack(pady=10)
    
    def create_receipt_tab(self):
        receipt_frame = ttk.Frame(self.notebook)
        self.notebook.add(receipt_frame, text="Receipt")
        tk.Label(receipt_frame, text="Order Receipt", font=("Arial", 16)).pack(pady=10)
    
    def open_content_editor(self):
        editor = tk.Toplevel()
        editor.title("Content Editor")
        tk.Label(editor, text="Content Editor (Admin)").pack(padx=10, pady=10)
        tk.Button(editor, text="Close", command=editor.destroy).pack(pady=5)
    
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = OnlineOrderingApp()
    app.mainloop()