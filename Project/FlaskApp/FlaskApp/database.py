#Bazadanych
import random
import string
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from config import Config

db = SQLAlchemy()

#UserMixin - flask wykorzystuje klase do logowania (niezbedne pola i funkcje)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), index=True, unique=True)
    password = db.Column(db.String())
    salt = db.Column(db.String())
    email = db.Column(db.String(), index=True, unique=True)

    def set_password(self, password):
        #zmiana na bajty
        _password = password.encode()
        _salt = bcrypt.gensalt()
        _hash = bcrypt.hashpw(_password + Config.PEPPER, _salt)
        #zapisanie w bazie
        self.salt = _salt.decode()
        self.password = _hash.decode()

    def checkPassword(self, password):
        _salt = self.salt.encode()
        _password = password.encode()
        _checkedHash = bcrypt.hashpw(_password + Config.PEPPER, _salt)
        return _checkedHash.decode() == self.password

    def __repr__(self):
        return f'{self.login}'


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())
    isPublic = db.Column(db.Boolean())
    userID = db.Column(db.String(), db.ForeignKey('user.login'))

class ConnectorNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    noteID = db.Column(db.Integer, db.ForeignKey('note.id'))

def fillDefault():
    user = User(
        login='Tester', 
        email='email@test.pl')
    user.set_password('password')
    db.session.add(user)

    user = User(
        login='Tester2', 
        email='email2@test.pl')
    user.set_password('password')
    db.session.add(user)

    note = Note(
        title='Testowa notatka', 
        text='To jest testowa notatka - notatka jest ustawiona jako publiczna',
        isPublic=True,
        userID='Tester')
    db.session.add(note)

    note = Note(
        title='Testowa notatka 2', 
        text='To jest testowa notatka - notatka jest ustawiona jako prywanta',
        isPublic=False,
        userID='Tester')
    db.session.add(note)

    note = Note(
        title='Testowa notatka 3', 
        text='To jest testowa notatka publiczna 2 - notatka jest ustawiona jako publiczna',
        isPublic=True,
        userID='Tester2')
    db.session.add(note)

    note = Note(
        title='Only user 2', 
        text='To jest testowa notatka prywatna testera 2 - nikt inny jej nie widzi',
        isPublic=False,
        userID='Tester2')
    db.session.add(note)

    note = Note(
        title='Testowa notatka prywatna dla wiekszosci 3', 
        text='To jest testowa notatka prywatna testera 2 - notatka jest widoczna dla drugiego użytkownika',
        isPublic=False,
        userID='Tester2')
    db.session.add(note)
    
    db.session.commit()

    noteID = Note.query.order_by(Note.id.desc()).first()
    connect = ConnectorNote(
        noteID = noteID.id,
        userID = 1
    )
    db.session.add(connect)
    db.session.commit()