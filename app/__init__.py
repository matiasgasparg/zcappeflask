from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, storage,initialize_app
from .routes.user_bp import user_bp
from .routes.img_bp import img_bp

from config import Config
from flask_cors import CORS
from .database import DatabaseConnection


# Configura el SDK de Firebase Admin


def init_app():
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    
    cred = credentials.Certificate("serviceAccountKey.json")
    initialize_app(cred, {'storageBucket': 'zcappetienda.appspot.com'})
    CORS(app, supports_credentials=True)
    app.config.from_object(
        Config
    )

    DatabaseConnection.set_config(app.config)

    app.register_blueprint(user_bp, url_prefix = '/users')
    app.register_blueprint(img_bp, url_prefix = '/upload')


    return app
