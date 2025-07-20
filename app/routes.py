from flask import Blueprint, render_template, request, redirect, url_for, session
# from .data.questions import QUESTIONS
import json
import random

main = Blueprint('main', __name__)
quiz_started = False

# questions_path = r".\\data\\teamcenter-all-questions.json"
# questions_path = r".\\data\\devops-quiz.json"
questions_path = r".\\data\\devopspi_quiz_s1_fixed_50-50.json"

with open(questions_path, 'r', encoding='utf8') as file:
        QUESTIONS_ORIGINAL = json.load(file)

def shuffle_questions(questions_path, original_questions):
    for level in original_questions:
        for category_dict in original_questions[level]:
            for category, questions in category_dict.items():
                random.shuffle(questions)

    # Stocker le résultat dans une variable
    QUESTIONS = original_questions
    return QUESTIONS

QUESTIONS = shuffle_questions(questions_path, QUESTIONS_ORIGINAL)
# QUESTIONS = QUESTIONS_ORIGINAL

# Liste des thèmes disponibles
THEMES = list(QUESTIONS.keys())

def get_questions(theme):
    """Retourne toutes les questions associées à un thème donné."""
    questions = []
    if theme in QUESTIONS:
        # Parcourir chaque catégorie et accumuler les questions
        for category in QUESTIONS[theme]:
            for question_list in category.values():
                questions.extend(question_list)  # Ajouter les questions du niveau 3
    # Mélanger les questions et les stocker dans la session
    # random.shuffle(questions)
    return questions


@main.route('/')
def index():
    return render_template('index.html', themes=THEMES)


@main.route('/quiz', methods=['POST'])
def start_quiz():
    selected_theme = request.form.get('theme')
    if selected_theme not in THEMES:
        return redirect(url_for('main.index'))  # Redirige si le thème est invalide

    # Initialiser la session pour le quiz
    session['score'] = 0
    session['current_question'] = 0  # Position de la question courante
    session['selected_theme'] = selected_theme  # Garder le thème pour les résultats
    
    # questions = get_questions(selected_theme)
    session['questions'] = 'test'

    session['wrong_answers'] = []
    quiz_started = True
    return redirect(url_for('main.quiz', theme=selected_theme, question_index=0))


@main.route('/quiz/<theme>/<int:question_index>', methods=['GET', 'POST'])
def quiz(theme, question_index):
    questions = get_questions(theme)
    test = session.get('questions')
    total_questions = len(questions)


    # Si question_index est trop grand (fin du quiz), rediriger vers les résultats
    if question_index >= len(questions):
        return redirect(url_for('main.result', theme=theme))

    question = questions[question_index]

    user_answer = None
    is_correct = None
    
    if request.method == 'POST':
        # Récupérer la réponse de l'utilisateur
        # user_answer = request.form.getlist('answer')
        user_answer = request.form.get('answer')

        # Comparer la réponse de l'utilisateur avec la bonne réponse
        correct = question['correct']
        # if len(correct)>1:
        # is_correct = set(user_answer) == set(correct)
        is_correct = user_answer == correct
        # else:
        #     is_correct = ??

        # Initialiser les mauvaises réponses dans la session si non existantes
        if 'wrong_answers' not in session:
            session['wrong_answers'] = []

        # Si la réponse est correcte, augmenter le score
        if is_correct:
            session['score'] += 1
        else:
            # Stocker les mauvaises réponses sous forme de dictionnaire avec contexte
            session['wrong_answers'].append({
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': correct
            })
            session.modified = True  # Assurer la mise à jour

        print("Après modification - wrong_answers :", session.get('wrong_answers'))
        
    score = session.get('score', 0)
    if question_index==0:
        success_rate=0
    else:
        success_rate = round(100*score/(question_index), 2)

    return render_template(
        'quiz.html', 
        theme=theme, 
        question=question, 
        question_index=question_index,
        user_answer=user_answer,
        is_correct=is_correct,
        questions=questions,
        total_questions=total_questions,
        score=score,
        success_rate=success_rate
    )


@main.route('/quiz/<theme>/result', methods=['GET'])
def result(theme):
    # questions = QUESTIONS.get(theme, [])
    questions = get_questions(theme)
    score = session.get('score', 0)
    total_questions = len(questions)  # Calculer le nombre total de questions
    success_rate = round(100*score/(total_questions), 1)
    correct_answers = []

    wrong_answers = session.get('wrong_answers',[])
    print("Données dans session['wrong_answers'] :", wrong_answers)  # Ajout de log

    # Pour chaque question, on affiche la bonne réponse
    for question in questions:
        correct_answers.append({
            'question': question['question'],
            'correct_answer': question['correct']
        })

    return render_template(
        'result.html',
        score=score,
        correct_answers=correct_answers,
        questions=questions,
        total_questions=total_questions,
        theme=theme,
        success_rate=success_rate,
        wrong_answers=wrong_answers)
