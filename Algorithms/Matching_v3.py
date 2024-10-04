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
export_sql.insertClusterAndPolylineData(route_data)