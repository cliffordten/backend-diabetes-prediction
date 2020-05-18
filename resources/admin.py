from flask import request
from datetime import date
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from models.admin import AdminModel
from models.hosdoctors import HosDoctorsModel


class AdminRegister(Resource):
    def post(self):
        data = request.get_json()

        if AdminModel.find_by_email(data['email']):
            return {"message": "Admin already exists"}, 400

        admin = AdminModel(**data)
        admin.save_to_db()

        return {"message": "created Admin"}

class CreateDoctors(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()

        data["docCode"] = HosDoctorsModel.create_doc()

        if HosDoctorsModel.find_by_email(data["email"]):
            return {"message": "Doctor already exists"}, 400

        while True:
            if not HosDoctorsModel.find_doc_by_code(data['docCode']):
                break
            data["docCode"] = HosDoctorsModel.create_doc()


        newDoc = HosDoctorsModel(**data)
        newDoc.save_to_db()

        return {"message": "Doctor Added",
                "doctor": newDoc.json()}


class GetAllHosDoctors(Resource):
    @jwt_required
    def get(self):

        return [x.json() for x in HosDoctorsModel.find_all()]