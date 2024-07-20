from flask import Flask,render_template,request, redirect, url_for
import json
import random
from pymongo import MongoClient
import time


app = Flask(__name__)


client = MongoClient('mongodb+srv://chamindusenehas:Chamee.19721@techverse.msx3fg5.mongodb.net/?retryWrites=true&w=majority&appName=techverse')
db = client['quiz']
collection = db['students']





def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

score = 0
username = ''
school = ''
password = ''


@app.route('/')
def home():
    global score 
    score = 0
    return render_template('coder.html')

@app.route('/submit', methods=['POST'])
def submit():
    global school
    global username
    global password
    global collection
    username = request.form['username']
    password = request.form['password']
    try:
        school = request.form['school']
        collection.insert_one({
            'username': username,
            'password': password,
            'school': school,
            'score': 0}
        )
    except:
        pass
    return render_template('main.html')

@app.route('/submit',methods=['GET'])
def submitt():
    return render_template('main.html',text='yes')

question_number = 1
showed = []
score = 0
unique_random_integer = 0

@app.route('/quiz',methods=['GET'])
def quiz():
    global showed
    global unique_random_integer
    global question_number
    showed =[]
    json_data = load_json('data/questions.json')
    unique_random_integer = random.randint(0,39)
    showed.append(unique_random_integer)
    print(len(showed))
    return render_template('quiz.html',gather=json_data,index=unique_random_integer,qnum=question_number,button='next')



@app.route('/quiz',methods=['POST'])
def quizz():
    global showed
    global score
    global unique_random_integer
    global question_number
    global school
    global username
    global collection
    json_data = load_json('data/questions.json')
    answersheet = request.form.get(f'q{unique_random_integer}')
    if answersheet == json_data[unique_random_integer]['answer']:
        score += 5
        collection.update_one({'username':username},{'$set':{'score':score}})


    con = True
    while con == True:
        unique_random_integer = random.randint(0,40)
        if not len(showed) <= 40:
            break
        if unique_random_integer not in showed:
            con = False
            showed.append(unique_random_integer)

    if len(showed) <= 2 :
        question_number += 1
        if len(showed) >= 40:
            return render_template('quiz.html',gather=json_data,index=unique_random_integer,qnum=question_number,button='submit')
        else:
            return render_template('quiz.html',gather=json_data,index=unique_random_integer,qnum=question_number,button='next')
    else:
        print(f'{len(showed)} end')
        showed = []
        question_number = 1
        collection.update_one({'username':username},{'$set':{'score':score}})
        unique_random_integer = 0
        
        return redirect(url_for('submit'))

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)

