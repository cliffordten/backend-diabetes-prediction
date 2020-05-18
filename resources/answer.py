from flask import request
from datetime import date, datetime
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from models.answer import AnswerModel
from prediction.predictor import Predictor
from models.result import ResultModel
from models.user import UserModel
from models.doctor import DocModel


class Answer(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        IBM = data['weight'] / ((data["height"]) ** 2)
        data['BMI'] = round(IBM, 2)
        data['date'] = str(date.today())
        data['time'] = str(datetime.now().time())
        user_id = get_jwt_identity()[0]
        user_email = get_jwt_identity()[1]

        user_e = UserModel.find_by_email(user_email)
        doc_e = DocModel.find_by_email(user_email)

        user = UserModel.find_by_id(user_id)
        doc = DocModel.find_by_id(user_id)
        _id = ''

        if doc and doc_e:
            data['doc_id'] = user_id
            data['user_id'] = None
            _id = "doc_" + str(user_id)


        if user and user_e:
            data['user_id'] = user_id
            data['doc_id'] = None
            _id = "pat_" + str(user_id)
        

        answer = AnswerModel(**data)
        answer.save_to_db()

        print(data['pregnancies'],data['glucose'],data['blood_pressure'],data['skin_thickness'],data['insulin'],data['BMI'],data['DPF'],data['age'])

        predictor = Predictor(data['pregnancies'],data['glucose'],data['blood_pressure'],data['skin_thickness'],data['insulin'],data['BMI'],data['DPF'],data['age'])

        value = predictor.predict()
        status = predictor.save_to_file(value)

        if value == 0:
            className = "none"
            message = "You don't have diabetes"
            sub_message = "Congratulation, Continue leaving a healthy life sytle"
            result = ResultModel(className, message, sub_message, data['date'], data['time'], data['user_id'], data['doc_id'], answer.id)
            result.save_to_db()
        elif value == 1:
            className = "error"
            message = "You have diabetes"
            sub_message = "Don't Pannic, Contact your doctor as soon as possible"
            result = ResultModel(className, message, sub_message, data['date'], data['time'], data['user_id'], data['doc_id'], answer.id)
            result.save_to_db()
        else:
            return {"message": "something went wrong"}, 500
            
        print(data['BMI'])
        

        return {"message": "Answer created successfully.",
                "id": answer.id,
                'user_id': _id
                }, 201
                
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()[0]
        user_email = get_jwt_identity()[1]

        user_e = UserModel.find_by_email(user_email)
        doc_e = DocModel.find_by_email(user_email)

        answers_user = AnswerModel.find_all_by_user_id(user_id)
        answers_doc = AnswerModel.find_all_by_doc_id(user_id)
        _id =''
        
        if answers_user and user_e:
            _id = "pat_" + str(user_id)
            return {"answers": [x.json(_id) for x in answers_user]}
        
        if answers_doc and doc_e:
            _id = "doc_" + str(user_id)
            return {"answers": [x.json(_id) for x in answers_doc]}

        if not answers_doc and not answers_user:
            return {'message': 'Answers not found'}, 404


class GetTodayAnswer(Resource):
     @jwt_required
     def get(self):
        user_id = get_jwt_identity()[0]

        _id =''

        user = UserModel.find_by_id(user_id)
        doc = DocModel.find_by_id(user_id)

        if user:
            _id = "pat_" + str(user_id)
        
        if doc:
            _id = "doc_" + str(user_id)

        answers = [x.json(_id) for x in AnswerModel.find_by_date(str(date.today()))]
        todayAnswers = []

        # return answers
        for answer in answers:

            x_id = answer['user_id'].split("_")[1]
            if(user_id == int(x_id)):
                todayAnswers.append(answer)
        
        if todayAnswers:
            return todayAnswers[-1]
            
        return {"message": "Take a test and see your result"}, 401


class GetAllAnswers(Resource):
    @classmethod
    def get(cls):

        answers_user = [x.jsonAll_pat() for x in AnswerModel.all_answers_user()]
        answers_doc = [x.jsonAll_doc() for x in AnswerModel.all_answers_doc()]

        return {
            "patients":answers_user,
            "doctors": answers_doc
            }
        
class GetUserAnswerById(Resource):
    @jwt_required
    def get(self, ind):
        user_id = get_jwt_identity()[0]
        user_email = get_jwt_identity()[1]

        user_e = UserModel.find_by_email(user_email)
        doc_e = DocModel.find_by_email(user_email)

        answers_user = AnswerModel.find_all_by_user_id(user_id)
        answers_doc = AnswerModel.find_all_by_doc_id(user_id)
        _id =''
        
        if answers_user and user_e:
            answer = AnswerModel.find_by_id(ind)
            for answer_user in answers_user:
                if ind == answer_user.id: 
                    return {"answers": answer_user.json(user_id)}
            return {'message': 'Answers not found'}, 404

        if answers_doc and doc_e:
            answer = AnswerModel.find_by_id(ind)
            for answer_doc in answers_doc:
                if ind == answer_doc.id: 
                    return {"answers": answer_doc.json(user_id)}
            return {'message': 'Answers not found'}, 404

        if not answers_doc and not answers_user:
            return {'message': 'No Details found'}, 404 