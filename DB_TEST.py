from app import db
from database import user
from app import DBsession


new_user = user('admin001',123456,'821269398@qq.com')

try:
    from database import user
    user_data = db.session.query(user).filter(user._account== 'admin002').all()
    db.session.commit()
    print(user_data)



except Exception as e:
    print('log')
    print(e)
    