#autoryzacja 
from flask import Blueprint, render_template, redirect, url_for, request, flash
from database import User
from flask_login import login_user, login_required, logout_user
from database import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    #pobranie danych formularza
    login = request.form.get('login')
    password = request.form.get('password')

    #walidacja

    #sprawdzenie poprawności logowania
    user = User.query.filter(User.login == login).first()
    if not user or not user.checkPassword(password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    #zalogowanie
    login_user(user)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    #pobranie danych formularza
    email = request.form.get('email')
    login = request.form.get('name')
    password = request.form.get('password')

    #sprawdzenie czy użytkownik o podanym emailu lub loginie już istnieje
    user = User.query.filter((User.email == email) | (User.login == login)).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    #dodanie użytkownika do bazy danych
    new_user = User(email=email, login=login)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))