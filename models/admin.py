from db import db


class AdminModel(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    username = db.Column(db.String(80))
    accountType = db.Column(db.String(80))

    hosDoctors = db.relationship('HosDoctorsModel', lazy='dynamic')


    def __init__(self, email, password, accountType, username):
        self.email = email
        self.password = password
        self.accountType = accountType
        self.username = username

    def json(self, doc, pat):
        return {
        # 'id': self.id,
        'firstname': "Hospital",
        'lastname': "Admin",
        'email': self.email,
        'doc': doc,
        'pat': pat,
        "accountType": self.accountType
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

