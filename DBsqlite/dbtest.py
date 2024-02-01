import sqlite3
import csv
import matplotlib.pyplot as plt
from datetime import datetime
# Connect to SQLite database
conn = sqlite3.connect('your_database.db')  # Replace with your actual database name
cursor = conn.cursor()

# Drop the Trades table if it exists
cursor.execute("DROP TABLE IF EXISTS Trades")
cursor.execute('''CREATE TABLE IF NOT EXISTS Trades (
  Event TEXT,
  side TEXT,
  symbol TEXT,
  quantity INT,
  price FLOAT,
  route TEXT,
  time TIME,
  account TEXT,
  note TEXT
)''') 

csv_file = 'csv/12-5-23 tradelog.csv'  # Replace with your actual CSV file path
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)

    # Insert data into the Trades table
    for row in csv_reader:
        cursor.execute('''
            INSERT INTO Trades (Event, side, symbol,quantity ,price , route, time, account, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row[0], row[1], row[2], int(row[3]), float(row[4]), row[5], row[6], row[7],row[8]))


# Commit changes and close the connection
conn.commit()
cursor.execute("SELECT time, price FROM Trades")
rows = cursor.fetchall()

# Separate the data into lists for plotting
times, prices = zip(*rows)
times = [datetime.strptime(time, '%H:%M:%S') for time in times]

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(times, prices, marker='o', linestyle='-')
plt.title('Trade Prices Over Time')
plt.xlabel('Time')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
conn.close()