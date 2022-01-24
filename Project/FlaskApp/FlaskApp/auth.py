#autoryzacja 
from xmlrpc.client import DateTime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
#bazadanych
from database import db, User, ResetToken
from datetime import datetime
#walidacja
from valid import passwordValidation, loginVallidation, emailVallidation
#generacja tokenu i wysłąnie mail'a
import random
import string
from flask_mail import Mail, Message

auth = Blueprint('auth', __name__)
mail = Mail()

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    #pobranie danych formularza
    login = request.form.get('login')
    password = request.form.get('password')

    #walidacja
    if not passwordValidation(password):
        flash('Bad password format. 1 lowercase, 1 uppercase, 1 number, at least 8 character')
        return redirect(url_for('auth.login'))
    if not loginVallidation(login):
        flash('Bad login format. Only numbers and letters avaible.')
        return redirect(url_for('auth.login'))

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

    #walidacja
    if not passwordValidation(password):
        flash('Bad password format. 1 lowercase, 1 uppercase, 1 number, at least 8 character')
        return redirect(url_for('auth.login'))
    if not loginVallidation(login):
        flash('Bad login format. Only numbers and letters avaible.')
        return redirect(url_for('auth.login'))
    if not emailVallidation(email):
        flash('Bad email format.')
        return redirect(url_for('auth.login'))

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


#zmiana hasła użytkownika zalogowanego
@auth.route('/password/reset')
@login_required
def passwordResetPassword():
    return render_template('passwordReset.html')

@auth.route('/password/reset', methods=['POST'])
@login_required
def passwordResetPassword_post():
    #pobranie danych formularza
    passwordOld = request.form.get('passwordOld')
    passwordNew = request.form.get('passwordNew')
    password = request.form.get('passwordNewRepeated')

    #walidacja
    if not passwordNew == password:
            flash('Please check inserted password and try again.')
            return redirect(url_for('auth.passwordResetPassword'))

    #sprawdzenie użytkownika
    user = User.query.filter(User.id == current_user.id).first()
    if not user:
        flash('Error Occured')
        return redirect(url_for('auth.passwordResetPassword'))
    if not user or not user.checkPassword(passwordOld):
        flash('Please check inserted password and try again.')
        return redirect(url_for('auth.passwordResetPassword'))

    user.set_password(password)
    db.session.commit()

    logout_user()
    return redirect(url_for('auth.login'))

#Odzyskiwanie hasła w przypadku utraty

@auth.route('/password/requireNew')
def passwordResetReq():
    return render_template('passwordResetEmail.html')

@auth.route('/password/requireNew', methods=['POST'])
def passwordResetReq_post():
    login = request.form.get('login')

    #sprawdzenie użytkownika
    user = User.query.filter(User.login == login).first()
    if not user:
        flash('Error Occured')
        return redirect(url_for('auth.passwordResetReq'))

    _token = ''.join(random.choices(string.ascii_lowercase, k=32))

    token = ResetToken(
        userID = user.id,
        token = _token,
        DataCreate = datetime.now()
    )
    db.session.add(token)
    db.session.commit()

    flash('Reset password on\n/password/reset/' + token.token + '\n Mail could be sent to:\n' + user.email)
    msg = Message('Reset password', sender = 'rafal.gulewski.stud@interia.pl', recipients = ['rafalgulewski@gmail.com'])
    msg.body = 'Reset password on\n/password/reset/' + token.token + '\n Mail could be sent to:\n' + user.email
    mail.send(msg)
    return redirect(url_for('auth.passwordResetReq'))

#Strona do resetowania hasła
@auth.route('/password/reset/<token>')
def passwordResetPasswordToken(token):
    return render_template('passwordResetToken.html', token = token)

@auth.route('/password/tokenReset/<token>', methods=['POST'])
def passwordResetPasswordToken_post(token):
    #token = request.form.get('token')
    password = request.form.get('password')
    passwordNew = request.form.get('passwordNew')

    if password != passwordNew:
        flash('Passwords aren\'t the same')
        return redirect(url_for('auth.passwordResetPassword', token=token))

    _token = ResetToken.query.filter(ResetToken.token == token).first()
    if not _token:
        flash('Token Expired')
        return redirect(url_for('auth.passwordResetPassword', token=token))
    user = User.query.filter((ResetToken.token == token) & (User.id == ResetToken.userID)).first()
    if not user:
        flash('Error Occured')
        return redirect(url_for('auth.passwordResetPassword', token=token))

    user.set_password(password)
    ResetToken.query.filter(ResetToken.token == token).delete()
    db.session.commit()
    
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))