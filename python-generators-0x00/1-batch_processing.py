import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator function to fetch rows in batches from the user_data table.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # Replace with your MySQL username
            password="your_password",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")
            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break
                yield rows  # Yield a batch of rows
            cursor.close()
    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        filtered_users = (user for user in batch if user['age'] > 25)
        for user in filtered_users:
            print(user)  # Process each filtered user (e.g., print them)

