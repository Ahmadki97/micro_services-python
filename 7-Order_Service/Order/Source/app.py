from flask import Flask
from config import DevelopmentConfig
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

login_manager = LoginManager()
login_manager.init_app(app)