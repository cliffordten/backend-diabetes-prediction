from flask import request
from datetime import date, datetime
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from models.askquestion import AskQuestionModel
from models.user import UserModel
from models.doctor import DocModel


class AskQuestion(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        data['date'] = str(date.today())
        data['time'] = str(datetime.now().time()).split(".")[0]
        user_id = get_jwt_identity()[0]
        user_email = get_jwt_identity()[1]

        user_e = UserModel.find_by_email(user_email)
        doc_e = DocModel.find_by_email(user_email)

        user = UserModel.find_by_id(user_id)
        doc = DocModel.find_by_id(user_id)

        if doc and doc_e:
            data['doc_id'] = user_id
            data['user_id'] = None
            data["name"] = doc.firstname.upper() + " " + doc.lastname.upper()


        if user and user_e:
            data['user_id'] = user_id
            data['doc_id'] = None
            data['name'] = user.firstname.upper() + " " + user.lastname.upper()
        

        question = AskQuestionModel(**data)
        question.save_to_db()

        return {"message": "Question Sent to all Users.",
                "id": question.id,
                "name": data['name']}, 201


    @jwt_required
    def get(self):

        questions = AskQuestionModel.find_all()

        if not questions:
            return {'message': 'No Questions found'}, 404

        return [question.json() for question in questions]