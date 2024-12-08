import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that opens a database connection, passes it to the function, 
    and ensures the connection is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Replace 'users.db' with your database
        try:
            result = func(conn, *args, **kwargs)  # Pass the connection as the first argument
        finally:
            conn.close()  # Ensure the connection is closed
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a user by ID from the 'users' table.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)

