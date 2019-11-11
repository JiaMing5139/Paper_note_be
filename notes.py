from flask import Blueprint
from flask import request
from dbext import db
from database import paper
from database import  sentence
from database import user
from database import  notes
from flask import jsonify
import uuid
import  json
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import func

note_bru = Blueprint('NOTES', __name__)

@note_bru.route('/note_add', methods=['GET', 'POST'])
def note_add():
    if request.method == "GET":
        return "i get a paper_uplodad Get http"
    if request.method == "POST":
        DBsession = sessionmaker(bind=db.engine)
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        sid = json_data.get('sid')
        uid = json_data.get('uid')
        note = json_data.get('note')
        pid = json_data.get('pid')
        print('sid:'+str(sid['0']))
        print('uid:'+str(uid))
        print('note:'+str(note))
        print('pid:' + str(pid))

        new_note = notes(sid = sid['0'], notes = note, uid = uid, pid = pid)

        dbsession: Session = DBsession()
        try:
             dbsession.add(new_note)
             dbsession.commit()
             dbsession.close()
        except Exception as e:
             print('log' + str(e))
             dbsession.rollback()
             return jsonify({"state":"failed"})
        return jsonify({"state":"success"})

@note_bru.route('/note_get', methods=['GET', 'POST'])
def note_get():
    if request.method == "GET":
        return "i get a paper_uplodad Get http"
    if request.method == "POST":
        DBsession = sessionmaker(bind=db.engine)
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        sid = json_data.get('sid')
        uid = json_data.get('uid')
        note = json_data.get('note')
        pid = json_data.get('pid')
        print('sid:'+str(sid['0']))
        print('uid:'+str(uid))
        print('note:'+str(note))
        print('pid:' + str(pid))

        dbsession = DBsession()
        try:
             new_notes = dbsession.query(notes,user._account).join(user,user._id == notes._uid).filter(notes._pid == pid,notes._sid == sid['0']).all()
             #numOfReply = dbsession.query(notes).filter(notes._pid == pid,notes._parentid == new_notes._id).all()
             dbsession.commit()
             #dbsession.close()
        except Exception as e:
             print('log:' + str(e))
             #dbsession.rollback()
             return jsonify({"state":"failed"})
        note_dic = []
        for note in new_notes:
            print(type(note))
            print(type(note[0]))
            print(note[1])
            notep = note[0]

            id = notep._id
            uid = notep._uid
            content = notep._notes
            thumup = notep._numOfnotes
            account = note[1]
            note_dic.append({'id':id,'uid':uid,'note':content,'account':account,'thumup':thumup})
        ret_dict = {'state': 'success', "notes_json": note_dic}
        notes_json = json.dumps(ret_dict)
        print(notes_json)

        #print(new_notes)
        return notes_json