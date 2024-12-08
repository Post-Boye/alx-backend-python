import time
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

def retry_on_failure(retries=3, delay=2):
    """
    Decorator to retry a function if it raises an exception.
    Retries the function `retries` times with a `delay` between attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= retries:
                        print(f"Operation failed after {retries} retries.")
                        raise e
                    print(f"Retrying due to error: {e}. Attempt {attempts}/{retries}")
                    time.sleep(delay)
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users from the 'users' table with retry on failure.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
try:
    users = fetch_users_with_retry()
    print(users)
except Exception as e:
    print(f"Failed to fetch users: {e}")

