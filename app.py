from flask import Flask,render_template,request, redirect, url_for,jsonify
import json
import random
from pymongo import MongoClient
import time


app = Flask(__name__)


client = MongoClient('mongodb+srv://chamindusenehas:Chamee.19721@techverse.msx3fg5.mongodb.net/?retryWrites=true&w=majority&appName=techverse')
db = client['quiz']
collection = db['students']
collection2 = db['locking']
collection3 = db['players']





def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
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
    global round1,round2
    username = request.form['username']
    password = request.form['password']
    try:
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
                'school': username,
                'quiz-score': 0,
                'Biology-score':0,
                'Chemistry-score':0,
                'Mathematics-score':0,
                'Physics-score':0
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
    global round1,round2
    collection3.delete_many({})
    return render_template('main.html',text='yes',)

question_number = 1
showed = []
not_showed = [2,0,1,3]

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

main_timer_running = False
buzzer_timer_running = False


@app.route('/buzz', methods=['POST'])
def buzz():
    collection2.update_one({'name': 'lock'}, {'$set': {'status': True}}, upsert=True)
    return jsonify({'status': 'locked'})

@app.route('/answer', methods=['POST'])
def answer():

    collection2.update_one({'name': 'lock'}, {'$set': {'status': False}}, upsert=True)
    collection3.update_one(
        {'username': username},
        {'$set': {'ready': False}},
        upsert=True
    )
    return jsonify({'status': 'unlocked'})

@app.route('/check_lock', methods=['GET'])
def check_lock():
    lock_status = collection2.find_one({'name': 'lock'})
    print(lock_status['status'])
    return jsonify({'locked': lock_status['status']})

@app.route('/reset_timer', methods=['POST'])
def reset_timer():
    collection2.update_one({'name': 'lock'}, {'$set': {'status': False}})
    return jsonify({'status': 'reset'})
@app.route('/get_timer_status', methods=['GET'])
def get_timer_status():
    main_timer_status = collection.find_one({'name': 'main_timer'}).get('status', False)
    return jsonify({'status': main_timer_status})


@app.route('/check_update', methods=['GET'])
def check_update():

    lock_status = collection2.find_one({'name': 'lock'})
    if lock_status:

        return jsonify({'status': lock_status['status']})
    else:
        return jsonify({'status': None})

@app.route('/join_quiz', methods=['GET'])
def join_quiz():
    collection3.update_one(
        {'username': username},
        {'$set': {'ready': True}},
        upsert=True
    )
    return render_template('waiting.html') 

@app.route('/join_quizzee', methods=['GET'])
def checker():
    num = collection3.count_documents({'ready': True})
    if num >= 2:
        return jsonify({'start_quiz': True}) 
    else:
        return jsonify({'start_quiz': False})
    
subjected =[]
 

@app.route('/subject')
def subjecteddd():
    global subjected
    return render_template('subject.html',used=subjected)

round1 = False
round2 = False


@app.route('/touching', methods=['POST'])
def touching():
    global round1, round2
    round = request.json.get('round')
    
    if round == 1 and not round1:
        round1 = True
    elif round == 2 and not round2:
        round2 = True
    
    return jsonify({"round1_locked": round1, "round2_locked": round2})


subject = None


@app.route('/select_subject', methods=['POST'])
def select_subject():
    global subject
    data = request.get_json()
    subject = data.get('subject')
    if subject:
        return jsonify({"success": True,'subject':subject})
    else:
        return jsonify({"success": False, "message": "Subject not found"})



@app.route('/numbers', methods=['GET'])
def select_subjec2t():
    global subject,qnums,qnumber
    return render_template('numbers.html',subjective=subject ,qnums=qnums)





def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)





json_data = load_json('data/round1.json')
selected_question = None
count = 0
qnumber = None
qnums = []

@app.route('/submit_question', methods=['POST'])
def submit_question():
    global subject, selected_question, count, qnumber, qnums
    data = request.get_json()
    qnumber = data.get('qnumber')
    qnums.append(qnumber+1)

    # Initialize bomb with a default value (like -1 or some other indicator of failure)
    bomb = -1

    # Check which subject and assign corresponding bomb value
    if subject == 'Biology':
        bomb = 0
    elif subject == 'Chemistry':
        bomb = 1
    elif subject == 'Physics':
        bomb = 2
    elif subject == 'Mathematics':
        bomb = 3

    # Check if bomb was assigned a valid value
    if bomb == -1:
        return jsonify({"message": "Invalid subject"}), 400

    # Now proceed with accessing the questions
    questions = json_data[bomb][subject]


    selected_question = questions[qnumber]
    count += 1
    return jsonify({"redirect": url_for('question_page')})


@app.route('/question_page')
def question_page():
    global selected_question
    return render_template('question_page.html',question=selected_question)


@app.route('/submit_answer',methods=['POST'])
def submit_answer():
    global subjected,subject,count,qnums
    answer = request.form.get('selected_answer')
    trueAnswer = selected_question['answer']
    print(answer)
    print(trueAnswer)
    print(username)
    if answer == trueAnswer:
        score = 10
    else:
        score = 0
    collection.update_one({f'username': username}, {'$inc': {f'{subject}-score': score}})
    if count < 4:
        print(count)
        return redirect('/numbers')
    else:
        subjected.append(subject)
        count = 0
        qnums = []
        return redirect('/subject')




    






























@app.route('/quiz', methods=['POST'])
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



    selected_answer = request.form.get(f'q{not_showed[0]}')
    print(selected_answer)
    print(json_data[not_showed[0]]['answer'])



 
    if selected_answer:
        correct_answer = json_data[not_showed[0]]['answer'] 


      
        if selected_answer == correct_answer:
            score += 10 
        else:
            if score > 5:
                score -= 5
            else:
                score = 0 

   
    collection.update_one({'username': username}, {'$set': {'quiz-score': score}})



   
    if len(showed) < 40:
       
        showed.append(not_showed[0])

       
        next_question_index = not_showed[1] if len(not_showed) > 1 else None 

        if next_question_index is not None:
           
            not_showed = not_showed[1:]

          
            question_number += 1

          
            return render_template('quiz.html', gather=json_data, index=next_question_index, qnum=question_number, button='next')
        else:
           
            reset_quiz_state()
            return redirect(url_for('submit'))
    else:
      
        reset_quiz_state()

        return redirect(url_for('submit'))
    



    
def reset_quiz_state():
   
    global showed, question_number, unique_random_integer, score, not_showed
    showed = []
    question_number = 1
    unique_random_integer = 0
    score = 0
    not_showed = generate_question_order() 

def generate_question_order():
   
    return list(range(len(load_json('data/questions.json'))))












if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)

