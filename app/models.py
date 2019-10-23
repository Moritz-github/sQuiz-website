from app import app
from app import db

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    quizzes = db.relationship('Quiz', backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.userID}', '{self.username}')"

class Quiz(db.Model):
    quizID = db.Column(db.Integer, primary_key=True)
    quizname = db.Column(db.String(100), nullable=False)
    authorID = db.Column(db.Integer, db.ForeignKey("user.userID"), nullable=False)

    questions = db.relationship("Question", backref="quiz", lazy=True)

    def __repr__(self):
        return f"Quiz('{self.quizID}', '{self.quizname}')"

class Question(db.Model):
    questionID = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    quizID = db.Column(db.Integer, db.ForeignKey("quiz.quizID"), nullable=False)

    def __repr__(self):
        return f"Question('{self.questionID}', '{self.content}', '{self.answer}')"