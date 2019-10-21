print('user_info worked')
from flask import Blueprint
from flask import request
from flask import  session
from flask import jsonify
import  json

from app import db
from app import DBsession
from database import user
user_info_bru = Blueprint('user',__name__)

@user_info_bru.route('/user_for',methods=['GET','POST'])
def user_get():
    if request.method == "GET":
        return "i get a Get http"
    if request.method == "POST":
        return "i get a Post http"


@user_info_bru.route('/user_login',methods=['GET','POST'])
def user_login():
    if request.method == "POST":
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        account = json_data.get('account')
        password = json_data.get('password')
        dbsession = DBsession()
        try:
         user_data = dbsession.query(user).filter(user._account == account).all()
        except Exception as e:
            return {"login":"failed",'uid':0}
        print('user_login:query_result'+str(user_data))
        if user_data == []:
            return jsonify({"login":"failed",'uid':0})
        elif user_data[0]._passwd != password:
             return jsonify({"login":"failed",'uid':0})
        session['uid'] = 1003
        return jsonify({"login":"success",'uid':user_data[0]._id,'account':user_data[0]._account})


@user_info_bru.route('/user_register',methods=['POST'])
def user_register():
    if request.method == "POST":
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        account = json_data.get('account')
        password = json_data.get('password')
        email = json_data.get('email')

        dbsession = DBsession()
        new_user = user(_account = account,_passwd = password,_email = email)
        try:

            db.session.add(new_user)
        except Exception as e:
            return jsonify({"register":'failed'})
        return "i get a Post http"

@user_info_bru.route('/user_edit',methods=['GET','POST'])
def user_edit():
    if request.method == "GET":
        uid = session.get("uid")
        print(uid)
        return "i want to edit user:" + str(uid)

    if request.method == "POST":
        uid = session.get("uid")
        return "i want to edit user:" + uid