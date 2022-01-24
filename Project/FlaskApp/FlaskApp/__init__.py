from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from database import db, User, fillDefault
from config import Config

#inicjalizacja
app = Flask(__name__)

app.config['SECRET_KEY'] =  Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URL
app.config['MAIL_SERVER']= Config.MAIL_SERVER
app.config['MAIL_PORT'] = Config.MAIL_PORT
app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = Config.MAIL_USE_SSL

#Tworzenie bazy danych
db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()
    fillDefault()

#Ścieżki związane z autoryzacją
from auth import mail, auth as auth_blueprint
app.register_blueprint(auth_blueprint)
mail = Mail(app)

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