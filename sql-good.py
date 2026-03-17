import sqlite3

def authenticate_user(username, password):
    conn = sqlite3.connect('enterprise_app.db')
    cursor = conn.cursor()
    
    # SECURE: Using parameterized queries (?) prevents SQL Injection.
    # The database driver safely escapes the input automatically.
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    # Executing the safe query with a tuple of variables
    cursor.execute(query, (username, password))
    user_record = cursor.fetchone()
    
    conn.close()
    
    if user_record:
        return True
    else:
        return False
