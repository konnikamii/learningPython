import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime


class TradingJournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Journal App")

        # Initialize variables
        self.symbol_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.date_var = tk.StringVar()

        # Create labels and entry widgets
        tk.Label(root, text="Symbol:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.symbol_var).grid(
            row=0, column=1, padx=10, pady=10
        )

        tk.Label(root, text="Quantity:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.quantity_var).grid(
            row=1, column=1, padx=10, pady=10
        )

        tk.Label(root, text="Price:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.price_var).grid(
            row=2, column=1, padx=10, pady=10
        )

        tk.Label(root, text="Date (YYYY-MM-DD):").grid(
            row=3, column=0, padx=10, pady=10
        )
        tk.Entry(root, textvariable=self.date_var).grid(
            row=3, column=1, padx=10, pady=10
        )

        # Create buttons
        tk.Button(root, text="Add Trade", command=self.add_trade).grid(
            row=4, column=0, columnspan=2, pady=10
        )
        tk.Button(root, text="Show Trades", command=self.show_trades).grid(
            row=5, column=0, columnspan=2, pady=10
        )

    def add_trade(self):
        symbol = self.symbol_var.get()
        quantity = self.quantity_var.get()
        price = self.price_var.get()
        date = self.date_var.get()

        if not all([symbol, quantity, price, date]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            datetime.strptime(date, "%Y-%m-%d")  # Validate date format
        except ValueError:
            messagebox.showerror("Error", "Invalid input for quantity, price, or date.")
            return

        # Append the trade to a CSV file
        with open("trades.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([symbol, quantity, price, date])

        messagebox.showinfo("Success", "Trade added successfully!")

    def show_trades(self):
        try:
            with open("trades.csv", mode="r") as file:
                reader = csv.reader(file)
                trades = list(reader)

            if not trades:
                messagebox.showinfo("No Trades", "No trades recorded yet.")
            else:
                trades_str = "\n".join([", ".join(trade) for trade in trades])
                messagebox.showinfo("Trades", trades_str)

        except FileNotFoundError:
            messagebox.showinfo("No Trades", "No trades recorded yet.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TradingJournalApp(root)
    root.mainloop()
