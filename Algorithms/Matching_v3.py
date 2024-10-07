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


# Get data from SQL
route_data = import_sql.getSQLData()
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
        polyline = get_polyline(start_latitude, start_longitude, end_latitude, end_longitude)
        
        # Update the DataFrame if polyline is not None
        if polyline is not None:
            route_data.at[index, 'polyline'] = polyline  # Fill the polyline column

print(route_data)


# now do this clustering
decoded_coords = []
route_map = {}
route_ids = []

for index, route in route_data.iterrows():
    route_id = route['route_id']
    encoded_polyline = route['polyline']

    decoded = polyline.decode(encoded_polyline)
    decoded_coords.extend(decoded)
    route_map[route_id] = decoded
    route_ids.append(route_id)

coords = np.array(decoded_coords)

scaler = StandardScaler()
scaled_coords = scaler.fit_transform(coords)

# db = DBSCAN(eps=0.5, min_samples=10)
# labels = db.fit_predict(scaled_coords)

kmeans = KMeans(n_clusters=10, random_state=42)
labels = kmeans.fit_predict(scaled_coords)

cluster_map = {}

current_index = 0

# Map each route_id to its cluster label based on the first coordinate
for route_id, coords in route_map.items():
    # Use the cluster label of the first coordinate of each route
    cluster_map[route_id] = labels[current_index]

    # Increment the index by the number of coordinates in the current route
    current_index += len(coords)

    # Check for overflow
    if current_index >= len(labels):
        break


#export_sql.insertClusterAndPolylineData(route_data, cluster_map)

### VISUALISE CLUSTERS ###
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

### ###

