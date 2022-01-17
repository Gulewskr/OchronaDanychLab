from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from database import db, User, fillDefault

#inicjalizacja
app = Flask(__name__)

#klucz do szyfrowania sesji użytkownika
app.config['SECRET_KEY'] = 'secret-key-goes-here'
#adress do bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


#Tworzenie bazy danych
db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()
    fillDefault()

#Ścieżki związane z autoryzacją
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

#Ścieżki ogólne
from main import main as main_blueprint
app.register_blueprint(main_blueprint)

#manager logowań
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run()