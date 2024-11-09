import math
import requests
from datetime import datetime
import pandas as pd
import import_sql
import export_sql
import mysql.connector
import numpy as np
from math import radians, sin, cos, sqrt, atan2
import googlemaps
import polyline
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
import folium
import matplotlib.cm as cm
import matplotlib.colors as colors
import time
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

while True:
    # Get data from SQL
    route_data = import_sql.getSQLData()
    route_data = route_data[0:501] #175 users
    print(route_data)


    # Haversine formula to calculate distance between two points on the Earth
    def haversine(lon1, lat1, lon2, lat2):
        R = 6371.0  # Radius of the Earth in km
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance


    def get_polyline(start_latitude, start_longitude, end_latitude, end_longitude):
        """
        Function to get polyline from start and end coordinates using Google Directions API.
        Args:
        - start_latitude: Latitude of the starting point.
        - start_longitude: Longitude of the starting point.
        - end_latitude: Latitude of the end point.
        - end_longitude: Longitude of the end point.
        
        Returns:
        - polyline: Encoded polyline string of the route.
        """
        # Construct the API request URL
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_latitude},{start_longitude}&destination={end_latitude},{end_longitude}&key=AIzaSyBWW9zve7B8Zy7HM2mHDtNz8HXED_HiFlg"

        # Make the API request
        response = requests.get(url)

        # Parse the JSON response
        directions = response.json()

        # Check if the request was successful
        if directions['status'] == 'OK':
            # Extract the polyline from the response
            polyline = directions['routes'][0]['overview_polyline']['points']
            return polyline
        else:
            print(f"Error fetching polyline: {directions['status']}")
            return None

    # Iterate through each row in the DataFrame
    for index, row in route_data.iterrows():
        # Check if the polyline column is empty
        if pd.isna(row['polyline']):  # Assuming 'polyline' is the name of the column
            start_latitude = row['start_latitude']
            start_longitude = row['start_longitude']
            end_latitude = row['end_latitude']
            end_longitude = row['end_longitude']

            # Get the polyline
            my_polyline = get_polyline(start_latitude, start_longitude, end_latitude, end_longitude)
            
            # Update the DataFrame if polyline is not None
            if my_polyline is not None:
                route_data.at[index, 'polyline'] = my_polyline  # Fill the polyline column

    print(route_data)

    # Example function to decode polylines
    def decode_polyline(encoded_polyline):
        return polyline.decode(encoded_polyline)

    # Sample route data (replace these with your actual route data)
    route_data = pd.DataFrame({
        'route_id': [1, 2, 3],
        'polyline': ['encoded_polyline_string_1', 'encoded_polyline_string_2', 'encoded_polyline_string_3']
    })

    # Step 1: Decode polylines and store routes
    decoded_routes = []
    for index, route in route_data.iterrows():
        encoded_polyline = route['polyline']
        if isinstance(encoded_polyline, str):
            decoded = decode_polyline(encoded_polyline)
            decoded_routes.append(decoded)
        else:
            print(f"Invalid polyline for route_id {route['route_id']}: {encoded_polyline}")

    # Step 2: Calculate DTW distances
    distance_matrix = np.zeros((len(decoded_routes), len(decoded_routes)))

    for i in range(len(decoded_routes)):
        for j in range(i, len(decoded_routes)):
            dtw_distance, _ = fastdtw(decoded_routes[i], decoded_routes[j], dist=euclidean)
            distance_matrix[i, j] = dtw_distance
            distance_matrix[j, i] = dtw_distance  # Symmetric matrix

    # Step 3: Cluster routes using KMeans
    # Reshape the distance matrix into a suitable format for KMeans
    # Flatten the distance matrix and find clusters based on similarities
    flat_distances = distance_matrix.flatten()
    # Use a method to find the optimal number of clusters (e.g., elbow method)
    # For this example, we set n_clusters to 2
    n_clusters = 2
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(flat_distances.reshape(-1, 1))

    # Step 4: Assign cluster labels to routes
    labels = kmeans.labels_

    # Map route_ids to their respective cluster labels
    cluster_map = {route_data['route_id'][i]: labels[i] for i in range(len(labels))}

    # Print the clustering results
    for route_id, cluster_label in cluster_map.items():
        print(f"Route ID: {route_id} is in Cluster: {cluster_label}")

# simpler clustering
    # # now do this clustering
    # decoded_coords = []
    # route_map = {}
    # route_ids = []

    # for index, route in route_data.iterrows():
    #     route_id = route['route_id']
    #     encoded_polyline = route['polyline']
        

    #     # Check if the polyline is valid and then decode
    #     if isinstance(encoded_polyline, str):
    #         decoded = polyline.decode(encoded_polyline)
    #         decoded_coords.extend(decoded)
    #         route_map[route_id] = decoded
    #         route_ids.append(route_id)
    #     else:
    #         print(f"Invalid polyline for route_id {route_id}: {encoded_polyline}")


    # coords = np.array(decoded_coords)

    # scaler = StandardScaler()
    # scaled_coords = scaler.fit_transform(coords)
    # n_clusters = 10
    # kmeans = KMeans(n_clusters = n_clusters, random_state=42)
    # labels = kmeans.fit_predict(scaled_coords)
    # cluster_map = {}
    # current_index = 0

    # # Map each route_id to its cluster label based on the first coordinate
    # for route_id, coords in route_map.items():
    #     # Use the cluster label of the first coordinate of each route
    #     cluster_map[route_id] = int(labels[current_index])

    #     # Increment the index by the number of coordinates in the current route
    #     current_index += len(coords)

    #     # Check for overflow
    #     if current_index >= len(labels):
    #         break

    # print(cluster_map)
# simpler clustering

    export_sql.insertClusterAndPolylineData(route_data, cluster_map)


    ### VISUALISE CLUSTERS  ONLY WORKS THE SECOND TIME BECAUSE THE ROUTE_DATA IS NOT UPDATED###
    route_data = import_sql.getSQLData()
    route_data = route_data[0:501]
    for travel_day in {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'}:
        day_route_data = route_data[(route_data['travel_day'] == travel_day)]

        # Step 2: Create a folium map centered at an average location
        # Calculate the mean latitude and longitude to set the initial map view
        mean_latitude = day_route_data['start_latitude'].mean()
        mean_longitude = day_route_data['start_longitude'].mean()

        # Initialize a folium map
        map_obj = folium.Map(location=[mean_latitude, mean_longitude], zoom_start=12, tiles='CartoDB positron')

        # Step 3: Set up color mapping for clusters
        unique_clusters = day_route_data['cluster_id'].unique()
        colormap = cm.get_cmap('Set1', len(unique_clusters))  # 'Set1' is a good color palette for categories
        norm = colors.Normalize(vmin=min(unique_clusters), vmax=max(unique_clusters))

        # Step 4: Plot start and end points with colors based on cluster ID
        for _, row in day_route_data.iterrows():
            # Set color based on cluster_id
            cluster_color = colors.to_hex(colormap(norm(row['cluster_id'])))

            # Add a circle marker for the start point
            folium.CircleMarker(
                location=[row['start_latitude'], row['start_longitude']],
                radius=5,
                color=cluster_color,
                fill=True,
                fill_color=cluster_color,
                fill_opacity=0.7,
                popup=f"Cluster ID: {row['cluster_id']}<br>Start Coordinates: ({row['start_latitude']}, {row['start_longitude']})"
            ).add_to(map_obj)

            # Add a circle marker for the end point with the same color
            folium.CircleMarker(
                location=[row['end_latitude'], row['end_longitude']],
                radius=5,
                color=cluster_color,
                fill=True,
                fill_color=cluster_color,
                fill_opacity=0.7,
                popup=f"Cluster ID: {row['cluster_id']}<br>End Coordinates: ({row['end_latitude']}, {row['end_longitude']})"
            ).add_to(map_obj)


            # Draw a polyline connecting the start and end points
            folium.PolyLine(
                locations=[(row['start_latitude'], row['start_longitude']), (row['end_latitude'], row['end_longitude'])],
                color=cluster_color,
                weight=2.5,
                opacity=0.8
            ).add_to(map_obj)

        # Step 5: Save the map as an HTML file
        map_filename = f"{travel_day.lower()}_route_clusters_map.html"
        map_obj.save(map_filename)
        print(f"Map created and saved as '{map_filename}' for {travel_day}.")

    ### MATCHING ALGORITHM ###

    ### TYPE 1: Location proximity matching ###
    time_threshold = 5 #minutes
    distance_threshold = 0.75 #km
    unique_clusters = route_data['cluster_id'].unique()

    matches = []
    for cluster_id in unique_clusters:
        for travel_day in {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'}:
            day_route_data = route_data[route_data['travel_day'] == travel_day]
            for i in range(len(day_route_data) - 1):
                for j in range(i + 1, len(day_route_data)):

                    # Assign driver logic based on car availability
                    if day_route_data.iloc[i]['has_car'] == 'YES' or day_route_data.iloc[j]['has_car'] == 'YES':
                        assigned_driver = day_route_data.iloc[i]['user_id'] if day_route_data.iloc[i]['has_car'] else day_route_data.iloc[j]['user_id']

                        # If the user leaves home at almost the same time, and lives close by...
                        user_i_start_time = datetime.strptime(day_route_data.iloc[i]['destination_arrival_time'], '%H:%M')
                        user_j_start_time = datetime.strptime(day_route_data.iloc[j]['destination_arrival_time'], '%H:%M')
                        start_time_diff = abs((user_i_start_time - user_j_start_time).total_seconds() / 60)
                        start_distance = haversine(day_route_data.iloc[i]['start_longitude'], day_route_data.iloc[i]['start_latitude'],
                                                    day_route_data.iloc[j]['start_longitude'], day_route_data.iloc[j]['start_latitude'])
                        if start_time_diff <= time_threshold and start_distance <= distance_threshold:
                            matches.append({
                                'user_id_person1': day_route_data.iloc[i]['user_id'],
                                'user_id_person2': day_route_data.iloc[j]['user_id'],
                                'person1_home_lat': day_route_data.iloc[i]['start_latitude'],
                                'person1_home_long': day_route_data.iloc[i]['start_longitude'],
                                'person1_destination_lat': day_route_data.iloc[i]['end_latitude'],
                                'person1_destination_long': day_route_data.iloc[i]['end_longitude'],
                                'person2_home_lat': day_route_data.iloc[j]['start_latitude'],
                                'person2_home_long': day_route_data.iloc[j]['start_longitude'],
                                'person2_destination_lat': day_route_data.iloc[j]['end_latitude'],
                                'person2_destination_long': day_route_data.iloc[j]['end_longitude'],
                                'status': 'active',
                                'status_info': "",
                                'match_type': 'type_1',
                                'match_direction': 'go',
                                'match_quality': (1 - (start_time_diff / time_threshold)) * (1 - (start_distance / distance_threshold)),
                                'google_actual_distance1': day_route_data.iloc[i]['google_actual_distance'],
                                'google_actual_distance2': day_route_data.iloc[j]['google_actual_distance'],
                                'distance_between_home': start_distance,
                                'distance_between_destination': end_distance,
                                'destination_arrival_diff': start_time_diff,
                                'destination_departure_diff': end_time_diff,
                                'matched_day': travel_day,
                                'driver': assigned_driver
                            })

                        # If the user leaves work at almost the same time, and works close by...
                        user_i_end_time = datetime.strptime(day_route_data.iloc[i]['destination_departure_time'], '%H:%M')
                        user_j_end_time = datetime.strptime(day_route_data.iloc[j]['destination_departure_time'], '%H:%M')
                        end_time_diff = abs((user_i_end_time - user_j_end_time).total_seconds() / 60)
                        end_distance = haversine(day_route_data.iloc[i]['end_longitude'], day_route_data.iloc[i]['end_latitude'],
                                                    day_route_data.iloc[j]['end_longitude'], day_route_data.iloc[j]['end_latitude'])
                        if end_time_diff <= time_threshold and end_distance <= distance_threshold:
                            matches.append({
                                'user_id_person1': day_route_data.iloc[i]['user_id'],
                                'user_id_person2': day_route_data.iloc[j]['user_id'],
                                'person1_home_lat': day_route_data.iloc[i]['start_latitude'],
                                'person1_home_long': day_route_data.iloc[i]['start_longitude'],
                                'person1_destination_lat': day_route_data.iloc[i]['end_latitude'],
                                'person1_destination_long': day_route_data.iloc[i]['end_longitude'],
                                'person2_home_lat': day_route_data.iloc[j]['start_latitude'],
                                'person2_home_long': day_route_data.iloc[j]['start_longitude'],
                                'person2_destination_lat': day_route_data.iloc[j]['end_latitude'],
                                'person2_destination_long': day_route_data.iloc[j]['end_longitude'],
                                'status': 'active',
                                'status_info': "",
                                'match_type': 'type_1',
                                'match_direction': 'return',
                                'match_quality': (1 - (end_time_diff / time_threshold)) * (1 - (end_distance / distance_threshold)),
                                'google_actual_distance1': day_route_data.iloc[i]['google_actual_distance'],
                                'google_actual_distance2': day_route_data.iloc[j]['google_actual_distance'],
                                'distance_between_home': start_distance,
                                'distance_between_destination': end_distance,
                                'destination_arrival_diff': start_time_diff,
                                'destination_departure_diff': end_time_diff,
                                'matched_day': travel_day,
                                'driver': assigned_driver
                            })

    matches_df_0 = pd.DataFrame(matches)
    #Only run once#
    export_sql.insertSQLData(matches_df_0)
    print("Matches exported")
    ### ###






    ### Count number of matches and store in 'users' ###
    matches_df = matches_df_0[['user_id_person1', 'user_id_person2']].drop_duplicates()
    # 2. Count occurrences of each user_id in both columns
    person1_counts = matches_df['user_id_person1'].value_counts().reset_index()
    person1_counts.columns = ['user_id', 'count_as_person1']

    person2_counts = matches_df['user_id_person2'].value_counts().reset_index()
    person2_counts.columns = ['user_id', 'count_as_person2']

    # 3. Merge the counts from both columns
    user_tally = pd.merge(person1_counts, person2_counts, on='user_id', how='outer')

    # 4. Fill NaN values with 0 for users who are present in only one of the columns
    user_tally['count_as_person1'].fillna(0, inplace=True)
    user_tally['count_as_person2'].fillna(0, inplace=True)

    # 5. Calculate the total tally for each user_id
    user_tally['total_tally'] = user_tally['count_as_person1'] + user_tally['count_as_person2']

    # 6. Select only 'user_id' and 'total_tally' columns
    user_tally = user_tally[['user_id', 'total_tally']]

    # Convert 'user_id' to string and 'total_tally' to int
    user_tally['user_id'] = user_tally['user_id'].astype(str)
    user_tally['total_tally'] = user_tally['total_tally'].astype(int)

    # Print the tally result for confirmation
    print("User Tally:\n", user_tally)

    # 7. Connect to MySQL database
    db_connection = mysql.connector.connect(
                host="db4free.net",
                port=3306,
                user="steven3397",
                password="pass123word", 
                database="drive2_db"
            )
    cursor = db_connection.cursor()

        # Clear last tally
    update_query = """
        UPDATE users 
        SET number_of_match = 0, 
            is_matched = 'NO'
    """
    cursor.execute(update_query)

    # 8. Update the 'users' table with 'number_of_match' and 'is_matched'
    for _, row in user_tally.iterrows():
        user_id = row['user_id']
        total_tally = row['total_tally']

        # Update 'number_of_match' and set 'is_matched' to 'YES' if total_tally > 0
        update_query = """
            UPDATE users 
            SET number_of_match = %s, 
                is_matched = CASE WHEN %s > 0 THEN 'YES' ELSE is_matched END
            WHERE user_id = %s
        """
        cursor.execute(update_query, (total_tally, total_tally, user_id))

    # 9. Commit the changes and close the connection
    db_connection.commit()
    cursor.close()
    db_connection.close()

    print("SQL table 'users' successfully updated with match tallies!")
    ### ###

    time.sleep(86400) # Sleep for 86400 seconds (24 hrs)