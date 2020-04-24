from db import db
from datetime import datetime


class ResultModel(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(80))
    message = db.Column(db.String(80))
    sub_message = db.Column(db.String(80))
    date = db.Column(db.String(80))
    time = db.Column(db.String(80))

    doc_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'))

    users = db.relationship('UserModel')
    docs = db.relationship('DocModel')


    def __init__(self, classname, message, sub_message, date, time, user_id, doc_id, answer_id):
        self.classname = classname
        self.message = message
        self.sub_message = sub_message
        self.date = date
        self.time = time
        self.user_id = user_id
        self.doc_id = doc_id
        self.answer_id = answer_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
        "classname": self.classname,
        "message": self.message,
        "sub_message": self.sub_message,
        "date": self.date,
        "time": self.time 
    }

    def jsonAll(self, _id):
        return {
        "classname": self.classname,
        "message": self.message,
        "sub_message": self.sub_message,
        "date": self.date,
        "time": self.time, 
        "user_id": _id,
        "answer_id": self.answer_id
    }

    def jsonAll_pat(self):
        return {
        "classname": self.classname,
        "message": self.message,
        "sub_message": self.sub_message,
        "date": self.date,
        "time": self.time, 
        "user_id": self.user_id,
        "answer_id": self.answer_id
    }

    def jsonAll_doc(self):
        return {
        "classname": self.classname,
        "message": self.message,
        "sub_message": self.sub_message,
        "date": self.date,
        "time": self.time, 
        "doc_id": self.doc_id,
        "answer_id": self.answer_id
    }

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id= user_id).first()

    @classmethod
    def find_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id= user_id).all()

    @classmethod
    def find_all_by_doc_id(cls, user_id):
        return cls.query.filter_by(doc_id= user_id).all()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date= date).all()

    @classmethod
    def all_results(cls):
        return cls.query.all()

    @classmethod
    def all_results_user(cls):
        return cls.query.filter_by(user_id= cls.user_id).all()
    
    @classmethod
    def all_results_doc(cls):
        return cls.query.filter_by(doc_id= cls.doc_id).all()

    @classmethod
    def paginate(cls, page):
        return cls.query.paginate(page=page, per_page=5)
