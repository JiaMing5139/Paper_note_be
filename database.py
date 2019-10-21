print('run database.py')
from app import db

print("start to create model")
class user(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    #__table_args__ = {"useexisting": True}
    _id= db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # id 整型，主键，自增，唯一
    _account = db.Column(db.String(20),unique=True)
    _passwd = db.Column(db.String(20))
    _email = db.Column(db.String(200))
    __tablename__ = 'user'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名

    def __init__(self,  acount,passwd,email):  # 初始化方法，可以对对象进行创建
        self._account = acount
        self._passwd = passwd
        self._email = email
    def __repr__(self):  # 输出方法，与__str__类似，但是能够重现它所代表的对象
        return '<user %r, %r, %r>' % (self._id, self._account, self._passwd)


class paper(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    #__table_args__ = {"useexisting": True}
    _id= db.Column(db.String(256), primary_key=True, unique=True)  # id 整型，主键，自增，唯一
    _title = db.Column(db.String(100))
    _abstract = db.Column(db.String(20000))
    _content = db.Column(db.TEXT(65534))
    _author = db.Column(db.TEXT(2000),default="null")
    _catlog = db.Column(db.String(20))
    _numOfnotes = db.Column(db.Integer,default = 0)

    __tablename__ = 'paper'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名
    def __init__(self,id, title, abstract,content = '',author = '' ,catlog = ''):  # 初始化方法，可以对对象进行创建
        self._id = id
        self._title = title
        self._abstract =abstract
        self._content = content
        self._author = author
        self._catlog = catlog

    def __repr__(self):  # 输出方法，与__str__类似，但是能够重现它所代表的对象
        return '<paper %r, %r, %r,%r>' % (self._title, self._abstract, self._author,self._content)


class test(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    # __table_args__ = {"useexisting": True}
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # id 整型，主键，自增，唯一
    _testdata = db.Column(db.String(20))
    __tablename__ = 'test'

    def __init__(self,testdata):  # 初始化方法，可以对对象进行创建
        self._testdata = testdata

    def __repr__(self):  # 输出方法，与__str__类似，但是能够重现它所代表的对象
        return '<test %r, %r, %r>' % (self.s_id, self.s_name, self.sage)


class sentence(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    #__table_args__ = {"useexisting": True}
    _id= db.Column(db.Integer, primary_key=True, unique=True)  # id 整型，主键，自增，唯一
    _pid = db.Column(db.String(256))  #forgin key
    _pos = db.Column(db.Integer)
    _type = _sentence = db.Column(db.String(10))
    _sentence = db.Column(db.String(20000))
    _numOfnotes = db.Column(db.Integer,default = 0)

    __tablename__ = 'sentence'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名
    def __init__(self,pid ,pos, sentence,type):  # 初始化方法，可以对对象进行创建
        self._pid = pid
        self._pos = pos
        self._sentence = sentence
        self._type = type

    def __repr__(self):  # 输出方法，与__str__类似，但是能够重现它所代表的对象
        return '<paper %r, %r, %r,%r,%r>' % (self._id, self._pid, self._pos,self._sentence,self._numOfnotes)
