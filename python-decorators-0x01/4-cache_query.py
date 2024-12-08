import time
import sqlite3
import functools

query_cache = {}

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

def cache_query(func):
    """
    Decorator to cache the results of database queries.
    Caches results based on the query string.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]  # Return cached result

        print(f"Cache miss for query: {query}")
        result = func(*args, **kwargs)  # Execute the function if not cached
        query_cache[query] = result  # Cache the result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users from the database with query caching.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute the query and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)

