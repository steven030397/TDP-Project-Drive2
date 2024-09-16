import mysql.connector

# Establish MySQL connection
connection = mysql.connector.connect(
    host="db4free.net",
    port="3306",
    user="steven3397",
    password="pass123word", 
    database="drive2_db"
)


# Create a cursor object using the connection
cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get results as dictionaries

# Define the query to select all rows from the 'route' table
query = "SELECT * FROM route"

# Execute the query
cursor.execute(query)

# Fetch all rows from the result
results = cursor.fetchall()

# Print each row
for row in results:
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()
