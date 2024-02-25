from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import app, db
from .models import User, Question, Category
import random
from sqlalchemy.sql import func

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/general-practice')
@login_required
def general_practice():
    questions = Question.query.order_by(func.random()).limit(10).all()
    return render_template('general_practice.html', questions=questions)

@app.route('/category-practice/<int:category_id>')
@login_required
def category_practice(category_id):
    questions = Question.query.filter_by(category_id=category_id).order_by(func.random()).limit(10).all()
    return render_template('category_practice.html', questions=questions, category_id=category_id)

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def question(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        selected_choice = request.form['choice']
        if selected_choice == question.correct_answer:
            flash('Correct!')
        else:
            flash('Incorrect!')
        return redirect(url_for('dashboard'))
    return render_template('question.html', question=question)