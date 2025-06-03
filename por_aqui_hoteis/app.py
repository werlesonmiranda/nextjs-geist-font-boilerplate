from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///por_aqui_hoteis.db'
db = SQLAlchemy(app)

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'hotel', or 'client'

# Create admin user
def create_admin():
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', password='admin', role='admin')
            db.session.add(admin)
            db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # In production, use proper password hashing
            login_user(user)
            flash('Logged in successfully.')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'hotel':
                return redirect(url_for('hotel_dashboard'))
            else:
                return redirect(url_for('client_dashboard'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.role == 'admin':
        flash('Access denied')
        return redirect(url_for('index'))
    return render_template('admin/dashboard.html')

if __name__ == '__main__':
    create_admin()
    app.run(debug=True, port=8000)
