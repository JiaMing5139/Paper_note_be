from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
db = SQLAlchemy()
paper_bru = Blueprint('PAPER',__name__)