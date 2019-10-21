from flask import Blueprint
from flask import request
from pydocx import PyDocX
from paperUtil import parseDocx
from app import db
from database import paper
from database import  sentence
from app import DBsession
from flask import jsonify
import uuid
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
            return jsonify({"upoad":"failed"})
        return jsonify({"upoad":"success"})

#going to insert sentence to database
#going to make html and store it in paperTable
def process_sentences(paper_id, sentences):
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
        return ''

@paper_bru.route('/getPaperByCatlog',methods=['GET','POST'])
def getPaperByCatlog():
    return ''

@paper_bru.route('/getPaperByTopTen',methods=['GET','POST'])
def getPaperByTopTen():
    data = request.get_data()
    json_data = json.loads(data.decode('utf-8'))
    numOftop = json_data.get('numOftop')
    #request for database
    dbsession = DBsession()
    try:
       papers = dbsession.query(paper).filter(paper.all()) # error!!!!
        #print(papers)
    except Exception as e:
        return {'query':'failed'}
    #papers_json =  papers(database) => papers_json
    return {'query':'success'}

@paper_bru.route('/getPaperByPid',methods=['GET','POST'])
def getPaperByPid():
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
