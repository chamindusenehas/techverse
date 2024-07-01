from flask import Flask,render_template,request, redirect, url_for
import json
import random


app = Flask(__name__)

def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

score = 0
user1 = ''
user2 = ''
user3 = ''
user4 = ''
user5 = ''
user6 = ''
school = ''


@app.route('/')
def home():
    global score 
    score = 0
    return render_template('coder.html')

@app.route('/submit', methods=['POST'])
def submit():
    global user1
    global user2
    global user3
    global user4
    global user5
    global user6
    global school
    user1 = request.form['username1']
    user2 = request.form['username2']
    user3 = request.form['username3']
    user4 = request.form['username4']
    user5 = request.form['username5']
    user6 = request.form['username6']

    school = request.form['school']
    return redirect(url_for('quiz'))

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
    global user2
    global user1
    global user3
    global user4
    global user5
    global user6
    global school
    json_data = load_json('data/questions.json')
    answersheet = request.form.get(f'q{unique_random_integer}')
    if answersheet == json_data[unique_random_integer]['answer']:
        score += 5

    con = True
    while con == True:
        unique_random_integer = random.randint(0,40)
        if not len(showed) <= 40:
            break
        if unique_random_integer not in showed:
            con = False
            showed.append(unique_random_integer)

    if len(showed) <= 40 :
        print(len(showed))
        question_number += 1
        if len(showed) >= 40:
            return render_template('quiz.html',gather=json_data,index=unique_random_integer,qnum=question_number,button='submit')
        else:
            return render_template('quiz.html',gather=json_data,index=unique_random_integer,qnum=question_number,button='next')
    else:
        print(f'{len(showed)} end')
        showed = []
        question_number = 1
        new_data = {'student1': user1,'student2':user2 ,'student3': user3,'student4':user4 ,'student5': user5,'student6':user6 , 'school': school,'score':score}

        def load_data():
            try:
                with open('scores.json', "r") as file:
                    data = json.load(file)
            except:
                data = {}
            return data
        
        def save_data(data):
            with open('scores.json', "w") as file:
                json.dump(data, file, indent=4)
        data = load_data()
        cond = True
        while cond ==True:
            random_number = random.randint(0,1000)
            if f'{random_number}' not in data:
                cond = False
                data[f"{random_number}"] = new_data
                save_data(data)
        
        return render_template('completed.html',score=score)

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)

