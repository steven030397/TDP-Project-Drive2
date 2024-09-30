import mysql.connector
import pandas as pd  # Import pandas
import numpy as np

def insertSQLData(matches):
    try:
        # Establish MySQL connection
        connection = mysql.connector.connect(
            host="db4free.net",
            port=3306,
            user="steven3397",
            password="pass123word", 
            database="drive2_db"
        )

        # Create a cursor object using the connection
        cursor = connection.cursor(dictionary=True)
        
        for i in range(len(matches)):
            cursor.execute("""
                INSERT INTO matching_data (user_id_person1, user_id_person2, distance_between_home, distance_between_destination, destination_arrival_diff, destination_departure_diff, 
                person1_home_lat, person1_home_long, person1_destination_lat, person1_destination_long, person2_home_lat, person2_home_long, person2_destination_lat, person2_destination_long,
                matched_day, driver_id, status, status_info, match_type, match_quality, match_direction)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                int(matches.iloc[i]['user_id_person1']) if isinstance(matches.iloc[i]['user_id_person1'], np.integer) else matches.iloc[i]['user_id_person1'],
                int(matches.iloc[i]['user_id_person2']) if isinstance(matches.iloc[i]['user_id_person2'], np.integer) else matches.iloc[i]['user_id_person2'],
                float(matches.iloc[i]['distance_between_home']) if isinstance(matches.iloc[i]['distance_between_home'], (np.float32, np.float64)) else matches.iloc[i]['distance_between_home'],
                float(matches.iloc[i]['distance_between_destination']) if isinstance(matches.iloc[i]['distance_between_destination'], (np.float32, np.float64)) else matches.iloc[i]['distance_between_destination'],
                float(matches.iloc[i]['destination_arrival_diff']) if isinstance(matches.iloc[i]['destination_arrival_diff'], (np.float32, np.float64)) else matches.iloc[i]['destination_arrival_diff'],
                float(matches.iloc[i]['destination_departure_diff']) if isinstance(matches.iloc[i]['destination_departure_diff'], (np.float32, np.float64)) else matches.iloc[i]['destination_departure_diff'],
                matches.iloc[i]['person1_home_lat'],
                matches.iloc[i]['person1_home_long'],
                matches.iloc[i]['person1_destination_lat'],
                matches.iloc[i]['person1_destination_long'],
                matches.iloc[i]['person2_home_lat'],
                matches.iloc[i]['person2_home_long'],
                matches.iloc[i]['person2_destination_lat'],
                matches.iloc[i]['person2_destination_long'],
                matches.iloc[i]['matched_day'],
                int(matches.iloc[i]['driver']) if isinstance(matches.iloc[i]['driver'], np.integer) else matches.iloc[i]['driver'],
                matches.iloc[i]['status'],
                matches.iloc[i]['status_info'],
                matches.iloc[i]['match_type'],
                matches.iloc[i]['match_quality'],
                matches.iloc[i]['match_direction']
            ))
            print(f"Row {i} inserted.")

        # Commit the changes
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


    




