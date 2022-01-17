from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from flask_login import UserMixin

import PyCrypto

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), index=True, unique=True)
    password = db.Column(db.String())
    salt = db.Column(db.String())
    email = db.Column(db.String(), index=True, unique=True)

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()

    def __repr__(self):
        return f'{self.login}'


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())
    isPublic = db.Column(db.Boolean())
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))

class ConnectorNote(db.Model):
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    noteID = db.Column(db.Integer, db.ForeignKey('note.id'))

def fill_db_with_values():
    tomas = User(
        login='Tomasz', email='tomasz@pw.edu.pl', lucky_number=17)
    tomas.set_password('Pa$$word')
    db.session.add(tomas)

    note = Note(title='Barista potrzebny', heading='Praca',
                body='W najbliższą sobotę będzie za duży ruch w kawiarni. Potrzebny barista na jeden dzień. Dobra stawka gwarantowana.',
                owner=tomas, public=False)
    db.session.add(note)

    note = Note(title='Wszyscy mile widziani', heading='Zaproszenie',
                body='Już niedługo odbędzie się ślub mojej córki. Wszyscy goście są mile widziani. Im nas więcej tym weselej.',
                owner=tomas, public=True)
    db.session.add(note)

    db.session.commit()