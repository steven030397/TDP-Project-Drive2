# Install required packages
# pip install scikit-learn
# pip install pandas

import sklearn

import math
from datetime import datetime
import pandas as pd
from IPython.display import display


def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c  

class User:
    def __init__(self, user_id, name, car_model, fuel_efficiency, start_longitude, start_latitude, end_longitude, end_latitude, start_point_name, end_point_name, distance, travel_time, start_time, end_time, travel_days):
        self.user_id = user_id
        self.name = name
        self.car_model = car_model  
        self.fuel_efficiency = fuel_efficiency
        self.start_longitude = start_longitude
        self.start_latitude = start_latitude
        self.end_longitude = end_longitude
        self.end_latitude = end_latitude
        self.start_point_name = start_point_name
        self.end_point_name = end_point_name
        self.distance = distance  
        self.travel_time = travel_time
        self.start_time = datetime.strptime(start_time, '%H:%M')  
        self.end_time = datetime.strptime(end_time, '%H:%M')  
        self.travel_days = travel_days  

    def __repr__(self):
        return f"User({self.name})"


def calculate_fuel_cost(distance, fuel_efficiency, fuel_price_per_liter=40):
    liters_needed = distance / fuel_efficiency
    return liters_needed * fuel_price_per_liter


def overlapping_days(days1, days2):
    return list(set(days1) & set(days2))


def find_matches(users, distance_threshold=1.0, time_threshold=30):
    matches = []
    
    for i, user1 in enumerate(users):
        for user2 in users[i+1:]:
            common_days = overlapping_days(user1.travel_days, user2.travel_days)
            if not common_days:
                continue  
            
            start_distance = haversine(user1.start_longitude, user1.start_latitude, user2.start_longitude, user2.start_latitude)
            end_distance = haversine(user1.end_longitude, user1.end_latitude, user2.end_longitude, user2.end_latitude)
            
            if start_distance <= distance_threshold and end_distance <= distance_threshold:
                start_time_diff = abs((user1.start_time - user2.start_time).total_seconds() / 60)
                end_time_diff = abs((user1.end_time - user2.end_time).total_seconds() / 60)
                
                if start_time_diff <= time_threshold and end_time_diff <= time_threshold:
                    match_time = (max(user1.start_time, user2.start_time), min(user1.end_time, user2.end_time))
                    matches.append({
                        'user_id_person1': user1.user_id,
                        'person1_name': user1.name,
                        'user_id_person2': user2.user_id,
                        'person2_name': user2.name,
                        'start_latitude': user1.start_latitude,
                        'start_longitude': user1.start_longitude,
                        'start_point_name': user1.start_point_name,
                        'end_latitude': user1.end_latitude,
                        'end_longitude': user1.end_longitude,
                        'end_point_name': user1.end_point_name,
                        'start_time': user1.start_time.strftime('%H:%M'),
                        'end_time': user1.end_time.strftime('%H:%M'),
                        'match_time': f"{match_time[0].strftime('%H:%M')} - {match_time[1].strftime('%H:%M')}",
                        'common_days': common_days
                    })
    
    return pd.DataFrame(matches)

def create_cost_table(users, matches_df, fuel_price_per_liter=40):
    cost_data = []
    
    for _, row in matches_df.iterrows():
        user1 = next(user for user in users if user.user_id == row['user_id_person1'])
        user2 = next(user for user in users if user.user_id == row['user_id_person2'])
        
        distance = user1.distance
        cost1 = calculate_fuel_cost(distance, user1.fuel_efficiency, fuel_price_per_liter)
        cost2 = calculate_fuel_cost(distance, user2.fuel_efficiency, fuel_price_per_liter)
        
        cost_data.append({
            'user_id_person1': user1.user_id,
            'person1_name': user1.name,
            'car_model_person1': user1.car_model,
            'fuel_efficiency_person1': user1.fuel_efficiency,
            'fuel_cost_person1': cost1,
            'user_id_person2': user2.user_id,
            'person2_name': user2.name,
            'car_model_person2': user2.car_model,
            'fuel_efficiency_person2': user2.fuel_efficiency,
            'fuel_cost_person2': cost2,
            'total_cost': cost1 + cost2,
            'common_days': row['common_days']
        })
    
    return pd.DataFrame(cost_data)


users = [
    User(1, "Alice", "Sedan", 15, 100.0, 13.7, 100.2, 13.8, "Start A", "End A", 5, 30, "08:00", "09:00", ["Monday", "Wednesday"]),
    User(2, "Bob", "SUV", 10, 100.1, 13.75, 100.25, 13.85, "Start B", "End B", 6, 35, "08:15", "09:15", ["Monday", "Friday"]),
    User(3, "Charlie", "Hatchback", 18, 101.0, 14.0, 101.1, 14.1, "Start C", "End C", 8, 45, "07:45", "08:45", ["Tuesday", "Wednesday"]),
    User(4, "Sally", "BMW", 18, 101.0, 14.0, 101.1, 14.1, "Start C", "End C", 8, 45, "07:45", "08:45", ["Thursday", "Sunday"]),
    User(5, "Jane", "Toyota", 18, 101.0, 14.0, 101.1, 14.1, "Start C", "End C", 8, 45, "07:45", "08:45", ["Tuesday", "Thursday"]),]

matches_df = find_matches(users, distance_threshold=13.0, time_threshold=60)
cost_df = create_cost_table(users, matches_df, fuel_price_per_liter=40)

display(cost_df)
display(matches_df)

combined_df = pd.merge(matches_df, cost_df, on=['user_id_person1', 'user_id_person2'])


pd.set_option('display.float_format', '{:.2f}'.format)


display(combined_df)
