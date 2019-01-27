import os
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = "apisecret"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
data_input = ROOT_DIR + "/data_input"
data_output = ROOT_DIR + "/data_output"
velocity_input = ROOT_DIR + "/controllers/velocity/velocity_input"
velocity_output = ROOT_DIR + "/controllers/velocity/velocity_output"
velocity_model = ROOT_DIR + "/controllers/velocity/velocity_model"
vemos2009_vx = velocity_model + "/vemos2009_vx.grd"
vemos2009_vy = velocity_model + "/vemos2009_vy.grd"
vemos2009_vz = velocity_model + "/vemos2009_vz.grd"
app.config['UPLOAD_FOLDER'] = data_input
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "transformacion.itr.online@gmail.com"
app.config['MAIL_PASSWORD'] = "Testing2018"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
