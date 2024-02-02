import customtkinter as ctk
from tkinter import ttk,messagebox
import csv
import tkinter as tk
from tkinter import ttk

def add_input_boxes():
    capital_label = tk.Label(stocks_frame, text="Capital:", bg="#121212", fg="white")
    capital_label.grid(row=row_count, column=0, padx=10, pady=5, sticky="w")
    capital_entry = tk.Entry(stocks_frame, bg="black", fg="white", relief="rounded")
    capital_entry.grid(row=row_count, column=1, padx=10, pady=5, sticky="w")
    capital_entries.append(capital_entry)

    stock_label = tk.Label(stocks_frame, text="Stock:", bg="#121212", fg="white")
    stock_label.grid(row=row_count, column=2, padx=10, pady=5, sticky="w")
    stock_entry = tk.Entry(stocks_frame, bg="black", fg="white", relief="rounded")
    stock_entry.grid(row=row_count, column=3, padx=10, pady=5, sticky="w")
    stock_entries.append(stock_entry)

    row_count += 1

# Create a function to save the input values to a CSV file
def save_to_csv():
    with open("stocks.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        for capital_entry, stock_entry in zip(capital_entries, stock_entries):
            capital = capital_entry.get()
            stock = stock_entry.get()
            if capital and stock:
                writer.writerow([capital, stock])
    clear_entries()

# Create a function to clear input entries
def clear_entries():
    for capital_entry, stock_entry in zip(capital_entries, stock_entries):
        capital_entry.delete(0, tk.END)
        stock_entry.delete(0, tk.END)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
root=ctk.CTk()

# Create a custom dark theme
style = ttk.Style()
style.configure("Dark.TFrame", background="#353535")
style.configure("Dark.TButton", background="blue", foreground="white", borderwidth=0, relief="flat")
style.map("Dark.TButton", background=[("active", "dark blue")])

root.geometry("850x500")
root.title("Stock Bot")
title_label=ctk.CTkLabel(root,text="Stock Bot",font=ctk.CTkFont(size=30,weight="bold"))
title_label.pack()

#root.configure(bg="#121212")
# Create a frame for the stocks section with a dark theme
stocks_frame = tk.Frame(root,bg="#353535")

stocks_frame.place(x=10, y=20, width=500, height=300)

# Create labels and entries for initial input
capital_label = tk.Label(stocks_frame, text="Capital:", bg="#353535", fg="white")
capital_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
capital_entry = tk.Entry(stocks_frame, bg="black", fg="white", relief="groove")
capital_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

stock_label = tk.Label(stocks_frame, text="Stock:", bg="#353535", fg="white")
stock_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
stock_entry = tk.Entry(stocks_frame, bg="black", fg="white", relief="groove")
stock_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")

# Create a button to add more input boxes
add_button = ttk.Button(stocks_frame, text="+", style="Round.TButton")

add_button.grid(row=0, column=4, padx=10, pady=5, sticky="w")

# Create a button to save input values to CSV
save_button = tk.Button(stocks_frame, text="Save", bg="#2196F3", fg="white", command=save_to_csv, relief="groove")
save_button.grid(row=1, column=0, columnspan=5, padx=10, pady=5)

# Initialize lists to store input entries
capital_entries = []
stock_entries = []

# Initialize row count for dynamic input boxes
row_count = 2

# Load saved stocks from the CSV file
try:
    with open("stocks.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                capital, stock = row
                capital_entry.insert(tk.END, capital)
                stock_entry.insert(tk.END, stock)
                add_input_boxes()  # Add input boxes dynamically
except FileNotFoundError:
    pass
root.mainloop()
