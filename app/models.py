from app import app
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    quizzes = db.relationship('Quiz', backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"

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