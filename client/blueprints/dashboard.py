from flask import Blueprint, render_template, request, redirect
from urllib.parse import quote
from urllib.request import urlopen
import json
import requests

dashboard = Blueprint('dashboard', __name__)

fruit_url = "http://127.0.0.1:2000/fruit"
fruit_specific_url = "http://127.0.0.1:2000/specific/{0}"
fruit_update_url = "http://127.0.0.1:2000/fruit/"
fruit_delete_url = "http://127.0.0.1:2000/fruit/"


@dashboard.route("/")
def dash():
    fruit = request.args.get('fruit')
    if not fruit:
        fruit = 'apple'
    data_list = get_fruit_list()
    data = get_fruit(fruit)
    return render_template("dashboard.html", data_list=data_list, data=data)

def get_fruit(fruit):
    try:
        query = quote(fruit)
        url = fruit_specific_url.format(query)
        data = urlopen(url).read()
        parsed = json.loads(data)
        data = None

        if parsed.get('Name'):

            Name = parsed['Name']
            Calories = parsed['Calories']
            TotalFat = parsed['TotalFat']
            Sodium = parsed['Sodium']
            TotalCarb = parsed['TotalCarb']
            Protein = parsed['Protein']
            Calcium = parsed['Calcium']
            Iron = parsed['Iron']
            Potassium = parsed['Potassium']
            data = {'Name': Name,
                'Calories': Calories,
                'TotalFat': TotalFat,
                'Sodium': Sodium,
                'TotalCarb':TotalCarb,
                'Protein': Protein,
                'Calcium': Calcium,
                'Iron':Iron,
                'Potassium': Potassium,
                }
        return data
    except:
        data = {'Name': "Not found"}
        return data

def get_fruit_list():
    try:
        data = urlopen(fruit_url).read()
        parsed = json.loads(data)
        data = []
        if parsed.get('data_fruit'):
            data = parsed.get('data_fruit')
            # for data_l in parsed.get('data_fruit'):
            #     Name = data_l['Name']
            #     Calories = data_l['Calories']
            #     TotalFat = data_l['TotalFat']
            #     Sodium = data_l['Sodium']
            #     TotalCarb = data_l['TotalCarb']
            #     Protein = data_l['Protein']
            #     Calcium = data_l['Calcium']
            #     Iron = data_l['Iron']
            #     Potassium = data_l['Potassium']
            #     print(data_l)
            #     data_r = {
            #         'Name': Name,
            #         'Calories': Calories,
            #         'TotalFat': TotalFat,
            #         'Sodium': Sodium,
            #         'TotalCarb': TotalCarb,
            #         'Protein': Protein,
            #         'Calcium': Calcium,
            #         'Iron': Iron,
            #         'Potassium': Potassium
            #         }
            #     print(data_r)
            #     data.append(data_r)
                # print(data_l['Name'])
        return data
    except:
        return data

@dashboard.route("/fruit/add", methods=["POST"])
def add():
        Name = request.form['addname']
        Calories = request.form['addcal']
        TotalFat = request.form['addfat']
        Sodium = request.form['addsodium']
        TotalCarb = request.form['addcarb']
        Protein = request.form['addprotein']
        Calcium = request.form['addcalcium']
        Iron = request.form['addiron']
        Potassium = request.form['addpotassium']
        # result = request.form['result']
        add_fruit(Name, Calories, TotalFat, Sodium, TotalCarb, Protein, Calcium, Iron, Potassium)
        return redirect("/")

def add_fruit(Name, Calories, TotalFat, Sodium, TotalCarb, Protein, Calcium, Iron, Potassium):
    try:
        fruit = None
        fruit = {
            'Name': Name,
            'Calories': float(Calories),
            'TotalFat': float(TotalFat),
            'Sodium': float(Sodium),
            'TotalCarb': float(TotalCarb),
            'Protein': float(Protein),
            'Calcium': float(Calcium),
            'Iron': float(Iron),
            'Potassium': float(Potassium)
        }
        x = requests.post(fruit_url, json = fruit)
        print(x)
    except:
        return print("fail to add")

@dashboard.route("/fruit/put", methods=["PUT", "GET", "POST"])
def update():
    if request.method == "GET":
        Name = request.args.get('editname')
        Calories = request.args.get('editcal')
        TotalFat = request.args.get('editfat')
        Sodium = request.args.get('editsodium')
        TotalCarb = request.args.get('editcarb')
        Protein = request.args.get('editprotein')
        Calcium = request.args.get('editcalcium')
        Iron = request.args.get('editiron')
        Potassium = request.args.get('editpotassium')
    else:
        Name = request.form['editname']
        Calories = request.form['editcal']
        TotalFat = request.form['editfat']
        Sodium = request.form['editsodium']
        TotalCarb = request.form['editcarb']
        Protein = request.form['editprotein']
        Calcium = request.form['editcalcium']
        Iron = request.form['editiron']
        Potassium = request.form['editpotassium']
        update_fruit(Name, Calories, TotalFat, Sodium, TotalCarb, Protein, Calcium, Iron, Potassium)
    return redirect('/')

def update_fruit(Name, Calories, TotalFat, Sodium, TotalCarb, Protein, Calcium, Iron, Potassium):
    try:
        fruit = None
        fruit = {
            'Name': Name,
            'Calories': float(Calories),
            'TotalFat': float(TotalFat),
            'Sodium': float(Sodium),
            'TotalCarb': float(TotalCarb),
            'Protein': float(Protein),
            'Calcium': float(Calcium),
            'Iron': float(Iron),
            'Potassium': float(Potassium)
        }
        upfruit = fruit_update_url+Name
        x = requests.put(upfruit, json = fruit)
        # data = urlopen(x).read()
        print(x)
        return x
    except:
        return ("fail to update")

@dashboard.route("/fruit/delete", methods=["PUT", "GET", "POST"])
def delete():
    if request.method == "GET":
        Name = request.args.get('deletename')
    else:
        Name = request.form['deletename']
        delete_fruit(Name)
    return redirect('/')
 
def delete_fruit(Name):
    try:
        fruit = None
        fruit = {
            'Name': Name
        }
        delfruit = fruit_delete_url+Name
        x = requests.delete(delfruit, json = fruit)
        # data = urlopen(x).read()
        return x
    except:
        return ("fail to delete")

