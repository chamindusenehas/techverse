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
    collection2.update_one(
        {'name': 'lock'},  # Filter for the 'lock' document
        {'$set': {'status': True}},  # Set the status to True (locked)
        upsert=True  # Create the document if it doesn't exist
    )
    return jsonify({'status': 'locked'})


@app.route('/answer', methods=['POST'])
def answer():
    # Answer was provided within 10 seconds, reset buzzer timer and unlock
    global buzzer_timer_running
    buzzer_timer_running = False
    
    # Unlock the quiz for everyone else to buzz again
    collection2.update_one(
        {'name': 'lock'},  # Filter for the 'lock' document
        {'$set': {'status': False}},  # Set the status to False (unlocked)
        upsert=True  # Create the document if it doesn't exist
    )
    
    return jsonify({'status':'unlocked'})

@app.route('/check_lock', methods=['GET'])
def check_lock():
    # Retrieve the lock status from the 'locking' collection
    lock_status = collection2.find_one({'name': 'lock'}).get('status', False)
    return jsonify({'locked': lock_status})

@app.route('/reset_timer', methods=['POST'])
def reset_timer():
    # Reset all players' main timers after the buzzer timeout
    collection.update_one({'name': 'main_timer'}, {'$set': {'status': True}}, upsert=True)
    return jsonify({'status': 'reset'})

@app.route('/get_timer_status', methods=['GET'])
def get_timer_status():
    main_timer_status = collection.find_one({'name': 'main_timer'}).get('status', False)
    return jsonify({'status': main_timer_status})








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

    # Load questions data from JSON
    json_data = load_json('data/questions.json')



    selected_answer = request.form.get(f'q{not_showed[0]}')  # Retrieves answer for the current question index
    print(selected_answer)
    print(json_data[not_showed[0]]['answer'])



    # Ensure the answer is available and compare with correct answer
    if selected_answer:
        correct_answer = json_data[not_showed[0]]['answer']  # Get the correct answer from the JSON


        # Compare answers and adjust score accordingly
        if selected_answer == correct_answer:
            score += 10  # Correct answer, increase score by 10
        else:
            if score > 5:
                score -= 5
            else:
                score = 0  # Incorrect answer, decrease score by 5

    # Update the score in MongoDB
    collection.update_one({'username': username}, {'$set': {'quiz-score': score}})



    # Manage question flow
    if len(showed) < 40:  # Continue until 40 questions are displayed
        # Mark the current question as answered
        showed.append(not_showed[0])

        # Move to the next question index
        next_question_index = not_showed[1] if len(not_showed) > 1 else None  # Get the next index from not_showed

        if next_question_index is not None:
            # Update not_showed to remove the answered question
            not_showed = not_showed[1:]

            # Increment question number
            question_number += 1

            # Return the next question
            return render_template('quiz.html', gather=json_data, index=next_question_index, qnum=question_number, button='next')
        else:
            # If no more questions, reset or move to the submission page
            reset_quiz_state()
            return redirect(url_for('submit'))
    else:
        # End the quiz and submit answers
        reset_quiz_state()
        return redirect(url_for('submit'))

def reset_quiz_state():
    # Reset the quiz state for the next attempt
    global showed, question_number, unique_random_integer, score, not_showed
    showed = []
    question_number = 1
    unique_random_integer = 0
    score = 0
    not_showed = generate_question_order()  # Assuming you have a function to regenerate the question order

def generate_question_order():
    # Logic for generating a shuffled list of question indices (not_showed)
    return list(range(len(load_json('data/questions.json'))))  # Replace with actual logic to create question order


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)

