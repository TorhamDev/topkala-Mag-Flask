import os
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
file_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = file_dir + "/database"
goal_route = os.path.join(file_dir,"app.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + goal_route

db = SQLAlchemy(app)

from TorhamBLOG import viwes
from TorhamBLOG import models