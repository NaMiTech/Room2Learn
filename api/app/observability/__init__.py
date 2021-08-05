from flask import Blueprint

observability_bp = Blueprint('observability', __name__, template_folder='templates')
from . import routes