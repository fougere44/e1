from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, login_manager
from . import db
from .models import User

auth = Blueprint('auth',__name__,template_folder='templates',static_folder='static',static_url_path="/Users/afougere/Git/project/app/app/static/css")

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Vérifie ton email ou ton mot de passe et essaye de te connecter une nouvelle fois', "warning")
        return redirect(url_for('auth.login'))


    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup',  methods=['POST'])
def signup_post():
    if request.method == 'POST':

        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('ton adresse email existe déjà !', "warning")
            return redirect(url_for('auth.signup'))
            

        if not len(password) >= 8:
            flash("Ton mot de passe doit au moins faire 8 caractères.", "warning")
            return redirect(url_for('auth.signup'))


        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        flash("Account created", "success")
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))




    