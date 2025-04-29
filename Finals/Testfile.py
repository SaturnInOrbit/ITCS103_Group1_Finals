import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import openpyxl
from datetime import datetime

# Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Constants
ADMIN_USER = "admin"
ADMIN_PASS = "password"

# Global storage
inventory = []           # List of Product objects
sales = []               # List of (username, product, price, date)
users = {}               # username -> {"password": str, "history": list of purchases}
current_user = None      # Stores the currently logged-in username

# Product structure
class Product:
    def __init__(self, name, price, stock, image_path):
        self.name = name
        self.price = price
        self.stock = stock
        self.image_path = image_path

# Main App
class ECommerceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("E-Commerce System")
        self.geometry("1100x750")
        self.resizable(False, False)
        self.configure(bg="#1a1a1a")

        self.current_cart = []  # Stores cart items for current user
        self.login_screen()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- AUTHENTICATION SCREENS ---
    def login_screen(self):
        self.clear_widgets()

        frame = ctk.CTkFrame(self, fg_color="#262626")
        frame.pack(expand=True)

        title = ctk.CTkLabel(frame, text="Login", font=("Arial", 28), text_color="#b84dff")
        title.pack(pady=30)

        user_label = ctk.CTkLabel(frame, text="Username:")
        user_label.pack()
        self.login_username = ctk.CTkEntry(frame)
        self.login_username.pack(pady=(0, 10))

        pass_label = ctk.CTkLabel(frame, text="Password:")
        pass_label.pack()
        self.login_password = ctk.CTkEntry(frame, show="*")
        self.login_password.pack(pady=(0, 20))

        login_btn = ctk.CTkButton(frame, text="Login", command=self.verify_login)
        login_btn.pack(pady=10)

        register_btn = ctk.CTkButton(frame, text="Create Account", command=self.register_screen)
        register_btn.pack(pady=10)

    def register_screen(self):
        self.clear_widgets()

        frame = ctk.CTkFrame(self, fg_color="#262626")
        frame.pack(expand=True)

        title = ctk.CTkLabel(frame, text="Register", font=("Arial", 28), text_color="#00cc66")
        title.pack(pady=30)

        user_label = ctk.CTkLabel(frame, text="Username:")
        user_label.pack()
        self.reg_username = ctk.CTkEntry(frame)
        self.reg_username.pack(pady=(0, 10))

        pass_label = ctk.CTkLabel(frame, text="Password:")
        pass_label.pack()
        self.reg_password = ctk.CTkEntry(frame, show="*")
        self.reg_password.pack(pady=(0, 20))

        create_btn = ctk.CTkButton(frame, text="Create Account", command=self.create_account)
        create_btn.pack(pady=10)

        back_btn = ctk.CTkButton(frame, text="Back to Login", command=self.login_screen)
        back_btn.pack(pady=10)

    def create_account(self):
        username = self.reg_username.get()
        password = self.reg_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if username in users:
            messagebox.showerror("Error", "Username already exists.")
            return

        users[username] = {"password": password, "history": []}
        messagebox.showinfo("Success", "Account created. Please login.")
        self.login_screen()

    def verify_login(self):
        global current_user

        username = self.login_username.get()
        password = self.login_password.get()

        if username == ADMIN_USER and password == ADMIN_PASS:
            self.admin_dashboard()
        elif username in users and users[username]["password"] == password:
            current_user = username
            self.user_shop_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    # --- ADMIN DASHBOARD ---
    def admin_dashboard(self):
        self.clear_widgets()

        title = ctk.CTkLabel(self, text="Admin Dashboard", font=("Arial", 28), text_color="#ff9933")
        title.pack(pady=20)

        add_product_btn = ctk.CTkButton(self, text="Add Product", command=self.add_product_popup)
        add_product_btn.pack(pady=10)

        download_sales_btn = ctk.CTkButton(self, text="Download Sales Report", command=self.download_sales_report)
        download_sales_btn.pack(pady=10)

        logout_btn = ctk.CTkButton(self, text="Logout", command=self.login_screen)
        logout_btn.pack(pady=10)

        self.admin_frame = ctk.CTkFrame(self, fg_color="#262626", height=400, width=900)
        self.admin_frame.pack(pady=20)

        self.refresh_inventory()

    def refresh_inventory(self):
        for widget in self.admin_frame.winfo_children():
            widget.destroy()

        if not inventory:
            label = ctk.CTkLabel(self.admin_frame, text="No Products Yet.", text_color="gray")
            label.pack()
            return

        for idx, product in enumerate(inventory):
            frame = ctk.CTkFrame(self.admin_frame, fg_color="#333333", corner_radius=10)
            frame.grid(row=idx//2, column=idx%2, padx=10, pady=10, sticky="nsew")

            img = Image.open(product.image_path)
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(frame, image=img, text="")
            img_label.image = img
            img_label.pack()

            info = f"{product.name}\n₱{product.price:.2f}\nStock: {product.stock}"
            label = ctk.CTkLabel(frame, text=info)
            label.pack()

            edit_btn = ctk.CTkButton(frame, text="Edit Stock", command=lambda p=product: self.edit_stock_popup(p))
            edit_btn.pack(pady=2)

            delete_btn = ctk.CTkButton(frame, text="Delete", fg_color="red", hover_color="#cc0000", command=lambda p=product: self.delete_product(p))
            delete_btn.pack(pady=2)

    def add_product_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add Product")
        popup.geometry("300x400")
        popup.configure(bg="#1a1a1a")

        name_label = ctk.CTkLabel(popup, text="Product Name:")
        name_label.pack()
        name_entry = ctk.CTkEntry(popup)
        name_entry.pack()

        price_label = ctk.CTkLabel(popup, text="Price:")
        price_label.pack()
        price_entry = ctk.CTkEntry(popup)
        price_entry.pack()

        stock_label = ctk.CTkLabel(popup, text="Stock:")
        stock_label.pack()
        stock_entry = ctk.CTkEntry(popup)
        stock_entry.pack()

        image_btn = ctk.CTkButton(popup, text="Select Image", command=lambda: self.select_image(popup))
        image_btn.pack(pady=10)

        add_btn = ctk.CTkButton(popup, text="Add", command=lambda: self.save_product(name_entry.get(), price_entry.get(), stock_entry.get(), self.selected_image, popup))
        add_btn.pack(pady=10)

    def select_image(self, popup):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if path:
            self.selected_image = path
            messagebox.showinfo("Image Selected", "Image successfully selected.")

    def save_product(self, name, price, stock, image, popup):
        if not (name and price and stock and image):
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Price must be number. Stock must be integer.")
            return

        new_product = Product(name, price, stock, image)
        inventory.append(new_product)
        popup.destroy()
        self.refresh_inventory()

    def edit_stock_popup(self, product):
        popup = tk.Toplevel(self)
        popup.title("Edit Stock")
        popup.geometry("250x200")
        popup.configure(bg="#1a1a1a")

        label = ctk.CTkLabel(popup, text=f"Editing stock for {product.name}")
        label.pack(pady=10)

        stock_entry = ctk.CTkEntry(popup)
        stock_entry.pack()

        save_btn = ctk.CTkButton(popup, text="Save", command=lambda: self.save_stock(product, stock_entry.get(), popup))
        save_btn.pack(pady=10)

    def save_stock(self, product, stock, popup):
        try:
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Error", "Stock must be an integer.")
            return

        product.stock = stock
        popup.destroy()
        self.refresh_inventory()

    def delete_product(self, product):
        if messagebox.askyesno("Delete", f"Are you sure you want to delete {product.name}?"):
            inventory.remove(product)
            self.refresh_inventory()

    def download_sales_report(self):
        if not sales:
            messagebox.showerror("Error", "No sales to report.")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

        if not filepath:
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sales Report"

        headers = ["Username", "Product", "Price", "Date"]
        ws.append(headers)

        for sale in sales:
            ws.append(sale)

        wb.save(filepath)
        messagebox.showinfo("Success", f"Sales report saved to {filepath}.")

    # --- USER SCREENS ---
    def user_shop_screen(self):
        self.clear_widgets()

        title = ctk.CTkLabel(self, text="Welcome to the Shop", font=("Arial", 28), text_color="#b84dff")
        title.pack(pady=20)

        self.refresh_user_shop()

        logout_btn = ctk.CTkButton(self, text="Logout", command=self.login_screen)
        logout_btn.pack(pady=10)

    def refresh_user_shop(self):
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        if not inventory:
            label = ctk.CTkLabel(self, text="No Products Available.", text_color="gray")
            label.pack(pady=10)
            return

        for idx, product in enumerate(inventory):
            frame = ctk.CTkFrame(self, fg_color="#333333", corner_radius=10)
            frame.pack(padx=20, pady=10, fill="x", anchor="w")

            img = Image.open(product.image_path)
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(frame, image=img, text="")
            img_label.image = img
            img_label.pack(side="left")

            info = f"{product.name}\n₱{product.price:.2f}\nStock: {product.stock}"
            label = ctk.CTkLabel(frame, text=info)
            label.pack(side="left", padx=10)

            add_to_cart_btn = ctk.CTkButton(frame, text="Add to Cart", command=lambda p=product: self.add_to_cart(p))
            add_to_cart_btn.pack(side="right", padx=10)

    def add_to_cart(self, product):
        if product.stock == 0:
            messagebox.showerror("Out of Stock", f"Sorry, {product.name} is out of stock.")
            return

        self.current_cart.append(product)
        product.stock -= 1
        messagebox.showinfo("Added to Cart", f"{product.name} has been added to your cart.")

        self.refresh_user_shop()

if __name__ == "__main__":
    app = ECommerceApp()
    app.mainloop()
