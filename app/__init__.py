from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jxkiopeppzhkfa:4fba5c6833078917e812eeaa982c6d7f869ed2c0f570935f0d31b3fe83dccca3@ec2-54-86-224-85.compute-1.amazonaws.com:5432/d9qdee50ds4ser'

    db.init_app(app)
    migrate.init_app(app,db)

    from app.models.planet import Planet

    from .routes import planets_bp
    app.register_blueprint(planets_bp)

    return app
