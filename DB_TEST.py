from app import db
from database import user
from app import DBsession


new_user = user('admin001',123456,'821269398@qq.com')

dbsession = DBsession()

dbsession.add(new_user)

dbsession.commit()
    