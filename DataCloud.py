
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect,url_for
from flask import jsonify
import json
from good import list
app = Flask(__name__)

'''
@app.route('/',methods=['GET','POST'])
def home():
    print('-----------')
    return render_template('main.html')
'''

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('mainPage.html')


@app.route('/search/',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        print(data['name']+data['province'])
        province = str(data['province'])
        name = str(data['name'])
        doctorlist1 = list(province,name)
        doctorlist2 = []
        for i in range (0,len(doctorlist1)):
            tuple = []
            for j in [14,1,6,3,4,13]:
                tuple.append(doctorlist1[i][j])
            doctorlist2.append(tuple)


        print(doctorlist2)

        return jsonify(doctorlist2)
    else:
        return render_template('searchPage.html')






if __name__=='__main__':
    app.run()