from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import app, db, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    quizzes = db.relationship('Quiz', backref="author", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    authorID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    questions = db.relationship("Question", backref="quiz", lazy=True)

    def __repr__(self):
        return f"Quiz('{self.id}', '{self.name}')"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # toDo fix this shit
    content = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    quizID = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)

    def __repr__(self):
        return f"Question('{self.id}', '{self.content}', '{self.answer}')"