from db import db


class AskQuestionModel(db.Model):
    __tablename__ = 'askquestion'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    question = db.Column(db.String(80))
    tag = db.Column(db.String(80))
    date = db.Column(db.String(80))
    time = db.Column(db.String(80))

    doc_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship('UserModel')
    docs = db.relationship('DocModel')

    def __init__(self, title, question, tag, date, time, user_id, doc_id):
        self.title = title
        self.question = question
        self.tag = tag
        self.date = date
        self.time = time
        self.user_id = user_id
        self.doc_id = doc_id