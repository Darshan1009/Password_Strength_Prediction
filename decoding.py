import os
import sqlite3

# Path to your database file (relative to this script)
db_path = os.path.join(os.path.dirname(__file__), 'Datasets', 'password_data.sqlite')

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Show all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables found in database:", tables)

# Loop through each table and display data
for table in tables:
    table_name = table[0]
    print(f"\nData from table '{table_name}':")
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Close the connection
conn.close()
