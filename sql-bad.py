import sqlite3

def authenticate_user(username, password):
    # Connect to the database
    conn = sqlite3.connect('enterprise_app.db')
    cursor = conn.cursor()
    
    # VULNERABILITY: Direct string interpolation allows SQL Injection.
    # An attacker could input: admin' -- 
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    # Executing the unsafe query
    cursor.execute(query)
    user_record = cursor.fetchone()
    
    conn.close()
    
    if user_record:
        return True
    else:
        return False
