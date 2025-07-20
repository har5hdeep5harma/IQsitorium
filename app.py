from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

def load_questions():
    with open(os.path.join('data', 'iq_questions.json')) as f:
        return json.load(f)
IQ_QUESTIONS = load_questions()

def calculate_iq_score(form_data):
    score = 0
    for i, question in enumerate(IQ_QUESTIONS):
        selected = form_data.get(f'q{i}')
        if selected and selected == question['answer']:
            score += 1
    return score

def interpret_score(score):
    total = len(IQ_QUESTIONS)
    percentage = (score / total) * 100
    if percentage >= 90:
        return 'Genius (IQ 130+)'  
    elif percentage >= 75:
        return 'Above Average (IQ 110–129)'
    elif percentage >= 50:
        return 'Average (IQ 90–109)'
    elif percentage >= 25:
        return 'Below Average (IQ 70–89)'
    else:
        return 'Low (IQ <70)'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/iq_test', methods=['GET', 'POST'])
def iq_test():
    if request.method == 'POST':
        score = calculate_iq_score(request.form)
        level = interpret_score(score)
        return render_template('result.html', score=score, level=level, total=len(IQ_QUESTIONS))
    return render_template('iq_test.html', questions=IQ_QUESTIONS)

if __name__ == '__main__':
    app.run(debug=True)
