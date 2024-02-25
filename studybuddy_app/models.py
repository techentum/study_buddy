from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

import json

from . import app

db = SQLAlchemy(app)

# Association table for user answered questions
answered_questions = db.Table('answered_questions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Backref to 'answered_questions' association table
    answered_questions = db.relationship('Question', secondary=answered_questions, lazy='subquery',
                                         backref=db.backref('users', lazy=True))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    
    # Relationship to questions
    questions = db.relationship('Question', backref='category', lazy=True)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    # Store answer choices as a JSON string; each choice can be a key in a dict
    answer_choices = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)  # E.g., 'Easy', 'Medium', 'Hard'
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    @property
    def choices(self):
        """Return answer choices as a Python dict."""
        return json.loads(self.answer_choices)

    @choices.setter
    def choices(self, choices_dict):
        """Set answer choices from a dict."""
        self.answer_choices = json.dumps(choices_dict)
        

