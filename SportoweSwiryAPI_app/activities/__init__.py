from flask import Blueprint

activities_bp = Blueprint('activities', __name__)

from SportoweSwiryAPI_app.activities import activities