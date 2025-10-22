import sqlite3
import os

# Ensure folder exists
if not os.path.exists('models'):
    os.makedirs('models')

# Create or connect to database
conn = sqlite3.connect('models/database.db')
cursor = conn.cursor()

# Create table for users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Database initialized successfully at models/database.db")
