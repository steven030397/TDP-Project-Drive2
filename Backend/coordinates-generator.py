import requests
import random
from datetime import datetime, timedelta
import faker
from faker import Faker
import mysql.connector
import requests
import random


numUser = 95


#####residential and business address api
def fetch_all_records(api_url, limit, offset=0):
    params = {'limit': limit, 'offset': offset}
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        records = data.get('result', {}).get('records', [])
        return records
    else:
        print("Error:", response.status_code)
        return []

def get_random_record(records, address_column_name):
    if records:
        random_record = random.choice(records)
        lat = float(random_record.get('latitude', 0))
        long = float(random_record.get('longitude', 0))
        address = random_record.get(address_column_name, 'Unknown address')
        return lat, long, address
    else:
        print("No records available.")
        return None

# Example usage
vic_residential_api_url = 'https://discover.data.vic.gov.au/api/3/action/datastore_search?resource_id=6ec3d5b8-5a3c-48b9-9256-f46ef578eaa1'
vic_business_api_url = 'https://discover.data.vic.gov.au/api/3/action/datastore_search?resource_id=5a781178-9508-4628-ba9c-dc72a156ef99'

residential_records = []
limit = 32000
offset = 0
while True:
    records = fetch_all_records(vic_residential_api_url, limit, offset)
    if not records:
        break
    residential_records.extend(records)
    offset += limit

business_records = []
limit = 32000
offset = 0
while True:
    records = fetch_all_records(vic_business_api_url, limit, offset)
    if not records:
        break
    business_records.extend(records)
    offset += limit

print(len(residential_records))
print(len(business_records))

def filter_records(records):
    filtered_records = []
    for record in records:
        lat_str = record.get('latitude')
        long_str = record.get('longitude')
        
        try:
            # Check if latitude and longitude are valid floats
            lat = float(lat_str) if lat_str is not None else None
            long = float(long_str) if long_str is not None else None
            
            # Only include records with valid lat and long
            if lat is not None and long is not None:
                filtered_records.append(record)
        except ValueError:
            # Skip records with invalid float values
            continue
    
    return filtered_records

# Filter out records with missing or invalid coordinates
filtered_residential_records = filter_records(residential_records)
filtered_business_records = filter_records(business_records)

print("Filtered Residential Records:", len(filtered_residential_records))
print("Filtered Business Records:", len(filtered_business_records))

# Your Google API key
API_KEY = 'AIzaSyBWW9zve7B8Zy7HM2mHDtNz8HXED_HiFlg'

def get_route_distance(origin, destination):
    """Function to get route distance between origin and destination using Google Maps Directions API."""
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY}'
    
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        # Extract distance and duration from the response
        distance = data['routes'][0]['legs'][0]['distance']['value']  # distance in meters
        duration = data['routes'][0]['legs'][0]['duration']['value']  # duration in seconds
        return distance, duration
    else:
        print(f"Error fetching directions: {data['status']}")
        return None, None

# # Function to get random coordinates within a radius around a specified location
# def get_random_coordinates(lat, lng, radius=5000, place_type="point_of_interest", max_results=10):
#     url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
#     params = {
#         'location': f"{lat},{lng}",
#         'radius': radius,  # In meters, can change based on how wide an area you want to search
#         'type': place_type,  # Types like 'restaurant', 'point_of_interest', 'store', etc.
#         'key': API_KEY
#     }
    
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         places = response.json().get('results', [])
#         if not places:
#             return None
        
#         # Select a random place from the results
#         place = random.choice(places)
        
#         place_name = place.get('name')
#         lat = place['geometry']['location']['lat']
#         lng = place['geometry']['location']['lng']
#         address = place.get('vicinity', 'Unknown location')
        
#         return lat, lng, place_name, address
#     else:
#         print("Error:", response.status_code)
#         return None

# # List of office place types to choose from
# ###home_place_types = ["postcode"]


# # List of office place types to choose from
# office_place_types = ["restaurant", "bar", "cafe", "store", "shopping_mall", "airport", 
#                       "gym", "hospital", "pharmacy", "bank", "school", "university", 
#                       "hotel", "police", "accounting", "post_office"]

# Function to generate weekly mileage percentage based on nrow
def calculate_weekly_mileage(nrow):
    base_percentage = random.uniform(20, 40)  # Base mileage percentage
    # More rows means higher percentage with a max of around 100%
    return min(100, base_percentage + (nrow * random.uniform(10, 20)))

# Function to generate weekly fuel spent based on nrow
def calculate_weekly_fuel_spent(nrow):
    base_fuel_cost = random.uniform(50, 100)  # Base fuel spent
    # More rows means higher fuel cost, with a max of around $300
    return min(300, base_fuel_cost + (nrow * random.uniform(20, 50)))

# Function to generate a random time within a given range
def generate_random_time(start_hour, end_hour):
    hour = random.randint(start_hour, end_hour)
    minute = random.choice([0, 15, 30, 45])
    return f"{hour:02d}:{minute:02d}"

# Function to add time intervals (e.g., travel time between home and office)
def add_time(base_time, min_minutes, max_minutes):
    time_format = "%H:%M"
    base_time_obj = datetime.strptime(base_time, time_format)
    added_minutes = timedelta(minutes=random.randint(min_minutes, max_minutes))
    new_time_obj = base_time_obj + added_minutes
    return new_time_obj.strftime(time_format)

# Function to assign random days of the week
def assign_days(nrow):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return random.sample(days, nrow)  # Pick nrow distinct days

# List to store generated data
route_data = []

# # Establish MySQL connection
connection = mysql.connector.connect(
    host="db4free.net",
    port="3306",
    user="steven3397",
    password="pass123word", 
    database="drive2_db"
)

my_cursor = connection.cursor()


# Create the SQL query
sql_query = """
SELECT MAX(user_id) FROM users;
"""

# Execute the query
my_cursor.execute(sql_query)

result = my_cursor.fetchone()

print(result[0])

if(result[0] == -1):
    k = 0
else:
    k = result[0]

print(k)

# Commit the changes
connection.commit()

# Close the connection
my_cursor.close()
connection.close()


# Generate numUser user pairs
for user_id in range(k+1, numUser+k+1):
    
    ###home_place_type = random.choice(home_place_types)
    ###home_location = get_random_coordinates(-37.8136, 144.9631, radius=50000, place_type=home_place_type)
    
    # Get a random office location (from one of the office types)
    # office_place_type = random.choice(office_place_types)
    # office_location = get_random_coordinates(-37.8136, 144.9631, radius=20000, place_type=office_place_type)
    
    ###if home_location and office_location:
        ###home_lat, home_long, home_name, home_address = home_location
        ###office_lat, office_long, office_name, office_address = office_location

    
    office_lat, office_long, office_address = office_location = get_random_record(filtered_business_records, 'business_address')
    
    home_lat, home_long, home_address = get_random_record(filtered_residential_records, 'building_address')

    # Combine latitude and longitude into a single string
    origin = f"{home_lat},{home_long}"
    destination = f"{office_lat},{office_long}"

    # Get actual route distance and duration
    google_actual_distance, google_actual_duration = get_route_distance(origin, destination)

    # Assign a random number of rows (1 to 5)
    nrow = random.randint(1, 5)

    # Calculate weekly mileage percentage and fuel spent based on nrow
    weekly_mileage_percentage = calculate_weekly_mileage(nrow)
    weekly_fuel_spent = calculate_weekly_fuel_spent(nrow)
    
    # Assign random days of the week for the routes
    travel_days = assign_days(nrow)

    # Calculate weekly mileage percentage and fuel spent based on nrow
    weekly_mileage_percentage = calculate_weekly_mileage(nrow)
    weekly_fuel_spent = calculate_weekly_fuel_spent(nrow)
    
    # Duplicate the row nrow times
    for i in range(nrow):

        # Generate random times for leaving home and returning
        leave_start_time = generate_random_time(6, 10)  # Leave home between 6:00 AM and 10:00 AM
        arrive_end_time = add_time(leave_start_time, 30, 90)  # Arrive at the office within 30-90 minutes
        
        leave_end_time = generate_random_time(15, 19)  # Leave office between 3:00 PM and 7:00 PM
        arrive_start_time = add_time(leave_end_time, 30, 90)  # Arrive home within 30-90 minutes
        
        route_data.append({
            'user_id': user_id,     
            'start_latitude': home_lat,
            'start_longitude': home_long,
            'start_point_name': home_address,
            'end_latitude': office_lat,
            'end_longitude': office_long,
            'end_point_name': office_address,
            'weekly_mileage_percentage': weekly_mileage_percentage,
            'weekly_fuel_spent': weekly_fuel_spent,
            'travel_day': travel_days[i],
            'leave_start_time': leave_start_time,
            'arrive_end_time': arrive_end_time,
            'leave_end_time': leave_end_time,
            'arrive_start_time': arrive_start_time,
            'google_actual_distance': google_actual_distance
        })

# Display generated data for verification
#for route in route_data:
 #   print(route)





# # Establish MySQL connection
connection = mysql.connector.connect(
    host="db4free.net",
    port="3306",
    user="steven3397",
    password="pass123word", 
    database="drive2_db"
)

my_cursor = connection.cursor()

fake = Faker()

# Function to generate random gender
def random_gender():
    return random.choice(['Male', 'Female', 'Other'])

# Function to generate random 'has_car' value
def random_has_car():
    return random.choice([True, False])

def check_existing_user(cursor, username, email):
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s OR email = %s", (username, email))
    return cursor.fetchone()[0] > 0

# Establish MySQL connection
connection = mysql.connector.connect(
    host="db4free.net",
    port="3306",
    user="steven3397",
    password="pass123word", 
    database="drive2_db"
)

my_cursor = connection.cursor()

# Generate users
for user_id in range(k+1, numUser+k+1):
    unique = False
    while not unique:
        username = fake.user_name()
        email = fake.email()
        
        # Check if username or email already exists
        if not check_existing_user(my_cursor, username, email):
            unique = True
            password = fake.password(length=10)
            first_name = fake.first_name()
            middle_name = fake.first_name()
            last_name = fake.last_name()
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=70)
            gender = random_gender()
            phone_number = fake.phone_number()
            address = fake.address().replace("\n", " ")
            state = fake.state()
            driver_license_number = fake.license_plate()
            has_car = random_has_car()
            
            # Create the SQL query
            sql_query = """
            INSERT INTO users 
            (user_id, username, password, email, first_name, middle_name, last_name, date_of_birth, gender, phone_number, address, state, driver_license_number, has_car)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Data tuple to insert
            user_data = (user_id, username, password, email, first_name, middle_name, last_name, date_of_birth, gender, phone_number, address, state, driver_license_number, has_car)
            
            # Execute the query
            my_cursor.execute(sql_query, user_data)

# Commit the changes
connection.commit()

# Close the connection
my_cursor.close()
connection.close()

print("ALL users inserted into the database successfully.")





# Establish connection
connection = mysql.connector.connect(
    host = "db4free.net",
    port = "3306",
    user = "steven3397",
    password = "pass123word", 
    database = "drive2_db"
)

# Create a cursor object
my_cursor = connection.cursor()

# # Function to generate the SQL INSERT INTO query
# def generate_insert_query():
#     return f"""
#     query = """
#     INSERT INTO route
#     (user_id, start_latitude, start_longitude, start_point_name, 
#     end_latitude, end_longitude, end_point_name, 
#     leave_start_time, arrive_end_time, leave_end_time, arrive_start_time, 
#     travel_day, weekly_mileage_percentage, weekly_fuel_spent) 
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """


# Generate SQL for all rows
try:
    # Parameterized query to insert data
    query = """
        INSERT INTO route
        (user_id, start_latitude, start_longitude, start_point_name, 
        end_latitude, end_longitude, end_point_name, 
        leave_start_time, destination_arrival_time, destination_departure_time, arrive_start_time, 
        travel_day, weekly_mileage_percentage, weekly_fuel_spent, google_actual_distance) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Execute query with parameters
    for route in route_data:
        my_cursor.execute(query, (
            route['user_id'], 
            route['start_latitude'], 
            route['start_longitude'], 
            route['start_point_name'], 
            route['end_latitude'], 
            route['end_longitude'], 
            route['end_point_name'], 
            route['leave_start_time'], 
            route['arrive_end_time'], 
            route['leave_end_time'], 
            route['arrive_start_time'], 
            route['travel_day'], 
            route['weekly_mileage_percentage'], 
            route['weekly_fuel_spent'],
            route['google_actual_distance']
        ))
    # Commit the transaction after all queries
    connection.commit()
    print("All data has been inserted successfully!")

except mysql.connector.Error as err:
    print(f"Error: {err}")
    connection.rollback()  # Rollback in case of error

finally:
    # Close the cursor and the connection
    my_cursor.close()
    connection.close()











