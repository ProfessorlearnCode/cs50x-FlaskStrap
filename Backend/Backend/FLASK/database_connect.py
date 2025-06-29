import sqlite3
import os

# Specify the path to your database file
db_path = 'backend/instance/database.db'  # Adjust the path if necessary

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to select all data from a specific table
cursor.execute("SELECT * FROM your_table_name")  # Replace with your table name

# Fetch and print results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
