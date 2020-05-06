from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
UPLOAD_FOLDER = './app/static/uploads'
SECRET_KEY = 'fjfjdjkfhdhrs12rf456fghtu6543'

app.config['SECRET_KEY'] = "WDRE3453wvigjd324VEERSD"
app.config['SQLALCHEMY_DATABASE_URI']="postgres://project2:project21234@localhost/project2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)


from app import views