from flask import Flask,jsonify
from flask_restx import Resource, Api, fields
from PIL import Image
from ml_model import TFModel
from PIL import Image
import base64, json, io

UPLOAD_FOLDER = './static/uploads'

app = Flask(__name__)
api = Api(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

img_input = api.model('Image', {
    'key': fields.String(required=True, description='key'),
    'base64': fields.String(required=True, description='base64 string')
})

# เปิดและอ่านไฟล์
f = open('fruit.json')
data_fruit = json.load(f)

model = TFModel(model_dir='./ml-model/')
model.load()

class fruitList(Resource):
    def get(self):
        # return ข้อมูลทั้งหมด
        return jsonify({'data_fruit': data_fruit})

    def post(self):
        # กำหนดข้อมูลที่จะใส่ตามไฟล์ json
        fruit = {
            'Name': api.payload['Name'],
            'Calories': api.payload['Calories'],
            'TotalFat': api.payload['TotalFat'],
            'Sodium': api.payload['Sodium'],
            'TotalCarb': api.payload['TotalCarb'],
            'Protein': api.payload['Protein'],
            'Calcium': api.payload['Calcium'],
            'Iron': api.payload['Iron'],
            'Potassium': api.payload['Potassium'],
        }
        # เพิ่มข้อมูลใหม่ลงข้อมูลเดิม
        data_fruit.append(fruit)
        return "successfully added"

class Editfruit(Resource):

    def delete(self,fruit):
        for check in data_fruit:
            if check['Name'] == fruit:
                # ลบ check ที่มี Name ตรงกับที่ user ใส่เข้ามา
                data_fruit.remove(check)
        return 'successfully delete data'

    def put(self, fruit):
        # ลูปข้อมูล i เป็นเลขเริ่มจาก 0 t เป็นข้อมูลเหมือน check
        for i, t in enumerate(data_fruit):
            if t['Name'] == fruit:
                
                fruit = {
                'Name': api.payload['Name'],
                'Calories': api.payload['Calories'],
                'TotalFat': api.payload['TotalFat'],
                'Sodium': api.payload['Sodium'],
                'TotalCarb': api.payload['TotalCarb'],
                'Protein': api.payload['Protein'],
                'Calcium': api.payload['Calcium'],
                'Iron': api.payload['Iron'],
                'Potassium': api.payload['Potassium'],
                }
                # ตั้งค่า data_fruit index ที่ i ให้เป็นอันใหม่ที่เราตั้ง
                data_fruit[i] = fruit

        return fruit

class Classification(Resource):

    @api.expect(img_input)
    def post(self):
        
        key_string = api.payload['key']
        img_string = api.payload['base64']
        imgdata = base64.b64decode(img_string)
 
        image_temp = Image.open(io.BytesIO(imgdata))

        outputs = model.predict(image_temp)

        outputs['key'] = key_string
        return jsonify(outputs)


# เป็น link สำหรับเรียกดูข้อมูล  
api.add_resource(fruitList,'/fruit')
api.add_resource(Editfruit,'/fruit/<fruit>')
api.add_resource(Classification,'/fruitml')


