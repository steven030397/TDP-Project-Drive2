from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector

# replace with non-local database Postgresql
connection = mysql.connector.connect( 
    host = "127.0.0.1",
    port="3306",
    user="root",
    password = "", 
    database="tdp-steven")


my_cursor=connection.cursor()
app = Flask(__name__) ## this is the default, it functions

app.secret_key = "super secret key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login',methods = ['GET','POST'])
def login():
    msg = ''
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        my_cursor.execute('SELECT email FROM users WHERE email=%s AND password=%s', (email, password))
        record = my_cursor.fetchone()

        if record:
            return redirect(url_for('home'))
        else:#if username and password false  
            msg = 'Incorrect username/password. Try again!'
    return render_template("login.html", msg=msg)


# @app.route('/login',methods = ['GET','POST'])
# def login():
    # msg=''
    # if request.method=='POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     my_cursor.execute('SELECT usertype, username FROM users WHERE username=%s AND password=%s', (username, password))    
    #     record = my_cursor.fetchone()
    #     if record: 
    #         session['loggedin'] = True
    #         session['username'] = record[1]
    #         if record[0] == 'Student':  # Check if the user is a student
    #             return render_template("studentdashboard.html")  # Redirect to the student dashboard
    #         else: #record[0] == 'Teacher':   Check if the user is a teacher
    #             return render_template("teacherdashboard.html")  # Redirect to the teacher dashboard
    #         # return redirect(url_for('home'))

        # else:#if username and password false  
        #     msg = 'Incorrect username/password. Try again!'
    # return render_template("login.html",msg=msg)

# @app.route('/', methods=['GET', 'POST'])
# #register route
# def register():
#     if request.method == 'POST':
#         # Retrieve form data
#         username = request.form['username']
#         password = request.form['password']
       
#         # Check if username already exists in the database
#         my_cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
#         existing_user = my_cursor.fetchone()

#         if existing_user:
#             msg = 'Username already exists. Please choose a different username.'
#             return render_template('register.html', msg=msg)
#         else:
#             # Insert new user into the database
#             my_cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password,))
#             connection.commit()
#             msg = 'Registration successful! You can now log in.'
#             return render_template('login.html', msg=msg)
#     else:
#         # If request method is GET, render the registration form
#         return render_template('register.html')


@app.route('/consent',methods=['GET', 'POST'])
def consent():
    if request.method == 'POST':
        return redirect(url_for('register'))
    return render_template("consent.html")   

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('first-name')
        middlename = request.form.get('middle-name')
        lastname = request.form.get('last-name')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        address = request.form.get('address')
        state = request.form.get('state')
        driverlicense  = request.form.get('driver-license')
        
                # Debugging: Print retrieved data
        print('First Name:', firstname)
        print('Middle Name:', middlename)
        print('Last Name:', lastname)
        print('Date of Birth:', dob)
        print('Gender:', gender)
        print('Phone:', phone)
        print('Address:', address)
        print('State:', state)
        print('Driver License:', driverlicense)

        # Check if phone number is already in database
        my_cursor.execute('SELECT COUNT(*) FROM user_personal_details WHERE phone_number = %s', (phone,))
        phone_exists = my_cursor.fetchone()[0] > 0

        if phone_exists:
            flash('Phone number already exists. Please use a different phone number.')
            return redirect(url_for('register'))  # Adjust URL as needed

        # Check if driver license is already in database
        my_cursor.execute('SELECT COUNT(*) FROM user_personal_details WHERE driver_license_number = %s', (driverlicense,))
        license_exists = my_cursor.fetchone()[0] > 0

        if license_exists:
            flash('Driver license already exists. Please use a different driver license.')
            return redirect(url_for('register'))  # Adjust URL as needed

        # If both checks pass, insert data into database
        my_cursor.execute(
            'INSERT INTO user_personal_details (first_name, middle_name, last_name, date_of_birth, gender, phone_number, address, state, driver_license_number, has_car) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (firstname, middlename, lastname, dob, gender, phone, address, state, driverlicense, '0')
        )
        connection.commit()  # Commit changes to the database

        return redirect(url_for('vehicle')) 
    return render_template("register.html")



@app.route('/commute-data' ,methods=['GET', 'POST'])
def commute_data():
    return render_template("commute-data.html")   

@app.route('/vehicle' ,methods=['GET', 'POST'])
def vehicle():
    return render_template("vehicle.html")  

@app.route('/credentials' ,methods=['GET', 'POST'])
def credentials():
    return render_template("credentials.html")  

@app.route('/home' ,methods=['GET', 'POST'])
def home():
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

# #define the link with html
# @app.route('/studentdashboard')
# def studentdashboard():
#     return render_template("studentdashboard.html",username = session['username'])

# @app.route('/teacherdashboard')
# def teacherdashboard():
#     return render_template("teacherdashboard.html",username = session['username'])

# @app.route('/mathquiz') 
# def mathquiz():
#     return render_template("mathquiz.html")

# @app.route('/englishquiz')
# def englishquiz():
#     return render_template("englishquiz.html")

# @app.route('/biologyquiz')
# def biologyquiz():
#     return render_template("biologyquiz.html")


@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    # if my_cursor:
    #     my_cursor.close()
    # if connection:
    #     connection.close()
    return redirect(url_for('login'))
                 
if __name__ == "__main__": # __name__ is a special built-in Python variable
    app.run(debug = True)

