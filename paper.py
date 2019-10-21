from flask import Blueprint
from flask import request
from pydocx import PyDocX
from paperUtil import parseDocx
from dbext import db
from database import paper
from flask import jsonify
from sqlalchemy.orm import sessionmaker
import  json


paper_bru = Blueprint('PAPER',__name__)


@paper_bru.route('/paper_upload',methods=['GET','POST'])
def paper_upload():
    if request.method == "GET":
        return "i get a paper_uplodad Get http"
    if request.method == "POST":
        DBsession = sessionmaker(bind=db.engine)
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
    DBsession = sessionmaker(bind=db.engine)
    session = DBsession()
    return ''

@paper_bru.route('/getPaperByTitle',methods=['GET','POST'])
def getPaperByTitle():
    if request.method == 'POST':
        DBsession = sessionmaker(bind=db.engine)
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
        return ''

@paper_bru.route('/getPaperByCatlog',methods=['GET','POST'])
def getPaperByCatlog():
    return ''

@paper_bru.route('/getPaperByTopTen',methods=['GET','POST'])
def getPaperByTopTen():
    print('start get PaperTotpen')
    DBsession = sessionmaker(bind=db.engine)
    # data = request.get_data()
    # json_data = json.loads(data.decode('utf-8'))
    # numOftop = json_data.get('numOftop')
    # print (numOftop)
    #request for database
    dbsession = DBsession()
    try:
       papers = dbsession.query(paper).filter().all() # error!!!!
       #print(len(papers))
       print(papers[0])
       print(type(papers))
       papers_json=get_papersjson(papers)
    except Exception as e:
        return {'query':'failed','exception':str(e)}
    print(papers_json)
    #papers_json =  papers(database) => papers_json
    papers_dict={'query':'success',"papers_json":papers_json}
    papers_json=json.dumps(papers_dict)
    return papers_json
def get_papersjson(papers):
    papers_json=[]
    for paper in papers:
        id=paper._id
        title=paper._title
        abstract=paper._abstract
        content=paper._content
        author=paper._author
        catlog=paper._catlog
        numOfnotes=paper._numOfnotes
        paper_json={"id":id,"title":title,"abstract":abstract,"content":content,"author":author,"catlog":catlog,
                    "numOfnotes":numOfnotes}
        papers_json.append(paper_json)
    return papers_json


@paper_bru.route('/papertest',methods=['GET','POST'])
def papertest():
    html = PyDocX.to_html('./paperPDF/' + 'bitcoin.docx')
    print(html)
    return html
