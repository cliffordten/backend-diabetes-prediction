from flask import request
from datetime import date, datetime
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from models.response import ResponseModel
from models.user import UserModel
from models.doctor import DocModel
from models.askquestion import AskQuestionModel
# extend_existing=True

class Response(Resource):
    @jwt_required
    def post(self, qid):
        data = request.get_json()
        data['date'] = str(date.today())
        data['time'] = str(datetime.now().time()).split(".")[0]
        user_id = get_jwt_identity()[0]
        user_email = get_jwt_identity()[1]

        question = AskQuestionModel.find_by_id(qid)
        data['askquestion_id'] = question.id

        user_e = UserModel.find_by_email(user_email)
        doc_e = DocModel.find_by_email(user_email)

        user = UserModel.find_by_id(user_id)
        doc = DocModel.find_by_id(user_id)

        if doc and doc_e:
            data['name'] = doc.firstname.capitalize() + " " + doc.lastname.capitalize()

        if user and user_e:
            data['name'] = user.firstname.capitalize() + " " + user.lastname.capitalize()

        

        response = ResponseModel(**data)
        response.save_to_db()

        return {"message": "Response is Sent to all Users.",
                "name": response.name}, 201

    @jwt_required
    def get(self, qid):

        responses = ResponseModel.find_all_by_qid(qid)

        if not responses:
            return {'message': 'No Results found'}, 200

        return [response.json() for response in responses]