# Install required packages
# pip install scikit-learn
# pip install pandas

import sklearn

import math
from datetime import datetime
import pandas as pd
import import_sql
import export_sql
import mysql.connector
import numpy as np

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



# class User:
#     def __init__(self, user_id, name, car_model, fuel_efficiency, start_longitude, start_latitude, end_longitude, end_latitude, start_point_name, end_point_name, distance, travel_time, start_time, end_time, travel_days):
#         self.user_id = user_id
#         self.name = name
#         self.car_model = car_model  
#         self.fuel_efficiency = fuel_efficiency
#         self.start_longitude = start_longitude
#         self.start_latitude = start_latitude
#         self.end_longitude = end_longitude
#         self.end_latitude = end_latitude
#         self.start_point_name = start_point_name
#         self.end_point_name = end_point_name
#         self.distance = distance  
#         self.travel_time = travel_time
#         self.start_time = datetime.strptime(start_time, '%H:%M')  
#         self.end_time = datetime.strptime(end_time, '%H:%M')  
#         self.travel_days = travel_days  

#     def __repr__(self):
#         return f"User({self.name})"


# def calculate_fuel_cost(distance, fuel_efficiency, fuel_price_per_liter=40):
#     liters_needed = distance / fuel_efficiency
#     return liters_needed * fuel_price_per_liter


# def overlapping_days(days1, days2):
#     return list(set(days1) & set(days2))


def find_matches(route_data, distance_threshold=1.0, time_threshold=30):
    matches = []
    speed = 65.2  # Speed in km/h to calculate waiting time from road congestion in Australia paper https://www.aaa.asn.au/wp-content/uploads/2019/06/Road-Congestion-In-Australia-2019-v.3.pdf
    
    for travel_day in {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'}:
        day_route_data = route_data[(route_data['travel_day'] == travel_day)]
        
        for i in range(len(day_route_data) - 1):
            for j in range(i + 1, len(day_route_data)):

                if day_route_data.iloc[i]['has_car'] or day_route_data.iloc[j]['has_car']:
                    if day_route_data.iloc[i]['has_car'] and day_route_data.iloc[j]['has_car']:
                        assigned_driver = 0
                    elif day_route_data.iloc[i]['has_car']:
                        assigned_driver = day_route_data.iloc[i]['user_id']  # User i is the driver
                    else:
                        assigned_driver = day_route_data.iloc[j]['user_id']  # User j is the driver
    
                
                    start_distance = haversine(day_route_data.iloc[i]['start_longitude'], day_route_data.iloc[i]['start_latitude'], day_route_data.iloc[j]['start_longitude'], day_route_data.iloc[j]['start_latitude'])

                    end_distance = haversine(day_route_data.iloc[i]['end_longitude'], day_route_data.iloc[i]['end_latitude'], day_route_data.iloc[j]['end_longitude'], day_route_data.iloc[j]['end_latitude'])

                    if start_distance <= distance_threshold and end_distance <= distance_threshold:

                        user_i_start_time = datetime.strptime(day_route_data.iloc[i]['destination_arrival_time'] ,'%H:%M')
                        user_i_end_time = datetime.strptime(day_route_data.iloc[i]['destination_departure_time'] ,'%H:%M')
                        user_j_start_time = datetime.strptime(day_route_data.iloc[j]['destination_arrival_time'] ,'%H:%M')
                        user_j_end_time = datetime.strptime(day_route_data.iloc[j]['destination_departure_time'] ,'%H:%M')
                        
                        start_time_diff = abs((user_i_start_time - user_j_start_time).total_seconds() / 60)
                        end_time_diff = abs((user_i_end_time - user_j_end_time).total_seconds() / 60)

                       
                        if start_time_diff <= time_threshold and end_time_diff <= time_threshold:
                            #match_time = (max(user1_start_time, user2.start_time), min(user1.end_time, user2.end_time))
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
                                'distance_between_home': start_distance,
                                'distance_between_destination': end_distance,
                                'destination_arrival_diff': start_time_diff,
                                'destination_departure_diff': end_time_diff,
                                'matched_day': travel_day,
                                'driver': assigned_driver,
                                'status': "active",
                                'status_info': "",
                                'match_type': "type_1",
                                'match_quality': "",
                                'match_direction': ""
                            })  
        
    return pd.DataFrame(matches)

matches_table = find_matches(route_data, distance_threshold=1.0, time_threshold=30)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(find_matches(route_data, distance_threshold=1.0, time_threshold=30))
pd.reset_option('display.max_rows')

#Only run once#
export_sql.insertSQLData(matches_table)

# def create_cost_table(user, matches_df, fuel_price_per_liter=40):
#     cost_data = []
    
#     for _, row in matches_df.iterrows():
#         user1 = next(user for user in users if user.user_id == row['user_id_person1'])
#         user2 = next(user for user in users if user.user_id == row['user_id_person2'])
        
#         distance = user1.distance
#         cost1 = calculate_fuel_cost(distance, user1.fuel_efficiency, fuel_price_per_liter)
#         cost2 = calculate_fuel_cost(distance, user2.fuel_efficiency, fuel_price_per_liter)
        
#         cost_data.append({
#             'user_id_person1': user1.user_id,
#             'person1_name': user1.name,
#             'car_model_person1': user1.car_model,
#             'fuel_efficiency_person1': user1.fuel_efficiency,
#             'fuel_cost_person1': cost1,
#             'user_id_person2': user2.user_id,
#             'person2_name': user2.name,
#             'car_model_person2': user2.car_model,
#             'fuel_efficiency_person2': user2.fuel_efficiency,
#             'fuel_cost_person2': cost2,
#             'total_cost': cost1 + cost2,
#             'common_days': row['common_days']
#         })
    
#     return pd.DataFrame(cost_data)


# users = [
#     User(1, "Alice", "Sedan", 15, 100.0, 13.7, 100.2, 13.8, "Start A", "End A", 5, 30, "08:00", "09:00", ["Monday", "Wednesday"]),
#     User(2, "Bob", "SUV", 10, 100.1, 13.75, 100.25, 13.85, "Start B", "End B", 6, 35, "08:15", "09:15", ["Monday", "Friday"]),
#     User(3, "Charlie", "Hatchback", 18, 101.0, 14.0, 101.1, 14.1, "Start C", "End C", 8, 45, "07:45", "08:45", ["Tuesday", "Wednesday"]),
#     User(4, "Sally", "BMW", 18, 101.0, 14.0, 101.1, 14.1, "Start C", "End C", 8, 45, "07:45", "08:45", ["Thursday", "Sunday"]),
#     User(5, "Jane", "Toyota", 18, 101.0, 14.0, 101.1, 14.1, "Start C", "End C", 8, 45, "07:45", "08:45", ["Tuesday", "Thursday"]),]

# # # matches_df = find_matches(user, distance_threshold=13.0, time_threshold=60)
# # # cost_df = create_cost_table(user, matches_df, fuel_price_per_liter=40)

# # # display(cost_df)
# # # display(matches_df)

# # # combined_df = pd.merge(matches_df, cost_df, on=['user_id_person1', 'user_id_person2'])


# # # pd.set_option('display.float_format', '{:.2f}'.format)


# # # display(combined_df)
