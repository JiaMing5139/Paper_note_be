from sqlalchemy.orm import sessionmaker
from dbext import db
from database import Message
from database import user

class MessageQueue:
    def __init__(self,account):
        self.MessageList = []
        self.account = account
        self.Dbsession =  sessionmaker(bind=db.engine)
        self.id = 0
    def fuilMessageQueue(self):
        dbsession = self.Dbsession()
        try:
            messages = dbsession.query(Message).filter(Message._dst == self.account).all()
        except Exception as e:
            print(e)
            return -1
        for mes in messages:
            self.MessageList.append(mes)
        print(self.MessageList)
        dbsession.close()
    def __len__(self):
        return len(self.MessageList)
    def getMessage(self):
        dbsession = self.Dbsession()
        ret_list = []
        for mes in self.MessageList:
             ret_list.append({'dst':mes._dst,'src':mes._src,'type':mes._type})
        return ret_list
    def dequeueAll(self):
        dbsession = self.Dbsession()
        for message in self.MessageList:
            dbsession.delete(message)
        dbsession.commit()
        dbsession.close()
    def  enqueue(self,type,src,dst):
        dbsession = self.Dbsession()
        new_message = Message(type, src, dst)
        dbsession.add(new_message)
        dbsession.commit()
        dbsession.close()
        pass
