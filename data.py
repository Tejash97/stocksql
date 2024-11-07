import sqlite3

# Connect to SQLite (it will create the database if it doesn't exist)
connection = sqlite3.connect("tejash_tshirts.db")
cursor = connection.cursor()

# Create the t_shirts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS t_shirts (
    t_shirt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT CHECK(brand IN ('Van Huesen', 'Levi', 'Nike', 'Adidas')),
    color TEXT CHECK(color IN ('Red', 'Blue', 'Black', 'White')),
    size TEXT CHECK(size IN ('XS', 'S', 'M', 'L', 'XL')),
    price INTEGER CHECK(price BETWEEN 10 AND 50),
    stock_quantity INTEGER,
    UNIQUE(brand, color, size)
);
''')

# Create the discounts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS discounts (
    discount_id INTEGER PRIMARY KEY AUTOINCREMENT,
    t_shirt_id INTEGER,
    pct_discount REAL CHECK(pct_discount BETWEEN 0 AND 100),
    FOREIGN KEY (t_shirt_id) REFERENCES t_shirts(t_shirt_id)
);
''')

# Insert some sample data into t_shirts table
t_shirts_data = [
    ('Van Huesen', 'Red', 'M', 30, 100),
    ('Levi', 'Blue', 'L', 40, 200),
    ('Nike', 'Black', 'S', 25, 150),
    ('Adidas', 'White', 'XL', 45, 120),
    ('Van Huesen', 'Black', 'M', 35, 80),
    ('Levi', 'Red', 'S', 28, 90),
    ('Nike', 'Blue', 'L', 38, 60),
    ('Adidas', 'Black', 'M', 40, 110)
]

cursor.executemany('''
INSERT OR IGNORE INTO t_shirts (brand, color, size, price, stock_quantity)
VALUES (?, ?, ?, ?, ?);
''', t_shirts_data)

# Insert some sample data into discounts table
discounts_data = [
    (1, 10.00),
    (2, 15.00),
    (3, 20.00),
    (4, 5.00),
    (5, 25.00),
    (6, 10.00),
    (7, 30.00),
    (8, 35.00)
]

cursor.executemany('''
INSERT INTO discounts (t_shirt_id, pct_discount)
VALUES (?, ?);
''', discounts_data)

# Commit the changes and close the connection
connection.commit()

# Verify the inserted records
cursor.execute("SELECT * FROM t_shirts;")
print("T-Shirts Records:")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM discounts;")
print("\nDiscounts Records:")
for row in cursor.fetchall():
    print(row)

# Close the connection
connection.close()
