from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "immm-totaly--secrettt--"
from app import routes
