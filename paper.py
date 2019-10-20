from flask import Blueprint
from flask import request
from pydocx import PyDocX
from paperUtil import parseDocx
from app import db
from database import paper
from app import DBsession
from flask import jsonify
import  json


paper_bru = Blueprint('PAPER',__name__)


@paper_bru.route('/paper_upload',methods=['GET','POST'])
def paper_upload():
    if request.method == "GET":
        return "i get a paper_uplodad Get http"
    if request.method == "POST":
        file = request.files['file']
        print("POST get" + file.filename)
        file.save('/Users/jiamingpan/PycharmProjects/Paper_note/paperPDF/' + file.filename)
        print("POST save"+file.filename)
        title,author,abstract = parseDocx(file.filename)
        print(title,author + '\n' + abstract)
        new_paper = paper(title= title,author = author,abstract = abstract)
        dbsession = DBsession()
        try:
            dbsession.add(new_paper)
            dbsession.commit()
            dbsession.close()
        except Exception as e:
            print('log' + e)
            return jsonify({"upoad":"failed"})
        return jsonify({"upoad":"success"})

@paper_bru.route('/get_top_paper',methods=['GET','POST'])
def get_top_paper():
    session = DBsession()
    return ''

@paper_bru.route('/getPaperByTitle',methods=['GET','POST'])
def getPaperByTitle():
    if request.method == 'POST':
        print('start getPaperByTitle')
        data = request.get_data()
        print(data)
        json_data = json.loads(data.decode('utf-8'))
        title = json_data.get('title')
        print(title)
        dbsession = DBsession()
        print('start dbop')
        try:
            papers = dbsession.query(paper).filter(paper._title.like(title)).all()
        except Exception as e:
            print('exception')
            return jsonify({"paperQuery": 'failed'})
        print(papers)
        return 'pp'


