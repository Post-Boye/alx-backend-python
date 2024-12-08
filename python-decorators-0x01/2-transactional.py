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

def transactional(func):
    """
    Decorator that wraps a function in a database transaction.
    Commits if the function succeeds, rolls back if it raises an error.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Run the decorated function
            conn.commit()  # Commit transaction if no errors
            return result
        except Exception as e:
            conn.rollback()  # Rollback transaction if an error occurs
            raise e  # Re-raise the exception
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update the email of a user in the 'users' table.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
print("User email updated successfully.")

