from db import db
from datetime import datetime


class QuestionModel(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(80))
    info = db.Column(db.String(80))
    answer = db.Column(db.String(80))
    tag = db.Column(db.String(80))

    def __init__(self, question, info, answer, tag):
        self.question = question
        self.info = info
        self.answer = answer
        self.tag = tag

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
        # 'id': self.id,
        'question': self.question,
        'info': self.info,
        'answer': self.answer,
        'tag': self.tag
    }

    @classmethod
    def find(cls, question):
        return cls.query.filter_by(question= question).first()
    
    @classmethod
    def paginate(cls, page):
        return cls.query.paginate(page=page, per_page=1)

    @classmethod
    def all_questions(cls):
        return cls.query.all()
