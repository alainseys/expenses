from flask import Flask, render_template, request, redirect, url_for, session, flash 
from datetime import datetime

from dotenv import load_dotenv
from functools import wraps
import os 
from extensions import db  # Import the SQLAlchemy instance from extensions.py

SITE_KEY = os.getenv('SITE_KEY')  # Get the site key from environment variables

app = Flask(__name__)  
app.secret_key = SITE_KEY  # Change this to a random secret key in production  
  
# SQLite database configuration  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
 
db.init_app(app)

# Import the models
from Models.user import User
from Models.entry import FinancialEntry

with app.app_context():
    db.create_all()  # Create database tables if they don't exist
#db = SQLAlchemy(app)  
  

  
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

@app.route('/entry', methods=['GET', 'POST'])
@login_required
def add_entry():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        description = request.form['description']
        entry_type = request.form['type']  # "income" or "expense"
        account = request.form['account']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')

        entry = FinancialEntry(
            user_id=session['user_id'],
            amount=amount,
            description=description,
            is_income=(entry_type == 'income'),
            account=account,
            date=date
        )
        db.session.add(entry)
        db.session.commit()
        flash('Entry added.', 'success')
        return redirect(url_for('report'))

    return render_template('add_entry.html')

@app.route('/report')
@login_required
def report():
    user_id = session['user_id']
    entries = FinancialEntry.query.filter_by(user_id=user_id).order_by(FinancialEntry.date.desc()).all()
    total = sum(e.amount if e.is_income else -e.amount for e in entries)

    return render_template('report.html', entries=entries, total=total)
  
@app.route('/logout')  
@login_required  
def logout():  
    session.pop('user_id', None)  
    flash('You have been logged out.', 'info')  
    return redirect(url_for('login'))  
  
if __name__ == '__main__':  
    app.run(debug=True)  

