from flask import Flask, render_template, url_for, request, redirect
from db import Score_DB
import os


app = Flask(__name__)
score_db = Score_DB('C:\\Users\\Admin\\PycharmProjects\\Flask_App\\static\\score.db')

quiz_data = {
    'title': 'Python Programming Quiz',
    'questions': [
        {
            'type': 'radio',
            'id': 1,
            'question_text': 'What is the capital of France?',
            'options': ['Paris', 'Berlin', 'London', 'Madrid'],
            'correct_answer': 'Paris'
        },
        {
            'type': 'radio',
            'id': 2,
            'question_text': 'Which programming language is this quiz about?',
            'options': ['Java', 'Python', 'C++', 'JavaScript'],
            'correct_answer': 'Python'
        },
        {
            'type': 'radio',
            'id': 3,
            'question_text': 'Which of the following is used in pencils?',
            'options': ['Graphite', 'Iron', 'Carbon', 'Silicon'],
            'correct_answer': 'Graphite'
        },
    ]
}

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/articles')
def articles():
    return render_template("article.html")

@app.route('/authors')
def authors():
    return render_template("authors.html")

@app.route('/quiz')
def quiz():
    return render_template("quiz.html", title=quiz_data['title'], quiz_title=quiz_data['title'],
                           questions=quiz_data['questions'])

@app.route('/quiz', methods=['POST'])
def quiz_post():
    user_answers = {key: value for key, value in request.form.items()}
    user_name = request.form['username']
    score, total_questions = calculate_score(user_answers)
    score_db.new_score(user_name, score)
    all_scores = score_db.get_scores()[::-1]
    print(all_scores)
    return render_template('result.html', title='Quiz Result', score=score, total_questions=total_questions,
                           score_ratings=all_scores)

def calculate_score(user_answers):
    score = 0
    total_questions = len(quiz_data['questions'])

    for question in quiz_data['questions']:
        question_id = question['id']
        user_answer = user_answers.get(str(question_id))
        if user_answer and user_answer == question['correct_answer']:
            score += 1

    return score, total_questions

if __name__ == '__main__':
    app.run(debug=True)