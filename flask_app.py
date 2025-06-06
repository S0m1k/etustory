from flask import Flask, render_template, url_for, request, redirect, session
from random import sample
from db import Score_DB
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
score_db = Score_DB("/data/score.db")
app.secret_key = 'BAD_SECRET_KEY'
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = {'txt', 'docx', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

image_lst = ['/static/check-ring-duotone0.svg', '/static/close-round-duotone0.svg'] # для доп картинок

quiz_data = {
    'title': 'Тест 139 лет ЛЭТИ',
    'questions': [
        {
            'type': 'radio', # я предполагаю что можно убрать тип
            'id': 0,
            'src': '/static/image-115.png',
            'question_text': 'Кто подписал указ о преобразовании технического училища в электротехничекий институт',
            'options': ['Александр II', 'Александр III', 'Николай II', 'А. С. Колпаков'],
            'correct_answer': 'Александр III',
            'cor_message': 'Абсолютно верно, это сделал Александр 3-ий  11-ого (23-его) июня 1891 года ',
            'wrong_message': '''Почти. 11 (23) июня 1891 года Император Александр III подписал указ о преобразовании Технического училища в Электротехнический институт (ЭТИ) с четырехлетним сроком обучения. Учебный план включал 20 дисциплин, из которых 7 – электротехнические..'''
        },
        {
            'type': 'radio',
            'id': 1,
            'src': '/static/image-311.png',
            'question_text': 'Кто основал первую в России кафедру теоретических основ электротехники в ЭТИ',
            'options': ['А. С. Попов', 'Г. О. Графтио', 'Н. А. Быков', 'И. И. Боргман'],
            'correct_answer': 'И. И. Боргман',
            'cor_message': 'Правильно! Профессор Петербургского университета И.И. Боргман основал эту кафедру в ЭТИ в 1893 году.',
            'wrong_message': '''Попробуйте еще раз! Кафедру теоретических основ электротехники основал И.И. Боргман, профессор Петербургского университета.'''
        },
        {
            'type': 'radio',
            'id': 2,
            'src': '/static/image-331.png',
            'question_text': 'С каким докладом выступил А. С. Попов перед преподатвателями и студентами ЭТИ в 1897 году?',
            'options': ['Об электрической тяге', 'О технике высоких напряжений', 'О беспроволочной телеграфии', 'О технике малых напряжений'],
            'correct_answer': 'О беспроволочной телеграфии',
            'cor_message': 'Отлично! Доклад А.С. Попова "О беспроволочной телеграфии" стал важным событием в развитии радиотехники в России.',
            'wrong_message': '''А.С. Попов представил доклад "О беспроволочной телеграфии", что стало важным шагом в истории радио.'''

        },
        {
            'type': 'radio',
            'id': 3,
            'src': '/static/image-341.png',
            'question_text': 'В каком году электротехничекий институт получил статусвысшего учебного заведения с введением пятикурсного обучения?',
            'options': ['1899', '1897', '1891', '1488'],
            'correct_answer': '1899',
            'cor_message': 'Блестяще! Это произошло в 1899 году, что значительно повысило уровень подготовки специалистов.',
            'wrong_message': '''Почти! Статус высшего учебного заведения был получен в 1899 году, тогда же было введено пятикурсное обучение.'''
        },
        {
            'type': 'radio',
            'id': 4,
            'src': '/static/image-351.png',
            'question_text': 'Какое звание присваивалось выпускникам ЭТИ начиная с 1900 года?',
            'options': ['Инжинер-механик', 'Инжинер-электрик', 'Инжинер-строитель', 'Электротехник'],
            'correct_answer': 'Инжинер-электрик',
            'cor_message': 'Именно! Выпускники становились "инженерами-электриками", что подчеркивало их специализацию.',
            'wrong_message': '''Вы были близки! С 1900 года выпускникам ЭТИ присваивалось звание "инженер-электрик".'''
        },
        {
            'type': 'radio',
            'id': 5,
            'src': '/static/image-361.png',
            'question_text': 'Кто был избран директором ЭТИ в 1905 году?',
            'options': ['А. С. Попов', 'Г. О. Графтио', 'Н. А. Быков', 'Г. О. Осадчий'],
            'correct_answer': 'А. С. Попов',
            'cor_message': 'Супер! Совет ЭТИ избрал А.С. Попова директором, что было признанием его заслуг.',
            'wrong_message': '''Не совсем так! Директором в 1905 году был избран А.С. Попов, изобретатель радио.'''
        },
        {
            'type': 'radio',
            'id': 6,
            'src': '/static/image-371.png',
            'question_text': 'В каком году электротехнический институт императора Александра III был переименован в Электротехнический институт имени В. И. Ульянова?',
            'options': ['1917', '1918', '1924', '1930'],
            'correct_answer': '1918',
            'cor_message': 'Да! Это произошло в 1918 году, после революции.',
            'wrong_message': ''' Переименование произошло в 1918 году, после революционных событий.'''
        },
        {
            'type': 'radio',
            'id': 7,
            'src': '/static/image-390.png',
            'question_text': 'В каком году ЛЭТИ наградиил орденом Ленина за большие заслуги в подготовке инжинерных кадров?',
            'options': ['1945', '1957', '1967', '1986'],
            'correct_answer': '1967',
            'cor_message': 'Превосходно! Высокая награда была получена в 1967 году.',
            'wrong_message': '''Не угадали! Орден Ленина ЛЭТИ получил в 1967 году.'''
        },
        {
            'type': 'radio',
            'id': 8,
            'src': '/static/image-401.png',
            'question_text': "В каком году ЛЭТИ получил статус технического университета и новое название - 'Санкт-Петербургский государственный электротехнический университет имени В. И. Ульянова'",
            'options': ['1989', '1990', '1991', '1992'],
            'correct_answer': '1992',
            'cor_message': 'Молодец! Это произошло в 1992 году, знаменуя новый этап в развитии вуза.',
            'wrong_message': '''Неправильный ответ: Чуть-чуть мимо! Статус технического университета был получен в 1992 году.'''
        },
        {
            'type': 'radio',
            'id': 9,
            'src': '/static/image-411.png',
            'question_text': 'В каком году выпускник ЛЭТИ Жорес Алферов получил нобелевскую премию по физике?',
            'options': ['1994', '1996', '1998', '2000'],
            'correct_answer': '2000',
            'cor_message': 'Браво! Алферов был награжден в 2000 году за свои выдающиеся работы в области полупроводниковых гетероструктур.',
            'wrong_message': '''Не в этот год! Жорес Алферов получил Нобелевскую премию в 2000 году.'''
        },
    ]
}

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/article/<string:slug>')
def article(slug):
     return render_template(f"article/{slug}.html")

@app.route('/authors')
def authors():
    return render_template("authors.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/authors', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print(allowed_file(file.filename))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home'))
    return redirect(url_for('authors'))

@app.route('/quiz')
def quiz():
    return render_template("quiz-start.html")

@app.route('/quiz/<int:id>')
def question(id):
    ans = quiz_data['questions'][id]
    ans['options'] = sample(ans['options'], k=len(ans['options']))
    return render_template('question.html', id=ans['id'], src=ans['src'],
                           question_text=ans['question_text'], options=ans['options'])

@app.route('/quiz/results')
def results():
    score_db.new_score(session['username'], session['score'])
    return render_template('result.html', score=session['score'],
                           total_questions=len(quiz_data['questions']))

@app.route('/quiz/allresults')
def allresults():
    all_scores = score_db.get_scores()[::-1]
    return render_template('allresults.html', score_ratings = all_scores)


@app.route('/quiz/<int:id>', methods=['GET', 'POST'])
def question_processing(id):
    ans = quiz_data['questions'][id]
    try:
        user_answers = [value for key, value in request.form.items()][0]
        if check_answer(user_answers, ans['correct_answer']):
            session['score'] += 1
            if id != 9:
                return render_template('answer.html', image1=ans['src'], image2=image_lst[0],
                                       new_id=ans['id'] + 1, text=ans['cor_message'])
            return render_template('answer_toresult.html', image1=ans['src'], image2=image_lst[0],
                                   text=ans['cor_message'])
        if id != 9:
            return render_template('answer.html', image1=ans['src'], image2=image_lst[1], new_id=ans['id'] + 1, text=ans['wrong_message'])
        return render_template('answer_toresult.html', image1=ans['src'], image2=image_lst[1], text=ans['wrong_message'])
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
