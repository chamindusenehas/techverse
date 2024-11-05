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
used_time = 0
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
        x = 0
        for y in collection.find({'username':username}):
            if y['username'] == username:
                x = 1
            else:
                x = 0
        if x == 1:
            return render_template('coder.html',txt='no')
        else:
            collection.insert_one({
                'username': username,
                'password': password,
                'school': school,
                'used-time': 0,
                'quiz-score': 0,
                'ai-score':0,
                'web-score':0,
                'cyber-score':0,
                }
            )
            return render_template('main.html')
    except:
        try:
            if not(collection.find({'username': username})) :
                return render_template('coder.html',txt='yes')
            elif password != collection.find_one({'username':username})['password']:
                return render_template('coder.html',txt='yes')
            else:
                return render_template('main.html')
        except:
            return render_template('coder.html',txt='yes')

@app.route('/submit',methods=['GET'])
def submitt():
    return render_template('main.html',text='yes')

question_number = 1
showed = []
not_showed = [23, 33, 14, 7, 20, 28, 8, 24, 0, 1, 10, 19, 34, 11, 37, 18, 21, 9, 27, 6, 31, 26, 12, 38, 36, 35, 25, 17, 39, 2, 15, 4, 29, 3, 16, 32, 22, 5, 13, 30]

score = 0
unique_random_integer = 0

@app.route('/quiz',methods=['GET'])
def quiz():
    global showed
    global unique_random_integer
    global question_number
    question_number = 1
    showed =[]
    global not_showed
    json_data = load_json('data/questions.json')
    showed.append(0)
    print(len(showed))
    return render_template('quiz.html',gather=json_data,index=not_showed[0],qnum=question_number,button='next')



@app.route('/quiz',methods=['POST'])
def quizz():
    global showed
    global score
    global unique_random_integer
    global question_number
    global school
    global username
    global collection
    global not_showed
    global used_time
    json_data = load_json('data/questions.json')
    answersheet = request.form.get(f'q{0}')
    score = request.form.get('beach')
    collection.update_one({'username':username},{'$set':{'used-time':score}})
    print(str(score) + 'this is the time lefted...' )


    numb = 0


    if len(showed) <= 40 :
        question_number += 1
        numb += 1
        return render_template('quiz.html',gather=json_data,index=not_showed[numb],qnum=question_number,button='buzz')
    else:
        print(f'{len(showed)} end')
        showed = []
        question_number = 1
        collection.update_one({'username':username},{'$set':{'used-time':used_time}})
        unique_random_integer = 0
        score = 0
        
        return redirect(url_for('submit'))

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)

