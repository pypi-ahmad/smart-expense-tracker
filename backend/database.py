import sqlite3

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses 
                 (id INTEGER PRIMARY KEY, vendor TEXT, date TEXT, 
                  total REAL, category TEXT)''')
    conn.commit()
    conn.close()

def save_expense(data):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (vendor, date, total, category) VALUES (?, ?, ?, ?)",
              (data.get('vendor_name'), data.get('date'), data.get('total_amount'), data.get('category')))
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect('expenses.db')
    # Return as list of dicts for easy dataframe creation
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]