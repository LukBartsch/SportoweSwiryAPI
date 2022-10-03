from flask import Blueprint

errors_bp = Blueprint('errors', __name__)

from SportoweSwiryAPI_app.errors import errors