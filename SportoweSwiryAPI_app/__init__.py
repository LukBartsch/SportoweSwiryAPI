from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from SportoweSwiryAPI_app.users import users_bp
    from SportoweSwiryAPI_app.activities import activities_bp
    from SportoweSwiryAPI_app.errors import errors_bp
    app.register_blueprint(errors_bp)
    app.register_blueprint(users_bp, url_prefix='/api/v1')
    app.register_blueprint(activities_bp, url_prefix='/api/v1')

    return app

# results = db.session.execute('show tables')
# for row in results:
#     print(row)
