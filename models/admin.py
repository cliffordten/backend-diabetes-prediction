from db import db


class AdminModel(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    docCode = db.Column(db.String(80))
    accountType = db.Column(db.String(80))

    def __init__(email, password, accountType):
        self.email = email
        self.password = password
        self.accountType = accountType
 
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # def create_doc(cls, docF)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_doctor(cls, code):
        return cls.query.filter_by(docCode=code).first()

    @classmethod
    def all_users(cls):
        return cls.query.all()