#!/usr/bin/python3

import sqlite3
import functools

def log_queries():
    """
    Decorator to log the SQL query before executing it.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            query = kwargs.get('query', args[0] if args else None)
            if query:
                print(f"Executing SQL Query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    """
    Fetch all users based on the given SQL query.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)



