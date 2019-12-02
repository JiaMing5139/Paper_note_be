from flask import Blueprint
from flask import request
from database import sentence
from app import DBsession

sentences_bru = Blueprint('SENTENCES',__name__)
