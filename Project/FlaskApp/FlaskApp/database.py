#Bazadanych
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

#UserMixin - flask wykorzystuje klase do logowania (niezbedne pola i funkcje)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), index=True, unique=True)
    password = db.Column(db.String())
    salt = db.Column(db.String())
    email = db.Column(db.String(), index=True, unique=True)

    def set_password(self, password):
        self.password = sha256_crypt.hash(password)
        #self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

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
    tomas = User(
        login='Tester', 
        email='email@test.pl', 
        salt="1234")
    tomas.set_password('password')
    db.session.add(tomas)

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

    db.session.commit()