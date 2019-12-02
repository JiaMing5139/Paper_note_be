print('user_info worked')
from flask import Blueprint
from flask import request
from flask import  session
from flask import jsonify
import  json
from sqlalchemy.orm import sessionmaker
from dbext import db


from database import user
user_info_bru = Blueprint('user',__name__)

@user_info_bru.route('/user_for',methods=['GET','POST'])
def user_get():
    if request.method == "GET":
        return "i get a Get http"
    if request.method == "POST":
        print('login')
        DBsession = sessionmaker(bind=db.engine)
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        account = json_data.get('account')
        password = json_data.get('password')
        dbsession = DBsession()
        try:
            user_data = dbsession.query(user).filter(user._account == account).all()
            dbsession.commit()
            #dbsession.close()
        except Exception as e:
            #dbsession.close()
            return {"login": "failed", 'uid': 1, 'exception': str(e)}
        print('user_login:query_result' + str(user_data))
        if user_data == []:
            return jsonify({"login": "failed", 'uid': 2, 'passwd': 'error'})
        elif user_data[0]._passwd != password:
            return jsonify({"login": "failed", 'uid': 3, 'passwd': 'error'})
        session['uid'] = 1003
        return jsonify({"login": "success", 'uid': user_data[0]._id, 'account': user_data[0]._account})

@user_info_bru.route('/user_login',methods=['GET','POST'])
def user_login():
    if request.method == "POST":
        print('login')
        DBsession = sessionmaker(bind=db.engine)
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        account = json_data.get('account')
        password = json_data.get('password')
        dbsession = DBsession()
        try:
         user_data = dbsession.query(user).filter(user._account == account).all()
         dbsession.commit()

        except Exception as e:
            #dbsession.close()
            return {"login":"failed",'uid':1,'exception':str(e)}
        print('user_login:query_result'+str(user_data))
        if user_data == []:
            return jsonify({"login":"failed",'uid':2,'passwd':'error'})
        elif user_data[0]._passwd != password:
             return jsonify({"login":"failed",'uid':3,'passwd':'error'})
        session['uid'] = 1003
        dbsession.close()
        return jsonify({"login":"success",'uid':user_data[0]._id,'account':user_data[0]._account})


@user_info_bru.route('/user_register',methods=['POST'])
def user_register():
    if request.method == "POST":
        DBsession = sessionmaker(bind=db.engine)
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        firstname = json_data.get('firstname')
        lastname = json_data.get('lastname')
        account = json_data.get('accountname')
        password = json_data.get('password')
        photoName = json_data.get('photoName')
        #confirm_password = json_data.get('confirm_password')
        email = json_data.get('email')
        #birthday = json_data.get('birthday')
        dbsession = DBsession()
        new_user = user(account,password,email,photoName)
        try:
            dbsession.add(new_user)
        except Exception as e:
            return jsonify({"register":'failed'})
        dbsession.commit()
        dbsession.close()
        return jsonify({'register':"success"})

@user_info_bru.route('/user_edit',methods=['GET','POST'])
def user_edit():
    if request.method == "GET":
        uid = session.get("uid")
        print(uid)
        return "i want to edit user:" + str(uid)

    if request.method == "POST":
        uid = session.get("uid")
        return "i want to edit user:" + uid

@user_info_bru.route('/photo_upload',methods=['GET','POST'])
def photo_upload():
    if request.method == "GET":
        return "i get a paper_uplodad Get http"
    if request.method == "POST":
        DBsession = sessionmaker(bind=db.engine)
        file = request.files['file']
        print("POST get" + file.filename)
        file.save('/Users/jiamingpan/PycharmProjects/Paper_note/static/' + file.filename)
        print("POST save"+file.filename)
        return jsonify({"upload":"success","filename":file.filename})