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
import paralleldots
paralleldots.set_api_key('5IAudGuShdT5PDelXQ9MVwurzPg1f5gsYBl5bLzULTE')

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
        parentid = json_data.get('parentid')
        #print('sid:'+str(sid['0']))
        print('uid:'+str(uid))
        print('note:'+str(note))
        print('pid:' + str(pid))
        print('parentid:' + str(parentid))

        result = paralleldots.abuse(note)
        if (result['abusive'] > 0.9 or result['hate_speech'] > 0.9):
            return{"state":"badcomment"}

        new_note = notes(sid = sid['0'], notes = note, uid = uid, pid = pid,parentid = parentid)
        dbsession = DBsession()
        try:
             inserded = dbsession.add(new_note)
             dbsession.flush()
             dbsession.refresh(new_note)
             new_id = new_note._id

             # new_notes = dbsession.query(notes).filter(notes._id == parentid).all()
             # new_notes[0]._numOfnotes += 1

             dbsession.commit()

             dbsession.close()
        except Exception as e:
             print('log' + str(e))
             dbsession.rollback()
             return ({"state": "failed"})
        return jsonify({"state":"success","new_id": new_id})

@note_bru.route('/subnote_add', methods=['GET', 'POST'])
def subnote_add():
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
        parentid = json_data.get('parentid')
        # print('sid:'+str(sid['0']))
        print('uid:' + str(uid))
        print('note:' + str(note))
        print('pid:' + str(pid))
        print('parentid:' + str(parentid))

        result = paralleldots.abuse(note)
        if (result['abusive'] > 0.9 or result['hate_speech'] > 0.9):
            return {"state": "badcomment"}

        new_note = notes(sid=sid['0'], notes=note, uid=uid, pid=pid, parentid=parentid)
        dbsession = DBsession()
        try:
            inserded = dbsession.add(new_note)
            dbsession.flush()
            dbsession.refresh(new_note)
            new_id = new_note._id

            new_notes = dbsession.query(notes).filter(notes._id == parentid).all()
            new_notes[0]._numOfnotes += 1

            dbsession.commit()

            dbsession.close()
        except Exception as e:
            print('log' + str(e))
            dbsession.rollback()
            return ({"state": "failed"})
        return jsonify({"state": "success", "new_id": new_id})


@note_bru.route('/subnote_get', methods=['GET', 'POST'])
def subnote_get():
        if request.method == "GET":
            return "i get a paper_uplodad Get http"
        if request.method == "POST":
            print("post")
            DBsession = sessionmaker(bind=db.engine)
            data = request.get_data()
            json_data = json.loads(data.decode('utf-8'))
            sid = json_data.get('sid')
            uid = json_data.get('uid')
            note = json_data.get('note')
            pid = json_data.get('pid')
            parentid = json_data.get('parentid')
            noteType = json_data.get('type')

            dbsession = DBsession()
            try:
               print(parentid)
               new_notes = dbsession.query(notes, user._account).join(user, user._id == notes._uid).filter(
                        notes._parentid == parentid).all()
               dbsession.commit()
                # dbsession.close()
            except Exception as e:
                print('log:' + str(e))
                # dbsession.rollback()
                return jsonify({"state": "failed"})
            note_dic = []
            for note in new_notes:
                notep = note[0]
                id = notep._id
                uid = notep._uid
                content = notep.notesContent
                _numOfnotes = notep._numOfnotes
                account = note[1]

                thumup = 0
                note_dic.append({'id': id, 'uid': uid, 'note': content, 'account': account, 'thumup': thumup,
                                 'numOfReply': _numOfnotes})
            ret_dict = {'state': 'success', "notes_json": note_dic}
            notes_json = json.dumps(ret_dict)
            print(notes_json)

            return notes_json

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
        parentid = json_data.get('parentid')
        noteType = json_data.get('type')

        dbsession = DBsession()
        numOfReplylist= []
        try:
            new_notes = dbsession.query(notes,user._account).join(user,user._id == notes._uid).filter(notes._pid == pid,notes._sid == sid['0']).all()
            dbsession.commit()
            #dbsession.close()
        except Exception as e:
             print('log:' + str(e))
             #dbsession.rollback()
             return jsonify({"state":"failed"})
        note_dic = []
        for note in new_notes:
            notep = note[0]
            if notep._parentid != None:
                continue
            id = notep._id
            uid = notep._uid
            content = notep.notesContent
            _numOfnotes = notep._numOfnotes
            account = note[1]
            thumup = 0
            note_dic.append({'id':id,'uid':uid,'note':content,'account':account,'thumup':thumup,'numOfReply':_numOfnotes})
        ret_dict = {'state': 'success', "notes_json": note_dic}
        notes_json = json.dumps(ret_dict)
        print(notes_json)

        return notes_json
