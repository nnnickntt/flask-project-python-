from flask import Flask, render_template, request
from blueprints.dashboard import dashboard
from urllib.request import urlopen
from models import db, Student
import requests, base64, json

ml_url = "http://127.0.0.1:2000/fruitml"
fruit_url = "http://127.0.0.1:2000/fruit"

UPLOAD_FOLDER = './static/uploads'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()

app.register_blueprint(dashboard)
# app.register_blueprint(addfruit)


@app.route('/about')
def about():
    student = Student.query.all()
    return render_template('about.html', student=student)


@app.route('/fruitml', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        img = request.files['file1']
        img_string = base64.b64encode(img.read())
        stringdec = img_string.decode('utf-8')
        pred_result = fruitml(stringdec)
        data = get_fruit_list()

        return render_template('prediction.html', pred_result=pred_result, data=data)
    return render_template('upload.html')

def fruitml(stringdec):
    try:
        ml = None
        ml = {
            'key': "imagefruit",
            'base64': stringdec
        }
        x = requests.post(ml_url, json = ml)
        # แปลง x เป็น json
        return x.json()
    except:
        return print("failml")

def get_fruit_list():
    try:
        data = urlopen(fruit_url).read()
        parsed = json.loads(data)
        data = []
        if parsed.get('data_fruit'):
            data = parsed.get('data_fruit')
        return data
    except:
        return data

app.env="development"
app.run(debug=True)
