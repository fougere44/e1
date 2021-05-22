from flask import Blueprint, render_template, request, redirect, jsonify, flash, current_app, url_for
from flask_login import login_required, current_user, LoginManager

import os
from werkzeug.utils import secure_filename
import traceback
from werkzeug.exceptions import InternalServerError

import base64
import io
from PIL import Image
import keras
from keras import backend as K
from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy as np
import logging

#create logger
logger = logging.getLogger('main.py')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.FileHandler('app/logs/myapp.log')
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address


#limiter = Limiter(app, key_func=get_remote_address)

#path_env = "C:\Users\afougere\Anaconda3\envs\IA-Racing"
#path_repo = "C:\Users\afougere\Git\e1\app"

main = Blueprint('main',__name__,template_folder='templates',static_folder='static',static_url_path="/Users/afougere/Git/e1/app/app/static/css")



@main.route('/')
def index():
    return render_template("index.html")


@main.route('/course')
def race():
    return render_template("course.html")
    

@main.route('/profile')
@login_required
def profile():
    name = current_user.name

    return render_template("profile.html", name=current_user.name)


def allowed_image(filename):
    allowed_image = ["PNG", "JPG", "JPEG", "GIF"]
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in allowed_image:
        return True

    else:
        return False


def allowed_image_filesize(filesize):
    max_image_size = 120 * 160 * 3
    if int(filesize) <= max_image_size:
        return True
    else:
        return False


@main.route("/upload-image", methods=['GET', 'POST'])
#@limiter.limit("5 per minute")
def upload_image():
    path_image = "C:/Users/afougere/Git/e1/app/app/static/img/uploads"

    if request.method == "POST":
        if request.files:
            if not allowed_image_filesize(request.cookies.get("filesize")):
                flash("File exceed maximum size", "danger")
                logger.warning("La taille de l'image excède la taille maximale autorisée")
                return redirect(url_for("main.profile"))


            image = request.files["image"]

            if image.filename == ".jpg":
                flash("L'image doit avoir un nom !", "danger")
                logger.warning("L'image doit avoir un nom")
                return redirect(url_for("main.profile"))

            if not allowed_image(image.filename):
                flash("Cette extension n'est pas autorisée, seules celles-ci sont autoriséés : PNG, JPG, JPEG", "danger")
                logger.warning("Cette extension n'est pas autorisée")
                return redirect(url_for("main.profile"))

            else:
                filename = secure_filename(image.filename)

                image.save(os.path.join(path_image, filename))
                prediction = getPrediction(filename)

                output1 = prediction[0]
                output2 = abs(prediction[1])

                logger.info("La prédiction de l'image a été réussie")   
                logger.info("L'image prédite a été sauvegardé dans le dossier static")
                print("image saved")

                prediction_text = "Prédiction vitesse : {} Prédiction angle : {} Label de l'image originale : {}".format(output2, output1, filename)
                
                prediction_1 = prediction_text[0:25]
                prediction_2 = prediction_text[40:64]
                prediction_3 = prediction_text[78:132]

                return render_template("profile.html", prediction_text= prediction_1 +  prediction_2 + prediction_3)
               
            
            return redirect(request.url)

    return render_template("profile.html") 


def getPrediction(filename):

    logger.info("Le modèle a bien été uploadé")   
    model = load_model('C:/Users/afougere/Git/e1/data_analysis/models/output_model/test_custom_warehouse_waveshare.h5')
    path_image = "C:/Users/afougere/Git/e1/data_analysis/data/images_data/images/test/test_images_flask/"
    image = load_img(path_image + filename)
    image = img_to_array(image)
    image = image.reshape((1,) + image.shape)
    image /= 255.0
    prediction = model.predict(image)
    
    response = [
            prediction[0][0][0],
            prediction[1][0][0]
    ]

    return response



## Errors

@main.errorhandler(403)
def access_forbidden(e):
    return render_template('403.html'), 403

@main.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500