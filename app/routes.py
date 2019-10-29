from app import app, db
import random
from flask import render_template, url_for, session, request, redirect, flash
from flask_login import current_user, login_user, logout_user
from app.models import User, Quiz, Question
from app.forms import RegisterForm, LoginForm

# test:development

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
    if request.method == "GET":
        return render_template("quiz.html", title="Frage", question = question)

    # if the user sumbits a question
    if request.method == "POST":
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

@app.route("/create", methods=["GET", "POST"])
def create_quiz():
    if request.method == "GET":
        return render_template("quiz_create.html", title="Quiz erstellen")
    
    if len(request.form) % 2 != 0:
        flash("Beim erstellen des Quiz ist ein fehler aufgetreten!")

    # !CHANGETHIS!
    quiz = Quiz(name="TEST", authorID=1)
    db.session.add(quiz)
    db.session.commit()

    # for x in request.form:
    #    print(x + ": ", end="")
    #    print(request.form[x])
    for question_number in range(int(len(request.form)/2)):
        content = request.form["question_content_" + str(question_number)]
        answer = request.form["question_answer_" + str(question_number)]
        q = Question(content=content, answer=answer, quizID=quiz.id)
        db.session.add(q)
    
    db.session.commit()

    flash("Quiz added!")
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Falscher Username oder falsches Passwort.")
            return redirect(url_for("login"))
        login_user(user)
        flash("Du wurdest erfolgreich eingeloggt.")
        return redirect(url_for("index"))
    return render_template("login.html", form = form, title="Login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Du bist bereits eingeloggt!")
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember_me.data)
        flash("Account erstellt!")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("Du wurdest erfolgreich ausgeloggt.")
    return redirect(url_for("index"))

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