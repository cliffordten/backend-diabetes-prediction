import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from resources.user import UserRegister, UserLogin, GetAllUsers, UserByEmail,UserByToken, UpdateUserDetails, UpdateUserPassword, GetAllDoctor, GetAllPatient
from resources.question import CreateQuestion, Question, GetAllQuestions
from resources.answer import Answer, GetUserAnswerById, GetTodayAnswer, GetAllAnswers
from resources.result import Result, GetTodayResult, GetAllResults
from resources.doctor import DocRegister
from resources.askquestion import AskQuestion
from resources.response import Response
from resources.admin import AdminRegister, CreateDoctors, GetAllHosDoctors
 
app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app) 

api.add_resource(UserRegister, '/api/v1/user/register')
api.add_resource(DocRegister, '/api/v1/doc/register')
api.add_resource(UpdateUserDetails, '/api/v1/user/details/update')
api.add_resource(UpdateUserPassword, '/api/v1/user/password/update')
api.add_resource(UserLogin, '/api/v1/login')
api.add_resource(GetAllUsers, '/api/v1/user/all')
api.add_resource(GetAllDoctor, '/api/v1/doc/all')
api.add_resource(GetAllPatient, '/api/v1/pat/all')
api.add_resource(UserByEmail, '/api/v1/user/<string:email>')
api.add_resource(UserByToken, '/api/v1/user/details')

api.add_resource(CreateQuestion, '/api/v1/new/question')
api.add_resource(Question, '/api/v1/question')
api.add_resource(GetUserAnswerById, '/api/v1/user/answer/<int:ind>')
api.add_resource(GetAllQuestions, '/api/v1/question/all')


api.add_resource(Answer, '/api/v1/user/answer')
api.add_resource(GetTodayAnswer, '/api/v1/user/answer/today')
api.add_resource(GetAllAnswers, '/api/v1/answer/all')

api.add_resource(Result, '/api/v1/user/result')
api.add_resource(GetTodayResult, '/api/v1/user/result/now')
api.add_resource(GetAllResults, '/api/v1/user/result/all')

api.add_resource(AskQuestion, '/api/v1/user/askquestion')
api.add_resource(Response, '/api/v1/user/response/<int:qid>')

api.add_resource(AdminRegister, '/api/v1/admin')
api.add_resource(CreateDoctors, '/api/v1/add/doctor')
api.add_resource(GetAllHosDoctors, '/api/v1/all/doctor')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True) 