from flask import request
from datetime import date
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from models.result import ResultModel
from models.user import UserModel
from models.doctor import DocModel


class Result(Resource):

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()[0]
        user_email = get_jwt_identity()[1]

        user_e = UserModel.find_by_email(user_email)
        doc_e = DocModel.find_by_email(user_email)

        results_user = ResultModel.find_all_by_user_id(user_id)
        results_doc = ResultModel.find_all_by_doc_id(user_id)

        _id =''

        if results_user and user_e:
            _id = "pat_" + str(user_id)
            return {"results": [x.jsonAll(_id) for x in results_user]}
        
        if results_doc and doc_e:
            _id = "doc_" + str(user_id)
            return {"results": [x.jsonAll(_id) for x in results_doc]}

        if not results_doc or not results_user:
            return {'message': 'No test taken yet'}, 404



class GetTodayResult(Resource):
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
        
        results = [x.jsonAll(_id) for x in ResultModel.find_by_date(str(date.today()))]
        todayResults = []

        # return results
        for result in results:

            x_id = result['user_id'].split("_")[1]
            if(user_id == int(x_id)):
                todayResults.append(result)
        
        if todayResults:
            return todayResults[-1]
            
        return {"help": "Take a test and see your result"}, 200


class GetAllResults(Resource):
    @classmethod
    def get(cls):
        
        results_user = [x.jsonAll_pat() for x in ResultModel.all_results_user()]
        results_doc = [x.jsonAll_doc() for x in ResultModel.all_results_doc()]

        return {
            "patients":results_user,
            "doctors": results_doc
            }
        
