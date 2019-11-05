from app import app, db
import random
from flask import render_template, url_for, session, request, redirect, flash
from flask_login import current_user, login_user, logout_user
from app.models import User, Quiz, Question
from app.forms import RegisterForm, LoginForm, QuizForm, EditQuizForm

# test:development

@app.before_request
def before_request():
    if not session:
        restart()


@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", title="Willkommen!", questions_all = Quiz.query.all())

    if request.method == "POST":
        reset_session()
        return redirect(url_for("view_quiz", id=request.form["quiz"]))


@app.route("/user/<name>")
def view_user(name):
    user = User.query.filter_by(username=name).first()
    if user is None:
        flash("Dieser User wurde nicht gefunden!")
        return redirect(url_for("index"))
    return render_template("user.html", user=user, title=user.username)


@app.route("/quiz/<id>")
def view_quiz(id):
    quiz = Quiz.query.filter_by(id=id).first()
    if quiz is None:
        flash("Dieses Quiz wurde nicht gefunden!")
        return redirect(url_for("index"))
    return render_template("quiz_view.html", quiz=quiz, title=quiz.name)


@app.route("/quiz/<id>/play", methods=["GET", "POST"])
def play_quiz(id):
    quiz = Quiz.query.filter_by(id=id).first()
    if quiz is None:
        flash("Quiz wurde nicht gefunden!")
        return redirect(url_for("index"))

    if session["question_number"] >= len(quiz.questions):
        return render_template("quiz_end.html", title="Ende")

    current_question = quiz.questions[session["question_number"]]
    form = QuizForm()

    # if the user sumbits a question
    if form.validate_on_submit():
        user_answer = form.answer.data
        is_correct = False
        # If user answer is correct
        if current_question.answer.lower() == user_answer.lower().replace(",", ".").strip("0"):
            session["answers_right"] += 1
            is_correct=True

        session["question_number"] += 1
        session["answers_total"] += 1

        return render_template("quiz_next.html", correct=is_correct, title="Nächste Frage", question=current_question)
    return render_template("quiz_play.html", title="Frage", question=current_question,quiz=quiz, form=form)


@app.route("/quiz/<quizID>/edit")
def edit_quiz(quizID):
    if current_user.is_anonymous:
        return redirect(url_for("index"))
    quiz = Quiz.query.filter_by(id=quizID).first()
    if quiz is None:
        flash("Dieses Quiz wurde nicht gefunden")
        return redirect(url_for("index"))
    if quiz.author.id != current_user.id:
        return redirect(url_for("index"))

    return render_template("edit_quiz.html", title="Quiz bearbeiten", quiz=quiz)


# toDo: mobile optimization
@app.route("/question/<questionID>/edit", methods=["GET", "POST"])
def edit_quiz_question(questionID):
    if current_user.is_anonymous:
        return redirect(url_for("index"))
    question = Question.query.filter_by(id=questionID).first()
    if question is None:
        flash("Dieses Quiz wurde nicht gefunden")
        return redirect(url_for("index"))
    if question.quiz.author.id != current_user.id:
        return redirect(url_for("index"))
    form = EditQuizForm()

    if form.validate_on_submit():
        db.session.query(Question).filter_by(id=questionID). \
            update({"content": form.question.data, "answer": form.answer.data})
        db.session.commit()
        return render_template("edit_quiz.html", title="Quiz bearbeiten", quiz=question.quiz)
    form.question.data = question.content
    form.answer.data = question.answer
    return render_template("edit_quiz.html", title="Frage bearbeiten", quiz=question.quiz,
                           question_to_edit=question, form=form)


@app.route("/quiz/<quizID>/add-question")
def create_question(quizID):
    if current_user.is_anonymous:
        return redirect(url_for("index"))
    quiz = Quiz.query.filter_by(id=quizID).first()
    if quiz is None:
        flash("Dieses Quiz wurde nicht gefunden")
        return redirect(url_for("index"))
    if quiz.author.id != current_user.id:
        return redirect(url_for("index"))
    question = Question(content=" ", answer=" ", quizID=quiz.id)
    db.session.add(question)
    db.session.commit()
    return redirect(url_for("edit_quiz_question", questionID=question.id))


@app.route("/question/<questionID>/delete")
def delete_quiz_question(questionID):
    if current_user.is_anonymous:
        return redirect(url_for("index"))
    question = Question.query.filter_by(id=questionID).first()
    if question is None:
        flash("Frage nicht gefunden")
        return redirect(url_for("index"))
    if question.quiz.author.id != current_user.id:
        return redirect(url_for("index"))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("edit_quiz", quizID=question.quiz.id))

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
    session["question_number"] = 0
    session["answers_total"] = 0
    session["answers_right"] = 0