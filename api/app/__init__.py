# higia-agencias/app/__init__.py

from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask import Flask, request, g, session, redirect
import os
from os.path import abspath, dirname, join
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required
import logging
from flask_caching import Cache
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome

db = SQLAlchemy()
migrate = Migrate()


login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]

    logger = logging.getLogger(__name__)

    mail = Mail(app)

    LOG_FILENAME = 'logs.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

    fontAwesome = FontAwesome(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    bootstrap = Bootstrap(app)

    # Define the application directory
    BASE_DIR = dirname(dirname(abspath(__file__)))
    # Media dir
    MEDIA_DIR = join(BASE_DIR, 'media')
    app.config['MEDIA_DIR'] = join(BASE_DIR, 'media')
    app.config['POSTS_IMAGES_DIR'] = join(MEDIA_DIR, 'posts')

    # Cache
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    from .public import public_bp
    app.register_blueprint(public_bp)

    from .clases import class_bp
    app.register_blueprint(class_bp)

    from .observability import observability_bp
    app.register_blueprint(observability_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    # Conexión a la base de datos relacional
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://%s:%s@%s:%s/%s" % (os.environ["BBDD_USER"],
                                                                                 os.environ["BBDD_PASSWORD"],
                                                                                 os.environ["BBDD_HOST"],
                                                                                 os.environ["BBDD_PORT"],
                                                                                 os.environ["BBDD_DATABASE"])

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]

#        db = SQLAlchemy(app)
        db.init_app(app)
        migrate.init_app(app, db)

    except Exception as e:
        print("Error al acceder a POSTGRES %s" % e)
        logger.error("Error al acceder a POSTGRES: %s" % e)

# TODO: Migraciones

    @app.after_request
    def after_request(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "POST, \
                                                            GET, \
                                                            OPTIONS, \
                                                            PUT, \
                                                            DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
        return response

    return app


def register_error_handlers(app):

    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404

    @app.errorhandler(401)
    def error_404_handler(e):
        return render_template('401.html'), 401
