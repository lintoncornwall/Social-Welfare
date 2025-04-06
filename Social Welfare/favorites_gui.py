#favorites_gui.py
import tkinter as tk
from tkinter import messagebox
import json
import os

class FavoritesWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Favorite Orders")
        self.window.geometry("500x400")
        
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
        selected = self.favorites_listbox.curselection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a favorite order.")
            return
        index = selected[0]
        favorite_order = self.favorites[index]
        confirm = messagebox.askyesno("Confirm Order", f"Place order for {favorite_order.get('main', 'N/A')} with {favorite_order.get('side', 'N/A')}?")
        if confirm:
            messagebox.showinfo("Order", "Favorite order placed successfully!")
            self.window.destroy()
    
    def delete_selected(self):
        selected = self.favorites_listbox.curselection()
        if not selected:
            messagebox.showwarning("Selection", "Select a favorite order to delete.")
            return
        index = selected[0]
        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete the selected favorite order?")
        if confirm:
            del self.favorites[index]
            with open("favorites.json", "w") as f:
                json.dump(self.favorites, f, indent=4)
            self.load_favorites()
            messagebox.showinfo("Delete", "Favorite order deleted.")
