import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO
import requests

class RestaurantOrderManagement:
    
    def __init__(self, root):
        self.root=root
        self.root.title("Restaurant Order Management")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        
        self.menu_items={
            "FRIES MEAL": 2.00,
            "LUNCH MEAL": 2.00,
            "BURGER MEAL": 3.00,
            "PIZZA MEAL": 4.00,
            "CHEESE BURGER": 2.50,
            "DRINKS": 1.00
        }
        
        self.exchange_rate=90
        
        self.setup_background()
        
        self.frame=ttk.Frame(root, padding=15)
        self.frame.place(
            relx=0.5, rely=0.5, anchor=tk.CENTER
        )
        
        ttk.Label(
            self.frame,
            text="Restaurant Order Management",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)
        
        
        self.menu_labels={}
        self.menu_quantities={}
        
        for row, (item, price) in enumerate(
            self.menu_items.items(), start=1
        ):
            label=ttk.Label(
                self.frame,
                text=f"{item} (${price:.2f})",
                font=("Arial", 11)
            )
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            self.menu_labels[item]=label
            entry=ttk.Entry(self.frame, width=10)
            entry.grid(row=row, column=1, padx=10, pady=5)
            
            self.menu_quantities[item]=entry
            
        ttk.Label(
            self.frame, text="Currency:"
        ).grid(row=7, column=0, pady=10)
        
        self.currency_var=tk.StringVar(value="USD")
        
        currency_dropdown=ttk.Combobox(
            self.frame,
            textvariable=self.currency_var,
            values=("USD", "INR"),
            state="readonly",
            width=10
        )
        currency_dropdown.grid(row=7, column=1, pady=10)
        
        self.currency_var.trace_add(
            "write", self.update_menu_prices
        )
        
        
        ttk.Button(
            self.frame,
            text="place order",
            command=self.place_order
        ).grid(row=9, column=0, columnspan=2, pady=15)
        
        
        ttk.Button(
            self.frame,
            text="clear order",
            command=self.clear_order
        ).grid(row=10, column=0, columnspan=2, pady=5)
        
        
    def setup_background(self):
        image_url=(
            "https://images.unsplash.com/"

            "photo-1517248135467-4c7edcad34c4"

            "?auto=format&fit=crop&w=800&q=80"
        )
        
        
        try:
            response=requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            image=Image.open(BytesIO(response.content))
            image=image.convert("RGB")
            image=image.resize((800, 600))
            
            self.background_image=ImageTk.PhotoImage(image)
            
            background_label=tk.Label(
                self.root,
                image=self.background_image
            )
            
            background_label.place(
                x=0, y=0, relwidth=1, relheight=1
            )
            
            background_label.lower()
            
        except Exception as e:
            self.root.configure(bg="#f5e6d3")
            print("Background image unavailable:", e)
            
    def update_menu_prices(self, *args):
        
        currency=self.currency_var.get()
        
        symbol="₹" if currency=="INR" else"$"
        rate=self.exchange_rate if currency=="INR" else 1
        
        for item, label in self.menu_labels.items():
            
            price=self.menu_items[item]*rate
            
            label.config(
                text=f"{item} ({symbol}{price:.2f}):"
            )
    def place_order(self):
        
        total_cost=0
        order_summary="ORDER SUMMARY\n\n"
        
        currency=self.currency_var.get()
        symbol="₹" if currency=="INR" else "$"
        rate=self.exchange_rate if currency=="INR" else 1
        
        for item, entry in self.menu_quantities.items():
            
            quantity_text=entry.get().strip()
            
            if not quantity_text.isdigit():
                messagebox.showerror(
                    "invalid quantity",
                    f"Enter a valid quantity for {item}."
                )
                return
            quantity=int(quantity_text)
            
            price=self.menu_items[item] * rate
            cost=quantity*price
            
            total_cost+=cost
            
            if quantity>0:
                order_summary+=(
                    f"{item}: {quantity} x "
                    f"{symbol}{price:.2f}="
                    f"{symbol}{cost:.2f}\n"
                )
                
        if total_cost > 0:
            
            order_summary+=(
                f"\nTotal cost: {symbol}{total_cost:.2f}"
            )
            
            messagebox.showinfo(
                "Order place successfully",
                order_summary
            )
            
        else:
            messagebox.showerror(
                "Error",
                "please order at least one item."
            )
            
    def clear_order(self):
        
        for entry in self.menu_quantities.values():
            entry.delete(0, tk.END)
            
        messagebox.showinfo(
            "Order Cleared",
            "All quantities have been cleared."
        )
        
if __name__ =="__main__":
    
    root=tk.Tk()
    
    app=RestaurantOrderManagement(root)
    
    root.mainloop()
                
            
                
            