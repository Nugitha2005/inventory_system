import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="inventory_db" # Make sure this matches your PHPMyAdmin DB Name!
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# --- LOGIN CHECK ---
def check_login(username, password):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    return False

# --- ITEM FUNCTIONS (Fixed Names) ---

# Renamed from 'add_item' to 'insert_item' to match main.py
def insert_item(name, price, qty):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # We removed 'category' because your UI doesn't have a box for it yet
            query = "INSERT INTO items (name, price, quantity) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, price, qty))
            conn.commit() # <--- IMPORTANT: Saves the data
            print(f"✅ Saved: {name}")
        except mysql.connector.Error as err:
            print(f"❌ Error Saving: {err}")
        finally:
            conn.close()

# Renamed from 'get_all_items' to 'fetch_all_items' to match main.py
def fetch_all_items():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        results = cursor.fetchall()
        conn.close()
        return results
    return []