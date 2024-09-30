# Install required packages
# pip install scikit-learn
# pip install pandas
# pip install googlemaps geopy shapely 

import googlemaps
from shapely.geometry import LineString, Point
from geopy.distance import geodesic
from shapely.ops import nearest_points

import sklearn
import math
from datetime import datetime
import pandas as pd
import import_sql
import mysql.connector

route_data = import_sql.getSQLData()
import googlemaps

try:
    gmaps = googlemaps.Client(key='AIzaSyBWW9zve7B8Zy7HM2mHDtNz8HXED_HiFlg')
    print("Google Maps Client initialized successfully.")
except Exception as e:
    print(f"Error initializing Google Maps Client: {e}")


#gmaps = googlemaps.Client(key='AIzaSyBWW9zve7B8Zy7HM2mHDtNz8HXED_HiFlg')# Function to calculate haversine distance (in km)
def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


# Function to find the decoded polyline (Google Maps encoded route)
def get_route(location1, location2):
    directions = gmaps.directions(location1, location2)
    polyline = directions[0]['overview_polyline']['points']
    decoded_polyline = googlemaps.convert.decode_polyline(polyline)  # Decode polyline to (lat, lon) tuples
    return decoded_polyline


# Function to find users near a specific route
def find_users_near_route(users, route_line, max_distance_km):
    nearby_users = []
    for user in users:
        user_location = Point(user['location'])  # Assume user['location'] is a tuple (lat, lon)        
        nearest_point = nearest_points(route_line, user_location)[0] # Find nearest point on the route to the user       
        distance_to_route = geodesic((user_location.y, user_location.x), # Calculate distance using geodesic distance
                                     (nearest_point.y, nearest_point.x)).kilometers
        if distance_to_route <= max_distance_km:
            nearby_users.append(user)
    return nearby_users


# Function to find matches based on distance and time threshold
def find_matches(route_data, distance_threshold=1.0, time_threshold=30):
    matches = []
    for travel_day in {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'}:
        route_data['travel_day'] = travel_day
        day_route_data = route_data[route_data['travel_day'] == travel_day]
        for i in range(len(day_route_data) - 1):
            for j in range(i + 1, len(day_route_data)):

                # Assign driver logic based on car availability
                if day_route_data.iloc[i]['has_car'] or day_route_data.iloc[j]['has_car']:
                    assigned_driver = day_route_data.iloc[i]['user_id'] if day_route_data.iloc[i]['has_car'] else day_route_data.iloc[j]['user_id']
                
                    # Calculate start and end distances
                    start_distance = haversine(day_route_data.iloc[i]['start_longitude'], day_route_data.iloc[i]['start_latitude'],
                                               day_route_data.iloc[j]['start_longitude'], day_route_data.iloc[j]['start_latitude'])
                    end_distance = haversine(day_route_data.iloc[i]['end_longitude'], day_route_data.iloc[i]['end_latitude'],
                                             day_route_data.iloc[j]['end_longitude'], day_route_data.iloc[j]['end_latitude'])

                    if start_distance <= distance_threshold and end_distance <= distance_threshold:
                        # Time calculations
                        user_i_start_time = datetime.strptime(day_route_data.iloc[i]['destination_arrival_time'], '%H:%M')
                        user_i_end_time = datetime.strptime(day_route_data.iloc[i]['destination_departure_time'], '%H:%M')
                        user_j_start_time = datetime.strptime(day_route_data.iloc[j]['destination_arrival_time'], '%H:%M')
                        user_j_end_time = datetime.strptime(day_route_data.iloc[j]['destination_departure_time'], '%H:%M')
                        
                        start_time_diff = abs((user_i_start_time - user_j_start_time).total_seconds() / 60)
                        end_time_diff = abs((user_i_end_time - user_j_end_time).total_seconds() / 60)
                        
                        if start_time_diff <= time_threshold and end_time_diff <= time_threshold:
                            matches.append({
                                'user_id_person1': day_route_data.iloc[i]['user_id'],
                                'user_id_person2': day_route_data.iloc[j]['user_id'],
                                'distance_between_home': start_distance,
                                'distance_between_destination': end_distance,
                                'destination_arrival_diff': start_time_diff,
                                'destination_departure_diff': end_time_diff,
                                'matched_day': travel_day,
                                'driver': assigned_driver
                            })
    
    return pd.DataFrame(matches)

if 'travel_day' not in route_data.columns:
    print("Column 'travel_day' is missing.")
    # ดำเนินการแก้ไข เช่น เพิ่มคอลัมน์ที่ขาดหายไป
else:
    # ดำเนินการต่อหากมีคอลัมน์
    matches_table = find_matches(route_data, distance_threshold=1.0, time_threshold=30)



# Example usage:
route_data = pd.DataFrame()  # Replace this with the actual data from import_sql.getSQLData()

matches_table = find_matches(route_data, distance_threshold=1.0, time_threshold=30)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(matches_table)
pd.reset_option('display.max_rows')
