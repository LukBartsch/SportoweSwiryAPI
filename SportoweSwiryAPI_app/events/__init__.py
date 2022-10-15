from flask import Blueprint

events_bp = Blueprint('events', __name__)

from SportoweSwiryAPI_app.events import events