import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd  # Import pandas
import folium

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

##############################

# Define the query to select all rows from the 'matching_data' table
query = """
SELECT 
    *
FROM 
    matching_data
"""

# Execute the query
cursor.execute(query)

# Fetch all rows from the result
data = cursor.fetchall()
match_data = pd.DataFrame(data)

#############################

# Define the query to select all rows from the 'route' table
query = """
SELECT 
    *
FROM 
    route
"""

# Execute the query
cursor.execute(query)

# Fetch all rows from the result
data = cursor.fetchall()
route_data = pd.DataFrame(data)

# Close the cursor and connection
cursor.close()
connection.close()



import folium
from folium.plugins import MarkerCluster

# Calculate bounds for the map to focus on the relevant area
bounds = [[route_data['start_latitude'].min(), route_data['start_longitude'].min()],
          [route_data['start_latitude'].max(), route_data['start_longitude'].max()]]

# Create a base map with bounds
m = folium.Map(location=[(bounds[0][0] + bounds[1][0]) / 2, (bounds[0][1] + bounds[1][1]) / 2], zoom_start=12)

# Create a MarkerCluster object
marker_cluster = MarkerCluster().add_to(m)

# Add home and office markers to the cluster
for _, row in route_data.iterrows():
    folium.Marker(
        location=[row['start_latitude'], row['start_longitude']],
        popup="Home",
        icon=folium.Icon(color='blue', icon='home', icon_size=(15, 15))
    ).add_to(marker_cluster)
    
    folium.Marker(
        location=[row['end_latitude'], row['end_longitude']],
        popup="Office",
        icon=folium.Icon(color='red', icon='briefcase', icon_size=(15, 15))
    ).add_to(marker_cluster)

# Save map to an HTML file
m.save('user_locations_map.html')
