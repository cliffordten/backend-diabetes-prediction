from db import db
import random
import string


class HosDoctorsModel(db.Model):
    __tablename__ = 'hosdoctors'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    name = db.Column(db.String(80))
    docCode = db.Column(db.String(80))
    tel = db.Column(db.String(80))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))


    admin = db.relationship('AdminModel')


    def __init__(self, email, name, tel, docCode):
        self.email = email
        self.name = name
        self.tel = tel
        self.docCode = docCode

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
        "name": self.name,
        "email": self.email,
        "tel": self.tel,
        "docCode": self.docCode,
        "id": self.id
    }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_doc_by_code(cls, code):
        return cls.query.filter_by(docCode=code).first()

    @classmethod
    def create_doc(cls):
        return  ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    @classmethod
    def find_all(cls):
        return cls.query.all()