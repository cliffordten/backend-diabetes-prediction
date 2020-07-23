from db import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'users'  

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))
    region = db.Column(db.String(80))
    city = db.Column(db.String(80))
    password = db.Column(db.String(80))
    cpassword = db.Column(db.String(80))
    sex = db.Column(db.String(80))
    regDate = db.Column(db.String(80))
    accountType = db.Column(db.String(80))

    dob = db.Column(db.String(80))
    pob = db.Column(db.String(80))
    tel = db.Column(db.String(80))
    bloodgrp = db.Column(db.String(80))
    bloodpres = db.Column(db.String(80))
    weight = db.Column(db.String(80))
    height = db.Column(db.String(80))


    answers = db.relationship('AnswerModel', lazy='dynamic')
    askquestion = db.relationship('AskQuestionModel', lazy='dynamic')
    results = db.relationship('ResultModel', lazy='dynamic')

    def __init__(self, firstname, lastname, username, email, region, city, password, cpassword, sex, regDate, accountType, dob, pob, tel, bloodgrp, bloodpres, weight, height):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.region = region
        self.city = city
        self.password = password
        self.cpassword = cpassword
        self.sex = sex
        self.regDate = regDate
        self.accountType = accountType
        self.dob = dob
        self.pob = pob
        self.tel = tel
        self.bloodgrp = bloodgrp
        self.bloodpres = bloodpres
        self.weight = weight
        self.height = height

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def json(self):
        return {
        # 'id': self.id,
        'firstname': self.firstname.capitalize(),
        'lastname': self.lastname.capitalize(),
        'email': self.email,
        'tel': self.tel,
        "accountType": self.accountType
    }

    def jsonAnswer(self):
        return {
            "email": self.email,
            "answers": [answer.json() for answer in self.answers.all()],
            "accountType": self.accountType
        }

    def jsonAll(self):
        return {
        # 'id': self.id,
        'firstname': self.firstname.capitalize(),
        'lastname': self.lastname.capitalize(),
        'username': self.username,
        'email': self.email,
        'region': self.region,
        'city': self.city,
        'sex': self.sex,
        "regDate": self.regDate,
        "accountType": self.accountType,
        "password": self.password,
        "dob": self.dob,
        "pob": self.pob,
        "tel": self.tel,
        "bloodgrp": self.bloodgrp,
        "bloodpres": self.bloodpres,
        "weight": self.weight,
        "height": self.height
    }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def all_users(cls):
        return cls.query.all()

    @classmethod
    def paginate(cls, page):
        return cls.query.paginate(page=page, per_page=8)

    @classmethod
    def updateDetails(cls, feild, data):
        feild.firstname = data['firstname']
        feild.lastname = data['lastname']
        feild.username = data['username']
        feild.email = data['email']
        feild.region = data['region']
        feild.city = data['city']
        feild.sex = data['sex']
        feild.regDate = data['regDate'] 
        feild.accountType = data['accountType']
        feild.dob = data['dob']
        feild.pob = data['pob']
        feild.tel = data['tel']
        feild.bloodgrp = data['bloodgrp'] 
        feild.bloodpres = data['bloodpres']
        feild.weight = data['weight']
        feild.height = data['height']

