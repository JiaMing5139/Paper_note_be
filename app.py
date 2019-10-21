print('run app.py')
from flask import Flask
from flask import request
from flask_cors import CORS
app = Flask(__name__)

print('init database')
# init database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
print("start to creat database")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@35.199.106.213:3306/papernote'
db = SQLAlchemy(app=app)
DBsession = sessionmaker(bind=db.engine)
print('import databse before')
import database
print('import databse after')

print('init blueprint')
# init blueprint
from user_info import user_info_bru
from paper import paper_bru
from sentences import  sentences_bru
app.config["SECRET_KEY"] = "renyizifuchuan"

CORS(app, supports_credentials=True)
app.register_blueprint(user_info_bru)
app.register_blueprint(paper_bru)
app.register_blueprint(sentences_bru)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "GET":
        return "i get a Get http"


if __name__ == '__main__':

    app.run()

