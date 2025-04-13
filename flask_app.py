from flask import Flask, render_template, url_for, request, redirect, session
from random import sample
from db import Score_DB
import os


app = Flask(__name__)
score_db = Score_DB('C:\\Users\\Admin\\PycharmProjects\\etustory\\static\\score.db')
app.secret_key = 'BAD_SECRET_KEY'

quiz_data = {
    'title': 'Тест 139 лет ЛЭТИ',
    'questions': [
        {
            'type': 'radio',
            'id': 0,
            'src': 'path',
            'question_text': 'Кто подписал указ о преобразовании технического училища в электротехничекий институт',
            'options': ['Александр II', 'Александр III', 'Николай II', 'А. С. Колпаков'],
            'correct_answer': 'Александр III'
        },
        {
            'type': 'radio',
            'id': 1,
            'src': 'path',
            'question_text': 'Кто основал первую в России кафедру теоретических основ электротехники в ЭТИ',
            'options': ['А. С. Попов', 'Г. О. Графтио', 'Н. А. Быков', 'И. И. Боргман'],
            'correct_answer': 'И. И. Боргман'
        },
        {
            'type': 'radio',
            'id': 2,
            'src': 'path',
            'question_text': 'С каким докладом выступил А. С. Попов перед преподатвателями и студентами ЭТИ в 1897 году?',
            'options': ['Об электрической тяге', 'О технике высоких напряжений', 'О беспроволочной телеграфии', 'О технике малых напряжений'],
            'correct_answer': 'О беспроволочной телеграфии'
        },
        {
            'type': 'radio',
            'id': 3,
            'src': 'path',
            'question_text': 'В каком году электротехничекий институт получил статусвысшего учебного заведения с введением пятикурсного обучения?',
            'options': ['1899', '1897', '1891', '1488'],
            'correct_answer': '1899'
        },
        {
            'type': 'radio',
            'id': 4,
            'src': 'path',
            'question_text': 'Какое звание присваивалось выпускникам ЭТИ начиная с 1900 года?',
            'options': ['Инжинер-механик', 'Инжинер-электрик', 'Инжинер-строитель', 'Электротехник'],
            'correct_answer': 'Инжинер-электрик'
        },
        {
            'type': 'radio',
            'id': 5,
            'src': 'path',
            'question_text': 'Кто был избран директором ЭТИ в 1905 году?',
            'options': ['А. С. Попов', 'Г. О. Графтио', 'Н. А. Быков', 'Г. О. Осадчий'],
            'correct_answer': 'А. С. Попов'
        },
        {
            'type': 'radio',
            'id': 6,
            'src': 'path',
            'question_text': 'В каком году электротехнический институт императора Александра III был переименован в Электротехнический институт имени В. И. Ульянова?',
            'options': ['1917', '1918', '1924', '1930'],
            'correct_answer': '1918'
        },
        {
            'type': 'radio',
            'id': 7,
            'src': 'path',
            'question_text': 'В каком году ЛЭТИ наградиил орденом Ленина за большие заслуги в подготовке инжинерных кадров?',
            'options': ['1945', '1957', '1967', '1986'],
            'correct_answer': '1967'
        },
        {
            'type': 'radio',
            'id': 8,
            'src': 'path',
            'question_text': "В каком году ЛЭТИ получил статус технического университета и новое название - 'Санкт-Петербургский государственный электротехнический университет имени В. И. Ульянова'",
            'options': ['1989', '1990', '1991', '1992'],
            'correct_answer': '1992'
        },
        {
            'type': 'radio',
            'id': 9,
            'src': 'path',
            'question_text': 'В каком году выпускник ЛЭТИ Жорес Алферов получил нобелевскую премию по физике?',
            'options': ['1994', '1996', '1998', '2000'],
            'correct_answer': '2000'
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
    return render_template("quiz-start.html")

@app.route('/quiz/<int:id>')
def question(id):
    ans = quiz_data['questions'][id]
    ans['options'] = sample(ans['options'], k=len(ans['options']))
    return render_template('question.html', question=ans)

@app.route('/quiz/results')
def results():
    score_db.new_score(session['username'], session['score'])
    all_scores = score_db.get_scores()[::-1]
    return render_template('result.html', title='Quiz Result', score=session['score'],
                           total_questions=len(quiz_data['questions']),
                           score_ratings=all_scores)


@app.route('/quiz/<int:id>', methods=['POST', 'GET'])
def question_processing(id):
    ans = quiz_data['questions'][id]
    try:
        user_answers = [value for key, value in request.form.items()][0]
        if check_answer(user_answers, ans['correct_answer']):
            session['score'] += 1
            if id != 9:
                return render_template('answer.html', image=ans['src'], new_id=ans['id'] + 1, text="Верно")
            return render_template('answer_toresult.html', image=ans['src'], text="Верно")
        if id != 9:
            return render_template('answer.html', image=ans['src'], new_id=ans['id'] + 1, text="Неверно")
        return render_template('answer_toresult.html', image=ans['src'], text="Неверно")
    except Exception:
        return redirect( url_for('question', id=id))


def check_answer(client_answer, right_answer):
    if client_answer == right_answer:
        return True
    return False

@app.route('/quiz', methods=['POST'])
def quiz_post():
    session['username'] = request.form['username']
    session['score'] = 0
    return redirect(url_for('question', id = 0))

if __name__ == '__main__':
    app.run(debug=True)