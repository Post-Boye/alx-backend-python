import seed

def stream_user_ages():
    """
    Generator function to yield user ages one by one.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:
        yield row[0]  # Yield only the age field
    
    cursor.close()
    connection.close()

def calculate_average_age():
    """
    Calculate the average age of users using the stream_user_ages generator.
    """
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        print("No users in the dataset.")
        return

    average_age = total_age / count
    print(f"Average age of users: {average_age:.2f}")

