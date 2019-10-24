from app import app, db
import random
from flask import render_template, url_for, session, request, redirect, flash
from app.models import User, Quiz, Question


@app.before_request
def before_request():
    if not session:
        restart()


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index_pickquiz.html", title="Willkommen!", questions_all = Quiz.query.all())

    if request.method == "POST":
        reset_session()
        return redirect(url_for("quiz", id=request.form["quiz"]))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    quiz_id = request.args.get("id")
    if not quiz_id:
        flash("Quiz wurde nicht gefunden!")
        return redirect(url_for("index"))

    all_questions = Question.query.filter_by(quizID=quiz_id).all()
    if session["question_number"] >= len(all_questions):
        return render_template("quiz_end.html", title="Ende")
    question = all_questions[session["question_number"]]
    # if the user loads the page he should be shown the question
    if(request.method == "GET"):
        return render_template("quiz.html", title="Frage", question = question)

    # if the user sumbits a question
    if (request.method == "POST"):
        user_answer = request.form["user_answer"]
        title = ""
        # If user answer is correct
        if question.answer.lower() == user_answer.lower().replace(",", ".").strip("0"):
            session["answers_right"] += 1
            is_correct=True
            title="Richtig"
        else:
            is_correct=False
            title="Falsch"

        print("JETZT wird question entfernt & quiz_next.html weitergegeben")

        session["question_number"] += 1
        session["answers_total"] += 1

        return render_template("quiz_next.html", correct=is_correct, title=title, question=question)


@app.route("/restart")
def restart():
    reset_session()
    flash("Eine neue Session wurde gestartet!")
    return redirect(url_for("index"))

def reset_session():
    session.clear()
    session["question_number"] = 0
    session["answers_total"] = 0
    session["answers_right"] = 0