from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_caching import Cache

app = Flask(__name__)
app.config.from_object(Config)

cache = Cache(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, constants
