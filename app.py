from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
db.init_app(app)

@app.before_request
def initialize():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('main'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Please choose a different username."

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            return redirect(url_for('main'))
        else:
            return "Invalid credentials. Please try again."
    
    return render_template('login.html')

@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
