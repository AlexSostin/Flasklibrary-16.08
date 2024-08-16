import sqlite3
from datetime import date

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create the books table with an additional image_url column
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    publication_year INTEGER,
    isbn TEXT,
    available_copies INTEGER DEFAULT 1,
    image_url TEXT
)
''')

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone_number TEXT,
    membership_date DATE
)
''')

# Create the loan table
cursor.execute('''
CREATE TABLE IF NOT EXISTS loan (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    user_id INTEGER,
    loan_date DATE,
    return_date DATE,
    status TEXT DEFAULT 'borrowed',
    FOREIGN KEY (book_id) REFERENCES books (book_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
''')

# Insert sample data into the books table with image URLs from Wikipedia
cursor.executemany('''
INSERT INTO books (title, author, genre, publication_year, isbn, available_copies, image_url)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', [
    ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1925, "9780743273565", 3, "https://upload.wikimedia.org/wikipedia/commons/7/7a/The_Great_Gatsby_Cover_1925_Retouched.jpg"),
    ("1984", "George Orwell", "Dystopian", 1949, "9780451524935", 5, "https://upload.wikimedia.org/wikipedia/commons/c/c3/1984first.jpg"),
    ("To Kill a Mockingbird", "Harper Lee", "Classic", 1960, "9780061120084", 2, "https://upload.wikimedia.org/wikipedia/commons/4/4f/To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg")
])

# Insert sample data into the users table
cursor.executemany('''
INSERT INTO users (name, email, phone_number, membership_date)
VALUES (?, ?, ?, ?)
''', [
    ("Alice Johnson", "alice.johnson@example.com", "555-1234", date(2023, 5, 10)),
    ("Bob Smith", "bob.smith@example.com", "555-5678", date(2022, 8, 15)),
    ("Charlie Brown", "charlie.brown@example.com", "555-9101", date(2024, 1, 5))
])

# Insert sample data into the loan table
cursor.executemany('''
INSERT INTO loan (book_id, user_id, loan_date, return_date, status)
VALUES (?, ?, ?, ?, ?)
''', [
    (1, 1, date(2024, 7, 15), None, 'borrowed'),
    (2, 2, date(2024, 8, 1), date(2024, 8, 10), 'returned'),
    (3, 3, date(2024, 8, 5), None, 'borrowed')
])

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created and sample data inserted successfully with book images.")
