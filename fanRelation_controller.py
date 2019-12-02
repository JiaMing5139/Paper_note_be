from flask import Blueprint
from flask import Blueprint
from flask import request
from flask import  session
from flask import jsonify
from database import fansRelation
from database import user
import  json
from sqlalchemy.orm import sessionmaker
from dbext import db

fans_bru = Blueprint('fans',__name__)

@fans_bru.route('/subscribe',methods=['GET','POST'])
def subscribe():
    if request.method == "GET":
        return "okok"
    if request.method == "POST":
        DBsession = sessionmaker(bind=db.engine)
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        subscribedAccount = json_data.get('subscribedAccount')
        subscriberAccount = json_data.get('subscriberAccount')


        dbsession = DBsession()
        print(subscriberAccount,subscribedAccount)
        new_Relation = fansRelation(subscriberAccount,subscribedAccount)
        try:
            db.session.add(new_Relation)
        except Exception as e:
            return jsonify({"subscribe":'failed'})
        db.session.commit()
        dbsession.close()
        return jsonify({'subscribe':"success"})


@fans_bru.route('/get_subscribed',methods=['GET','POST'])
def get_subScribed():
    if request.method == "POST":
        DBsession = sessionmaker(bind=db.engine)
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        subscriberAccount = json_data.get('subscriberAccount')
        dbsession = DBsession()
        print("subscriberAccount",subscriberAccount)
        try:
         user_info = dbsession.query()
         full_subscribed = dbsession.query(fansRelation,user).join(user,user._account == fansRelation._subscriberAccount).filter(fansRelation._subscribedAccount == subscriberAccount).all()
         #acquire own information
         subscriber = dbsession.query(user).filter(user._account == subscriberAccount)
         full_following =  dbsession.query(fansRelation,user).join(user,user._account == fansRelation._subscribedAccount).filter(fansRelation._subscriberAccount == subscriberAccount).all()
         #full = dbsession.query(fansRelation).filter(fansRelation._subscriberAccount == subscriberAccount).all()
         dbsession.commit()
         #dbsession.close()
        except Exception as e:
            #dbsession.close()
            print(str(e))
            return {"login":"failed",'uid':1,'exception':str(e)}
        Msg_subscribed = []
        for item in full_subscribed:
            Relation = item[0]
            User = item[1]
            Msg_subscribed.append({'subscriberAccount':User._account,'subscriberphoto':User._photoName})
        Msg_following = []
        for item in full_following:
            Relation = item[0]
            User = item[1]
            Msg_following.append({'subscribedAccount': User._account, 'subscribedphoto': User._photoName})

        ret_dict = {'state': 'success','subscriberphoto':subscriber[0]._photoName, "subscribed_json": Msg_subscribed,"following_json": Msg_following}
        Relation_json = json.dumps(ret_dict)
        print(Relation_json)
        dbsession.close()
        return Relation_json



