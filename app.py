from flask import Flask
from flask import request
from flask_cors import CORS
from dbext import db
app = Flask(__name__)


# init database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@35.198.8.198:3306/papernotee'
db.init_app(app)

#import database

# init blueprint
from user_controller import user_info_bru
from paper_controller import paper_bru
from notes_controller import note_bru
from fanRelation_controller import fans_bru
app.config["SECRET_KEY"] = "renyizifuchuan"

CORS(app, supports_credentials=True)
app.register_blueprint(user_info_bru)
app.register_blueprint(note_bru)
app.register_blueprint(paper_bru)
app.register_blueprint(fans_bru)




@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "GET":

        return "crazy crazy"

@app.route('/create_all', methods=['GET', 'POST'])
def create_all():
    if request.method == "GET":
        print('start create table')
        db.create_all()
        return "successfully create_all tables"


if __name__ == '__main__':
    #start create tablet

    app.run(debug = True)