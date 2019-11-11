from flask import Blueprint
from flask import request
from pydocx import PyDocX
from paperUtil import parseDocx
from dbext import db
from database import paper
from database import  sentence
from flask import jsonify
import uuid
import  json
from sqlalchemy.orm import sessionmaker


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
        title,author,abstract,sentences_list = parseDocx(file.filename)
        #print(title,author + '\n' + abstract)

        pid = uuid.uuid3(uuid.NAMESPACE_DNS,title)
        html_content = process_sentences(str(pid), sentences_list)
        print('paperid:',pid)
        new_paper = paper(id = str(pid),title= title,author = author,abstract = abstract,content = html_content)
        dbsession = DBsession()
        try:
            dbsession.add(new_paper)
            dbsession.commit()
            dbsession.close()
        except Exception as e:
            print('log' + str(e))
            dbsession.rollback()
            return jsonify({"upload":"failed"})
        return jsonify({"upload":"success"})

#going to insert sentence to database
#going to make html and store it in paperTable
def process_sentences(paper_id, sentences):
    DBsession = sessionmaker(bind=db.engine)
    dbsession = DBsession()
    html_content = ''
    try:
        for pos,stc in enumerate(sentences):
            #print('pos:' + str(pos) + stc)
            if pos == 0:
                type = 'header'
                html_content+= '<h3>'+stc+'</h>'
            else:
                html_content += '<p v-on:clic   k=paper_click($event) class='+str(pos)+'>' + stc + '</p>'
                #html_content += '<p  class=' + str(pos) + '>' + stc + '</p>'
                type = 'text'
            new_sentences = sentence(pid=paper_id, pos=pos, sentence=stc, type=type)
            dbsession.add(new_sentences)
    except Exception as e:
        print('log:'+str(e))
        dbsession.rollback()
    dbsession.commit()
    return html_content


#title, author, abstract, sentences_list = parseDocx('bitcoin.docx')
#process_sentences(1,sentences_list)


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
    dbsession = DBsession()
    try:
       papers = dbsession.query(paper).filter().all() # error!!!!
       #print(len(papers))
       #print(papers[0])
       #print(type(papers))
       papers_json=get_papersjson(papers)
    except Exception as e:
        return {'query':'failed','exception':str(e)}
    #print(papers_json)
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

@paper_bru.route('/getPaperByPid',methods=['GET','POST'])
def getPaperByPid():
    DBsession = sessionmaker(bind=db.engine)
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        pid = json_data.get('pid')
        # request for database
        dbsession = DBsession()
    paper_result = ''
    try:
        #user_data = dbsession.query(user).filter(user._account == account).all()
        paper_result = dbsession.query(paper).filter(paper._id == pid).one() # error!!!!
    except Exception as e:
        print("log"+str(e))
    print(paper_result)
    ret_dic = {'id':paper_result._id,'title':paper_result._title,'author':paper_result._author,'content':paper_result._content}
    return json.dumps(ret_dic)

@paper_bru.route('/papertest',methods=['GET','POST'])
def papertest():
    html = PyDocX.to_html('./paperPDF/' + 'bitcoin.docx')
    print(html)
    return html
