from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

try:
    # Load the CSV data into a DataFrame
    df = pd.read_csv('car.csv')
except FileNotFoundError:
    print("Error: CSV file not found. Please ensure 'car.csv' exists in the same directory as your Python script.")
    exit()

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/app', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        car_make = request.form['carMake']
        model_year = request.form['modelYear']

        try:
            # Filter the DataFrame with case-insensitive search (optional)
            filtered_data = df[(df['Car Make'].str.lower() == car_make.lower()) & (df['Model Year'] == int(model_year))]

            # Handle case where no results are found
            if filtered_data.empty:
                results = "No results found for that car make and model year."
            else:
                # Improve output formatting (optional)
                results = filtered_data.to_html(index=False, escape=False)  # Prevent HTML escaping for better table display
        except (ValueError, KeyError):  # Handle potential errors during filtering
            results = "Invalid input. Please enter a valid car make and model year."

        return render_template('index.html', car_make=car_make, model_year=model_year, results=results)
    else:
        # Clear previous search results
        return render_template('index.html', car_make='', model_year='', results='')

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for easier development