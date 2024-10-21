from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# replace with non-local database Postgresql
connection = mysql.connector.connect(
    host = "db4free.net",
    port="3306",
    user="steven3397",
    password = "pass123word", 
    database="drive2_db")


my_cursor=connection.cursor()
app = Flask(__name__) ## this is the default, it functions

app.secret_key = "super secret key"

@app.route("/")
def index():
    # Get the source query parameter
    source = request.args.get('source')

    # Clear all session data
    session.clear()

    # Flash messages based on the source
    if source == 'logout':
        flash('You have been logged out successfully.', 'success')
    elif source == 'registered':
        flash('Registration successful! Please log in.', 'success')
    else:
        flash('Welcome to the homepage.', 'info')

    return render_template("index.html")

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Connect to MySQL Database
        conn = mysql.connector.connect(
            host = "db4free.net",
            port="3306",
            user="steven3397",
            password = "pass123word", 
            database="drive2_db")
        cursor = conn.cursor()

        # Check if the user exists in the database by email
        cursor.execute("SELECT user_id, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            user_id, hashed_password = user # unpacking user, assigning both values to tuples values

            # Verify the password
            if True:
            #if check_password_hash(hashed_password, password):
                # Password is correct, log the user in
                session['user_id'] = user_id
                session['email'] = email
                flash('Logged in successfully!')

                cursor.execute("SELECT first_name, middle_name, last_name FROM users WHERE user_id = %s", (user_id,))
                names = cursor.fetchone()
                first_name, middle_name, last_name = names
                session['first_name'] = first_name
                session['middle_name'] = middle_name
                session['last_name'] = last_name

                return redirect(url_for('home'))
            else:
                flash('Invalid email or password. Please try again.')
        else:
            flash('Email does not exist. Please register first.')

        conn.close()
    return render_template("login.html")


@app.route('/consent',methods=['GET', 'POST'])
def consent():
    if request.method == 'POST':
        return redirect(url_for('register'))
    return render_template("consent.html")   

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collect data from the form
        session['first_name'] = request.form.get('first-name')
        session['middle_name'] = request.form.get('middle-name')
        session['last_name'] = request.form.get('last-name')
        session['dob'] = request.form.get('dob')
        session['gender'] = request.form.get('gender')
        session['phone'] = request.form.get('phone')
        session['address'] = request.form.get('address')
        session['state'] = request.form.get('state')
        session['driver_license'] = request.form.get('driver-license')

        connection = mysql.connector.connect(
        host = "db4free.net",
        port="3306",
        user="steven3397",
        password = "pass123word", 
        database="drive2_db")
        
        # Check if phone number or driver license already exists in database
        my_cursor = connection.cursor()
        my_cursor.execute('SELECT COUNT(*) FROM users WHERE phone_number = %s', (session['phone'],))
        phone_exists = my_cursor.fetchone()[0] > 0

        if phone_exists:
            flash('Phone number already exists. Please use a different phone number.')
            return redirect(url_for('register'))

        my_cursor.execute('SELECT COUNT(*) FROM users WHERE driver_license_number = %s', (session['driver_license'],))
        license_exists = my_cursor.fetchone()[0] > 0

        if license_exists:
            flash('Driver license already exists. Please use a different driver license.')
            return redirect(url_for('register'))

        # Proceed to the next step
        return redirect(url_for('vehicle'))

    return render_template("register.html")

@app.route('/test-personal')
def test_personal():
    # Initialize a dictionary to hold session data
    session_data = {
        'First Name': session.get('first_name'),
        'Middle Name': session.get('middle_name'),
        'Last Name': session.get('last_name'),
        'Date of Birth': session.get('dob'),
        'Gender': session.get('gender'),
        'Phone': session.get('phone'),
        'Address': session.get('address'),
        'State': session.get('state'),
        'Driver License': session.get('driver_license'),
        'Vehicles': session.get('vehicles', 'No vehicle data found'),
        'Home Address': session.get('home_address'),
        'Office Address': session.get('office_address'),
        'Percentage Mileage': session.get('percentage_mileage'),
        'Fuel Cost': session.get('fuel_cost'),
        'Username': session.get('username'),
        'Email': session.get('email'),
        'Email Confirmed': session.get('confirm_email'),
        'Password': session.get('password'),
        'Password Confirmed': session.get('confirm_password'),
        'Username': session.get('user_id'),
        'Home Latitude': session.get('home_lat'),
        'Home Longitude': session.get('home_long'),
        'Office Latitude': session.get('office_lat'),
        'Office Longitude': session.get('office_long'),
        'Google Actual Distance': session.get('google_actual_distance')
    }

    # Add dynamic days data
    days_data = {}
    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        leave_home = session.get(f'{day}_leave_home')
        arrive_office = session.get(f'{day}_arrive_office')
        leave_office = session.get(f'{day}_leave_office')
        arrive_home = session.get(f'{day}_arrive_home')

        if leave_home or arrive_office or leave_office or arrive_home:
            days_data[day.capitalize()] = {
                'Leave Home': leave_home,
                'Arrive Office': arrive_office,
                'Leave Office': leave_office,
                'Arrive Home': arrive_home
            }

    # Include days data in session_data
    session_data['Days Data'] = days_data

    return session_data


@app.route('/vehicle', methods=['GET', 'POST'])
def vehicle():
    if request.method == 'POST':
        has_car = request.form.get('hasCar')

        if has_car == 'yes':
            # Collect vehicle details from the form
            session['vehicles'] = []
            brands = request.form.getlist('brand[]')
            models = request.form.getlist('model[]')
            years = request.form.getlist('year[]')
            registrations = request.form.getlist('registration[]')
            garage_locations = request.form.getlist('garage-location[]')

            if len(brands) == len(models) == len(years) == len(registrations) == len(garage_locations):
                for i in range(len(brands)):
                    vehicle = {
                        'brand': brands[i],
                        'model': models[i],
                        'year': years[i],
                        'registration': registrations[i],
                        'garage_location': garage_locations[i]
                    }
                    session['vehicles'].append(vehicle)
            else:
                flash('Mismatch in vehicle details. Please check your entries.')
                return redirect(url_for('vehicle'))

        # Proceed to the next step (e.g., finalize registration)
        return redirect(url_for('commute'))

    return render_template("vehicle.html")

@app.route('/commute', methods=['GET', 'POST'])
def commute():
    if request.method == 'POST':
        # Store individual form fields in the session
        session['home_address'] = request.form.get('home-address')
        session['office_address'] = request.form.get('office-address')
        session['home_lat'] = request.form.get('lat1')
        session['home_long'] = request.form.get('lng1')
        session['office_lat'] = request.form.get('lat2')
        session['office_long'] = request.form.get('lng2')
        session['google_actual_distance'] = request.form.get('google_actual_distance')
        
        # Store selected days and times
        days = request.form.getlist('days[]')
        for day in days:
            session[f'{day.lower()}_leave_home'] = request.form.get(f'{day.lower()}-leave-home')
            session[f'{day.lower()}_arrive_office'] = request.form.get(f'{day.lower()}-arrive-office')
            session[f'{day.lower()}_leave_office'] = request.form.get(f'{day.lower()}-leave-office')
            session[f'{day.lower()}_arrive_home'] = request.form.get(f'{day.lower()}-arrive-home')
        
        # Store weekly mileage and fuel cost
        session['percentage_mileage'] = request.form.get('weekly-mileage')
        session['fuel_cost'] = request.form.get('weekly-fuel-cost')

        return redirect(url_for('credentials'))

    return render_template('commute.html')






@app.route('/credentials' ,methods=['GET', 'POST'])
def credentials():
    if request.method == 'POST':
    # Extract and store form data in the session
        session['username'] = request.form.get('username')
        session['email'] = request.form.get('email')
        session['confirm_email'] = request.form.get('confirm-email')
        session['password'] = request.form.get('password')
        session['confirm_password'] = request.form.get('confirm-password')
        
        if session['email'] != session['confirm_email']:
            flash('Emails do not match. Please try again.')
            return redirect(url_for('credentials'))

        # Perform additional processing, such as validating passwords
        if session['password'] != session['confirm_password']:
            flash('Passwords do not match. Please try again.')
            return redirect(url_for('credentials'))

        if len(session['password']) < 8:
            flash('Password must be at least 8 characters long.')
            return redirect(url_for('credentials'))

        try:
            # Connect to MySQL Database
            connection = mysql.connector.connect(
                host = "db4free.net",
                port="3306",
                user="steven3397",
                password = "pass123word", 
                database="drive2_db")
            cursor = connection.cursor()
            connection.start_transaction()

            # Check if email already exists in the database
            cursor.execute("SELECT * FROM users WHERE email = %s", (session['email'],))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Email already exists. Please use a different email.')
                connection.rollback()
                connection.close()
                return redirect(url_for('credentials'))

            # Hash the password
            hashed_password = generate_password_hash(session['password'], method='pbkdf2:sha256')

            # Insert new user data into the MySQL database
            has_car = bool(session.get('vehicles')) and session.get('vehicles') != 'No vehicle data found'
            cursor.execute("""
                INSERT INTO users (username, password, email, first_name, middle_name, last_name, date_of_birth, gender, phone_number, address, state, driver_license_number, has_car, address_latitude, address_longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                session['username'], hashed_password, session['email'], session['first_name'],
                session['middle_name'], session['last_name'], session['dob'], session['gender'],
                session['phone'], session['address'], session['state'], session['driver_license'],
                has_car, session['home_lat'], session['home_long'] 
            ))
            print("User data inserted")

            # Get the new user ID
            new_user_id = cursor.lastrowid
            print(f"New User ID: {new_user_id}")

            # Insert vehicle data (one row per vehicle)
            vehicles = session.get('vehicles')
            if vehicles and vehicles != 'No vehicle data found':
                for vehicle in session['vehicles']:
                    cursor.execute("""
                        INSERT INTO vehicles (user_id, car_brand, car_model, car_year, license_plate, garage_address)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (new_user_id, vehicle['brand'], vehicle['model'], vehicle['year'], vehicle['registration'], vehicle['garage_location']))
                    print(f"Vehicle data inserted: {vehicle}")


            days_data = {}
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                leave_home = session.get(f'{day}_leave_home')
                arrive_office = session.get(f'{day}_arrive_office')
                leave_office = session.get(f'{day}_leave_office')
                arrive_home = session.get(f'{day}_arrive_home')

                if leave_home or arrive_office or leave_office or arrive_home:
                    days_data[day.capitalize()] = {
                        'Leave Home': leave_home,
                        'Arrive Office': arrive_office,
                        'Leave Office': leave_office,
                        'Arrive Home': arrive_home
                    }
            # Insert route data for each day (one row per day)
            for day, times in days_data.items():
                cursor.execute("""
                    INSERT INTO route (user_id, start_latitude, start_longitude, start_point_name, end_latitude, end_longitude, end_point_name, home_departure_time, destination_arrival_time, destination_departure_time, home_arrival_time, travel_day, weekly_mileage_percentage, weekly_fuel_spent, google_actual_distance)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    new_user_id, session['home_lat'], session['home_long'], session['home_address'], session['office_lat'], session['office_long'],
                    session['office_address'], times['Leave Home'], times['Arrive Office'], times['Leave Office'], times['Arrive Home'],
                    day, session['percentage_mileage'], session['fuel_cost'], session['google_actual_distance']
                ))
                print(f"Route data inserted for day: {day}")

            # Commit all the changes
            connection.commit()
            session['user_id'] = new_user_id
            print("Data committed")
            # Redirect to home after successful registration
            return redirect(url_for('index', source='registered'))

        except mysql.connector.Error as err:
            # Rollback in case of an error
            connection.rollback()
            flash(f"An error occurred: {err}")
            print(f"Error: {err}")

        finally:
            # Close the connection
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Connection closed")

    return render_template("credentials.html")  

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear all session data
    session.clear()
    
    # Redirect to the index page with a query parameter
    return redirect(url_for('index', source='logout'))



@app.route('/home' ,methods=['GET', 'POST'])
def home():

    conn = mysql.connector.connect(
            host = "db4free.net",
            port="3306",
            user="steven3397",
            password = "pass123word", 
            database="drive2_db")
    cursor = conn.cursor()


    my_id = session["user_id"]
    cursor.execute("SELECT user_id_person2, matched_day FROM matching_data WHERE user_id_person1 = %s", (my_id, ))
    id_of_your_match = cursor.fetchall()
    # Separate the data into two lists or sets of variables
    user_ids = [match[0] for match in id_of_your_match]  # List of all user_id_person2
    match_days = [match[1] for match in id_of_your_match]  # List of all matched_day

    # Store them separately in session
    session["MATCH_USER_IDS"] = user_ids
    session["MATCH_DAYS"] = match_days

    cursor.execute("SELECT user_id_person1, matched_day FROM matching_data WHERE user_id_person2 = %s",(my_id, ))
    id_of_your_match = cursor.fetchall()
    session["MATCH_TEST2"] = id_of_your_match

    cursor.execute("""SELECT users.username , gender 
    FROM matching_data 
    JOIN users ON matching_data.user_id_person2 = users.user_id 
    WHERE matching_data.user_id_person1 = %s""", (my_id, ))
    name_your_match = cursor.fetchall()
    session["NAME_TEST"] = name_your_match

    cursor.execute("""SELECT users.username , gender 
    FROM matching_data 
    JOIN users ON matching_data.user_id_person1 = users.user_id 
    WHERE matching_data.user_id_person2 = %s""", (my_id, ))
    name_your_match = cursor.fetchall()
    session["NAME_TEST2"] = name_your_match

    return render_template("home.html")

   
@app.route('/conversation' ,methods=['GET', 'POST'])
def conversation():
    return render_template("conversation.html") 

 
@app.route('/settings' ,methods=['GET', 'POST'])
def settings():
    return render_template("settings.html") 

@app.route('/dashboard' ,methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html") 



@app.route('/admin' ,methods=['GET', 'POST'])
def admin():
    return render_template("admin.html") 

@app.route('/admin2' ,methods=['GET', 'POST'])
def admin2():
    return render_template("admin2.html") 

@app.route('/admin3' ,methods=['GET', 'POST'])
def admin3():
    return render_template("admin3.html") 

if __name__ == "__main__": # __name__ is a special built-in Python variable
    app.run(debug = True)

