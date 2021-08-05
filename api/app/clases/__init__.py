from flask import Blueprint

class_bp = Blueprint('clases', __name__, template_folder='templates')

from . import routes
