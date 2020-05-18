from db import db


class ResponseModel(db.Model):
    __tablename__ = 'response'

    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String(80))
    date = db.Column(db.String(80))
    time = db.Column(db.String(80))
    name = db.Column(db.String(80))

    askquestion_id = db.Column(db.Integer, db.ForeignKey('askquestion.id'))

    askquestion = db.relationship('AskQuestionModel')

    def __init__(self, response, date, time, name, askquestion_id):
        self.response = response
        self.date = date
        self.time = time
        self.name = name
        self.askquestion_id = askquestion_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
        "response": self.response,
        "date": self.date,
        "time": self.time, 
        "name": self.name,
        "askquestion_id": self.askquestion_id,
    }

    @classmethod
    def find_all_by_qid(cls, askquestion_id):
        return cls.query.filter_by(askquestion_id= askquestion_id).all()