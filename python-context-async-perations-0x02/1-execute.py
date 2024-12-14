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

class ExecuteQuery:
    def __init__(self, db_name, query, params):
        """
        Initialize the ExecuteQuery object with the database name, query, and parameters.
        :param db_name: Name of the database to connect to
        :param query: SQL query to execute
        :param params: Parameters for the SQL query
        """
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Open the database connection, execute the query, and return the results.
        :return: Query results
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the database connection. Handles exceptions if any occur.
        :param exc_type: Exception type
        :param exc_value: Exception value
        :param traceback: Traceback object
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.commit()
            self.connection.close()

# Example usage
if __name__ == "__main__":
    # Create an example database and table for demonstration purposes
    db_name = "example.db"
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [("Alice", 30), ("Bob", 20), ("Charlie", 35)])
        conn.commit()

    # Use the ExecuteQuery context manager to query the database
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery(db_name, query, params) as results:
        # Print the query results
        for row in results:
            print(row)

