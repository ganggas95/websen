from flask import Flask
import os
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'GIS Secret Key: bismillah!@#$%^'
UPLOAD_FOLDER = os.path.sep + 'uploads' + os.path.sep+"profile"+os.path.sep
DATA_FOLDER = os.path.sep + 'temp' + os.path.sep
app.config['UPLOAD_FOLDER'] = app.root_path +os.path.sep+"static"+ UPLOAD_FOLDER
app.config['DATA_FOLDER'] = app.root_path + DATA_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:keyfaton@localhost/websen_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

from websen import views, url