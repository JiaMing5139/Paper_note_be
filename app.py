from flask import Flask
from flask import request
from flask_cors import CORS
from dbext import db
app = Flask(__name__)


# init database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@35.199.106.213:3306/papernote'
db.init_app(app)
with app.app_context():
    db.create_all()
#import database

# init blueprint
from user_info import user_info_bru
from paper import paper_bru
app.config["SECRET_KEY"] = "renyizifuchuan"

CORS(app, supports_credentials=True)
app.register_blueprint(user_info_bru)
app.register_blueprint(paper_bru)



@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "GET":
        return "crazy crazy"


if __name__ == '__main__':

    app.run(debug = True)