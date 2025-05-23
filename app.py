from flask import Flask, render_template,render_template_string, request, redirect, url_for, session, flash  
from flask_sqlalchemy import SQLAlchemy  
from werkzeug.security import generate_password_hash, check_password_hash  
from functools import wraps 
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file 
import os

SITE_KEY = os.getenv('SITE_KEY')  # Get the site key from environment variables

app = Flask(__name__)  
app.secret_key = SITE_KEY  # Change this to a random secret key in production  
  
# SQLite database configuration  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)  
  
# User model  
class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(80), unique=True, nullable=False)  
    password_hash = db.Column(db.String(128), nullable=False)  
  
    def set_password(self, password):  
        self.password_hash = generate_password_hash(password)  
  
    def check_password(self, password):  
        return check_password_hash(self.password_hash, password)  
  
# Create database tables if not exist  
with app.app_context():  
    db.create_all()  
  
# Login required decorator  
def login_required(f):  
    @wraps(f)  
    def decorated_function(*args, **kwargs):  
        if 'user_id' not in session:  
            flash('Please login to access this page.', 'warning')  
            return redirect(url_for('login'))  
        return f(*args, **kwargs)  
    return decorated_function  
  
# Routes and views  
  
@app.route('/')  
@login_required  
def home():  
    user = User.query.get(session['user_id'])  
    return render_template('home.html', user=user)
 
  
@app.route('/login', methods=['GET', 'POST'])  
def login():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password']  
  
        user = User.query.filter_by(username=username).first()  
        if user and user.check_password(password):  
            session['user_id'] = user.id  
            flash('Logged in successfully.', 'success')  
            return redirect(url_for('home'))  
        else:  
            flash('Invalid username or password.', 'danger')  
  
    return render_template('login.html')
  
@app.route('/register', methods=['GET', 'POST'])  
def register():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password']  
  
        if User.query.filter_by(username=username).first():  
            flash('Username already exists. Please choose a different one.', 'danger')  
        else:  
            new_user = User(username=username)  
            new_user.set_password(password)  
            db.session.add(new_user)  
            db.session.commit()  
            flash('Registration successful. You can now log in.', 'success')  
            return redirect(url_for('login'))  
  
    return render_template('register.html')
    
  
  
@app.route('/logout')  
@login_required  
def logout():  
    session.pop('user_id', None)  
    flash('You have been logged out.', 'info')  
    return redirect(url_for('login'))  
  
if __name__ == '__main__':  
    app.run(debug=True)  

