from db import db
from datetime import datetime


class AnswerModel(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    pregnancies = db.Column(db.Float)
    glucose = db.Column(db.Float)
    blood_pressure = db.Column(db.Float)
    skin_thickness = db.Column(db.Float)
    insulin = db.Column(db.Float)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    age = db.Column(db.Float)
    BMI = db.Column(db.Float)
    DPF = db.Column(db.Float)
    date = db.Column(db.String(80))
    time = db.Column(db.String(80))

    doc_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    result = db.relationship('ResultModel', backref='results', uselist=False)
    users = db.relationship('UserModel')
    docs = db.relationship('DocModel')


    def __init__(self, pregnancies, glucose, blood_pressure, skin_thickness, insulin, height, weight, age, BMI, DPF, date, time, user_id, doc_id):
        self.pregnancies = pregnancies
        self.glucose = glucose
        self.blood_pressure = blood_pressure
        self.skin_thickness = skin_thickness
        self.insulin = insulin
        self.height = height
        self.weight = weight
        self.age = age
        self.BMI = BMI
        self.DPF = DPF
        self.date = date
        self.time = time
        self.user_id = user_id
        self.doc_id = doc_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self, _id):
        return {
        "pregnancies": self.pregnancies,
        "glucose": self.glucose,
        "blood_Pressure": self.blood_pressure,
        "skin_thickness": self.skin_thickness,
        "insulin": self.insulin,
        "BMI": self.BMI,
        "DPF": self.DPF,
        "Age": self.age,
        "date": self.date, 
        "time": self.time, 
        "user_id": _id,
        "answer_id": self.id
    }

    def jsonAll(self, _id):
        return {
        "pregnancies": self.pregnancies,
        "glucose": self.glucose,
        "blood_Pressure": self.blood_pressure,
        "skin_thickness": self.skin_thickness,
        "insulin": self.insulin,
        "height": self.height,
        "weight": self.weight,
        "BMI": self.BMI,
        "DPF": self.DPF,
        "Age": self.age,
        "date": self.date, 
        "time": self.time, 
        "user_id": _id
    }

    def jsonAll_pat(self):
        return {
        "pregnancies": self.pregnancies,
        "glucose": self.glucose,
        "blood_Pressure": self.blood_pressure,
        "skin_thickness": self.skin_thickness,
        "insulin": self.insulin,
        "height": self.height,
        "weight": self.weight,
        "BMI": self.BMI,
        "DPF": self.DPF,
        "Age": self.age,
        "date": self.date, 
        "time": self.time, 
        "user_id": self.user_id
    }

    def jsonAll_doc(self):
        return {
        "pregnancies": self.pregnancies,
        "glucose": self.glucose,
        "blood_Pressure": self.blood_pressure,
        "skin_thickness": self.skin_thickness,
        "insulin": self.insulin,
        "height": self.height,
        "weight": self.weight,
        "BMI": self.BMI,
        "DPF": self.DPF,
        "Age": self.age,
        "date": self.date, 
        "time": self.time, 
        "doc_id": self.doc_id
    }

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id= user_id).first()

    @classmethod
    def find_by_doc_id(cls, doc_id):
        return cls.query.filter_by(doc_id= doc_id).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id= _id).first()

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
    def all_answers_user(cls):
        return cls.query.filter_by(user_id= cls.user_id).all()
    
    @classmethod
    def all_answers_doc(cls):
        return cls.query.filter_by(doc_id= cls.doc_id).all()
