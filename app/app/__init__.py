from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from importlib import import_module
import flask_monitoringdashboard as dashboard

import logging
from logging.handlers import SMTPHandler


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    
    ### Création de l'application Flask
    app = Flask(__name__)

    app.config['SECRET_KEY'] ='0123456'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/afougere/Git/e1/app/app/base_de_donnees/db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    ### Connexion au dashboard Flask-Monitoring
    dashboard.config.init_from(file='/Users/afougere/Git/e1/app/app/configs.cfg')
    dashboard.bind(app)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    mail_handler = SMTPHandler(
        mailhost=('smtp.gmail.com', 587),
        fromaddr= 'fougereaudrey.servererrors@gmail.com' ,
        toaddrs=['fougereaudrey90@gmail.com'],
        subject='Application Error',
        credentials=('fougereaudrey.servererrors@gmail.com', 'P@ssword2809'),
        secure= ())

# setLevel spécifie le plus haut niveau de sévérité qu'un logger va traiter. debug est le niveau le plus bas et critical le niveau le plus haut mail_handler(logging.CRITICAL)
# Si le niveau de sévérité est INFO, le logger ne traite que les messages de niveau INFO, WARNING, ERROR et CRITICAL;
# il ignore les messages de niveau DEBUG
    mail_handler.setLevel(logging.CRITICAL)

# setFormatter sélectionne l'objet Formatter utilisé par cet handler
    mail_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))

# addHandler ajoute un objet handler, en l'occurence cet objet est mail_handler, défini plus haut à la ligne 45
    app.logger.addHandler(mail_handler)

    return app



