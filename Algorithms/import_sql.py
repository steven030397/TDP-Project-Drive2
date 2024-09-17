import mysql.connector
import pandas as pd  # Import pandas

def getSQLData():
    # Establish MySQL connection
    connection = mysql.connector.connect(
        host="db4free.net",
        port=3306,
        user="steven3397",
        password="pass123word", 
        database="drive2_db"
    )

    # Create a cursor object using the connection
    cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get results as dictionaries

    # Define the query to select all rows from the 'route' table
    query = """
    SELECT 
        route.route_id,
        users.user_id,
        route.start_latitude,
        route.start_longitude,
        route.end_latitude,
        route.end_longitude,
        route.destination_arrival_time,
        route.destination_departure_time,
        route.travel_day,
        users.has_car
    FROM 
        route
    JOIN 
        users 
    ON 
        route.user_id = users.user_id;
    """

    # Execute the query
    cursor.execute(query)

    # Fetch all rows from the result
    prematching_data = cursor.fetchall()

    # Convert the fetched data into a DataFrame
    df = pd.DataFrame(prematching_data)

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Return the DataFrame
    return df
