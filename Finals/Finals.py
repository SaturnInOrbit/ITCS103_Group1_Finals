import customtkinter as ctk

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")  # Options: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("green")  # You can change it to "green" or "dark-blue"

# Create the main application window
app = ctk.CTk()
app.title("Patient Login Record - Hospital System")
app.geometry("400x400")
app.resizable(False, False)

# Title Label
title_label = ctk.CTkLabel(app, text="Patient Login", font=ctk.CTkFont(size=24, weight="bold"))
title_label.pack(pady=20)

# Username Entry
username_label = ctk.CTkLabel(app, text="Username (Patient ID):", anchor="w")
username_label.pack(fill="x", padx=40, pady=(10, 0))

username_entry = ctk.CTkEntry(app, placeholder_text="Enter your patient ID")
username_entry.pack(fill="x", padx=40, pady=10)

# Password Entry
password_label = ctk.CTkLabel(app, text="Password:", anchor="w")
password_label.pack(fill="x", padx=40, pady=(10, 0))

password_entry = ctk.CTkEntry(app, placeholder_text="Enter your password", show="*")
password_entry.pack(fill="x", padx=40, pady=10)

# Login Button
login_button = ctk.CTkButton(app, text="Login", fg_color='#008000')
login_button.pack(pady=20)

# Footer/Info Label
info_label = ctk.CTkLabel(app, text="Login to view your previous registrations.", font=ctk.CTkFont(size=12))
info_label.pack(pady=10)

# Start the application
app.mainloop()
