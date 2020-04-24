from flask import request
from datetime import date
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from models.question import QuestionModel

class CreateQuestion(Resource):
    
    def post(self):
        data = request.get_json()

        if QuestionModel.find(data['question']):
            return {"message": "Question already exists"}, 400

        question = QuestionModel(**data)
        question.save_to_db()

        return {"message": "Question created successfully"}


class Question(Resource):
    @jwt_required
    def get(self):
        page = request.args.get("page", 1, type=int)
        questions = QuestionModel.paginate(page)
        question = [x.json() for x in questions.items]
        
        return{
            # 'id': self.id,
            'question': question[0],
            'pagination':{
                "current": questions.page,
                "total": questions.total,
                "next": questions.next_num,
                "prev": questions.prev_num
            }
        }

class GetAllQuestions(Resource):
    @classmethod
    def get(cls):
        questions = [x.json() for x in QuestionModel.all_questions()]

        return {"questions":questions}