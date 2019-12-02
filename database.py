print('run database.py')
from dbext import db
from sqlalchemy_fulltext import FullText, FullTextSearch
import sqlalchemy_fulltext.modes as FullTextMode

print("start to create model")
class user(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表al
    #__table_args__ = {"useexisting": True}
    _id= db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # id 整型，主键，自增，唯一
    _account = db.Column(db.String(20),unique=True)
    _passwd = db.Column(db.String(20))
    _email = db.Column(db.String(200))
    _photoName = db.Column(db.String(200))
    __tablename__ = 'user'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名

    def __init__(self,  acount,passwd,email,photoName):  # 初始化方法，可以对对象进行创建
        self._account = acount
        self._passwd = passwd
        self._email = email
        self._photoName = photoName
    def __repr__(self):  # 输出方法，与__str__类似，但是能够重现它所代表的对象
        return '<user %r, %r, %r>' % (self._id, self._account, self._passwd)

class fansRelation(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表al
    #__table_args__ = {"useexisting": True}
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    #_subscriberId= db.Column(db.Integer)  # id 整型，主键，自增，唯一
    _subscriberAccount = db.Column(db.String(20))
    #_subscribedId = db.Column(db.Integer)
    _subscribedAccount = db.Column(db.String(20))
    __tablename__ = 'fansRelation'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名

    def __init__(self,_subscriberAccount,_subscribedAccount):  # 初始化方法，可以对对象进行创建
       # self._subscriberId = _subscriberId
        self._subscriberAccount = _subscriberAccount
       # self._subscribedid = _subscribedid
        self._subscribedAccount = _subscribedAccount
    def __repr__(self):  # 输出方法，与__str__类似，但是能够重现它所代表的对象
        return '<user %r, %r>' % (self._subscriberAccount, self._subscribedAccount)


class paper(FullText,db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    #__table_args__ = {"useexisting": True}
    _id= db.Column(db.String(256), primary_key=True, unique=True)  # id 整型，主键，自增，唯一
    _title = db.Column(db.String(100))
    _abstract = db.Column(db.String(20000))
    _content = db.Column(db.TEXT(65534))
    _author = db.Column(db.TEXT(2000),default="null")
    _catlog = db.Column(db.String(20))
    _numOfnotes = db.Column(db.Integer,default = 0)

    __fulltext_columns__ = ('_abstract', ' _content')
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

class notes(FullText,db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    #__table_args__ = {"useexisting": True}
    _id= db.Column(db.Integer, primary_key=True, autoincrement=True,unique=True)  # id 整型，主键，自增，唯一
    _parentid = db.Column(db.Integer)
    _pid = db.Column(db.String(256))
    _sid = db.Column(db.String(256))  #forgin key
    _uid = db.Column(db.Integer) #forgin key
    notesContent = db.Column(db.String(20000))
    _numOfnotes = db.Column(db.Integer,default = 0)
    __fulltext_columns__ = ('notesContent',)
    __tablename__ = 'notes'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名
    def __init__(self,sid ,notes,uid,pid,parentid = 0):  # 初始化方法，可以对对象进行创建
        self._sid = sid
        self.notesContent = notes
        self._uid = uid
        self._parentid = parentid
        self._pid = pid

    def __repr__(self):  # 输出方法，与__str__类似，但是能够重现它所代表的对象
        return '<note %r, %r, %r,%r>' % (self._sid, self.notesContent, self._uid, self._numOfnotes)

class user_paper(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    #__table_args__ = {"useexisting": True}
    _id= db.Column(db.Integer, primary_key=True, unique=True)  # id 整型，主键，自增，唯一
    _pid = db.Column(db.String(256))  #forgin key
    _uid =  db.Column(db.Integer)

    __tablename__ = 'user_paper'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名
    def __init__(self,pid ,uid):  # 初始化方法，可以对对象进行创建
        self._pid = pid
        self._uid = uid

class queue(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    #__table_args__ = {"useexisting": True}
    _id= db.Column(db.Integer, primary_key=True, unique=True)  # id 整型，主键，自增，唯一
    _pid = db.Column(db.String(256))  #forgin key
    _uid =  db.Column(db.Integer)

    __tablename__ = 'queue'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名
    def __init__(self,pid ,uid):  # 初始化方法，可以对对象进行创建
        self._pid = pid
        self._uid = uid

FULLTEXT_TABLE = "test_full_text"
from sqlalchemy.ext.declarative import declarative_base
BASE = declarative_base()

class RecipeReviewModel(FullText, db.Model):
    __tablename__ = FULLTEXT_TABLE
    # mroonga engine supporting CJK chars
    # __table_args__ = {'mysql_engine': 'MyISAM',
    #                   'mysql_charset': 'utf8'}

    __fulltext_columns__ = ('commentor', 'review')

    id = db.Column(db.Integer, primary_key=True)
    commentor = db.Column(db.String(length=100))
    review = db.Column(db.Text())

    def __init__(self, commentor, review):
        self.review = review
        self.commentor = commentor
