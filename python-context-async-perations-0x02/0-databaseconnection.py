import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        """
        Initialize the DatabaseConnection object with the database name.
        :param db_name: Name of the database to connect to
        """
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """
        Open the database connection and return the cursor for executing queries.
        :return: Database cursor
        """
        self.connection = sqlite3.connect(self.db_name)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the database connection. Handles exceptions if any occur.
        :param exc_type: Exception type
        :param exc_value: Exception value
        :param traceback: Traceback object
        """
        if self.connection:
            self.connection.commit()
            self.connection.close()

# Example usage
if __name__ == "__main__":
    # Create an example database and table for demonstration purposes
    db_name = "example.db"
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.executemany("INSERT INTO users (name) VALUES (?)", [("Alice",), ("Bob",), ("Charlie",)])
        conn.commit()

    # Use the custom context manager to query the database
    with DatabaseConnection(db_name) as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

    # Print the query results
    for row in results:
        print(row)

