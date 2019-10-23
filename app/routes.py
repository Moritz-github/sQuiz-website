from app import app
import random
from flask import render_template, url_for, session, request, redirect, flash
from app.questions.question_pools import question_pools


@app.before_request
def before_request():
    if not session:
        restart()


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["question_pool"] = request.form["question_pool"]

    if "question_pool" in session:
        return render_template("index_start.html", title="Los gehts!")

    return render_template("index_pickpool.html", title="Willkommen!", question_pool = question_pools.keys())


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    # checks if the user tried to go onto the quiz page, even though he did not select a question pool
    if "question_pool" not in session:
        flash("Bitte wähle zuerst einen Fragenkatalog aus")
        return redirect(url_for("index"))

    current_question = session["question_number"]

    # If quiz is loaded as a POST, that means the user submits a question
    if (request.method == "POST" and "question" in session):
        session["question_number"] = current_question + 1
        session["answers_total"] = session["answers_total"]+1
        user_answer = request.form["user_answer"]
        title = ""
        # If user answer is correct
        if session["answer"].lower().strip("0") == user_answer.lower().replace(",", ".").strip("0"):
            session["answers_right"] = session["answers_right"]+1
            is_correct=True
            title="Richtig"
        else:
            is_correct=False
            title="Falsch"

        print("JETZT wird question entfernt & quiz_next.html weitergegeben")
        session.pop("question")

        return render_template("quiz_next.html", correct=is_correct, title=title)
    
    # If no answer is sent, ask one
    if "question" not in session:
        session["question"], session["answer"] = question_pools[session["question_pool"]].get_question()
    return render_template("quiz.html", title="Frage " + str(session["question_number"]))


@app.route("/restart")
def restart():
    session.clear()
    session["question_number"] = 1
    session["answers_total"] = 0
    session["answers_right"] = 0
    flash("Eine neue Session wurde gestartet!")
    return redirect(url_for("index"))