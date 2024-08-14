from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Path to store users and user information
user_data_file = 'users.json'
user_info_file = 'user_info.json'
pdf_folder = 'workouts'  # Folder where the PDFs are stored

# Function to read users data from JSON
def load_users():
    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            return json.load(file)
    return {}

# Function to save users data to JSON
def save_users(users):
    with open(user_data_file, 'w') as file:
        json.dump(users, file)

# Function to load user info data
def load_user_info():
    if os.path.exists(user_info_file):
        with open(user_info_file, 'r') as file:
            return json.load(file)
    return {}

# Function to save user info data
def save_user_info(user_info):
    with open(user_info_file, 'w') as file:
        json.dump(user_info, file)

# BMR calculation
def bmr_calc(weight, height, age):
    BMR = 88.362 + 13.397 * weight + 4.799 * height - 5.677 * age
    return BMR

# Calorie calculation based on goal and activity level
def cals(goal, level, bmr):
    levels_factors = [1.2, 1.375, 1.55, 1.725, 1.9]
    factor = levels_factors[level]
    goals = [0, -500, 500]  # 0: Maintain, -500: Cutting, 500: Bulking
    return bmr * factor + goals[goal]

# Macronutrients calculation based on calories, goal, and weight
def macros(cals, goal, weight):
    if goal == 0:  # Normal person
        proteins = round(weight * 0.8)
        fats = round(cals * 0.3 / 9)
        carbs = round((cals - (proteins * 4 + fats * 9)) / 4)
    else:  # New bodybuilder
        proteins = round(weight * 2)
        fats = round(cals * 0.3 / 9)
        carbs = round((cals - (proteins * 4 + fats * 9)) / 4)
    return {"proteins": proteins, "carbs": carbs, "fats": fats}

# Detect which PDF workout plan to download
def detect(goal, level):
    if level == 0:  # Beginner
        if goal == 0:  # Lose weight
            return "one.pdf"
        else:  # Gain weight
            return "two.pdf"
    else:  # Intermediate
        if goal == 0:  # Lose weight
            return "three.pdf"
        else:  # Gain weight
            return "four.pdf"

# Route for the sign-up and login page
@app.route('/')
def index():
    return render_template('index.html')

# Handle user sign-up
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not username or not email or not password:
        flash('Please fill out all fields!')
        return redirect(url_for('index'))

    users = load_users()

    if email in users:
        flash('User already exists! Please log in.')
        return redirect(url_for('index'))

    # Store the new user in the JSON file
    users[email] = {
        'username': username,
        'password': password
    }
    save_users(users)

    flash('Account created successfully! Please log in.')
    return redirect(url_for('index'))

# Handle user login
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    users = load_users()

    if email in users and users[email]['password'] == password:
        flash(f'Welcome back, {users[email]["username"]}!')
        return redirect(url_for('main'))
    else:
        flash('Invalid credentials. Please try again.')
        return redirect(url_for('index'))

# Route for the main user data input page
@app.route('/main')
def main():
    return render_template('main.html')

# Handle user data submission
@app.route('/submit_user_data', methods=['POST'])
def submit_user_data():
    weight = float(request.form.get('weight'))
    height = float(request.form.get('height'))
    age = int(request.form.get('age'))
    activity_level = int(request.form.get('activity_level')) - 1  # Adjust to 0-4

    goal_str = request.form.get('goal')
    goal_mapping = {'maintain': 0, 'cutting': 1, 'bulking': 2}
    goal = goal_mapping.get(goal_str.lower(), 0)  # Default to 'maintain'

    user_type = int(request.form.get('user_type'))  # 0: Normal, 1: New bodybuilder

    bmr = bmr_calc(weight, height, age)
    total_cals = cals(goal, activity_level, bmr)
    macro_data = macros(total_cals, user_type, weight)

    user_info = load_user_info()
    user_info['user_data'] = {
        'weight': weight,
        'height': height,
        'age': age,
        'activity_level': activity_level + 1,
        'goal': goal_str,
        'bmr': bmr,
        'total_cals': total_cals,
        'macros': macro_data
    }
    save_user_info(user_info)

    flash('User data has been successfully submitted!')
    return redirect(url_for('results'))

# Route to display the results
@app.route('/results')
def results():
    user_info = load_user_info().get('user_data', {})
    macros = user_info.get('macros', {})
    goal = user_info.get('goal')
    activity_level = user_info.get('activity_level')

    # Determine the workout PDF based on goal and level
    pdf_file = detect(goal, activity_level)
    return render_template('results.html', macros=macros, pdf_file=pdf_file)

# Route to download the selected PDF
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(pdf_folder, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
