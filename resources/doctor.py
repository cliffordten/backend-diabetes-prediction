from flask import request
from datetime import date
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token

from models.user import UserModel
from models.hosdoctors import HosDoctorsModel
from models.doctor import DocModel
import time

class DocRegister(Resource):

    def post(self):
        data = request.get_json()
        data['username'] = ((data['firstname']).replace(" ", '')).lower() + ((data['lastname']).replace(" ", '')).lower()
        data['accountType'] = 'doc'
        data['regDate'] = str(date.today())

        data['dob'] = 'None'
        data['pob'] = 'None'
        data['region'] = 'None'
        data['city'] = 'None'
        data['bloodgrp'] = 'None'
        data['bloodpres'] = 'None'
        data['weight'] = 'None'
        data['height'] = 'None'

        if not HosDoctorsModel.find_doc_by_code(data['adminCode']):
            return { "message": "Invalid Code From Admin \n Please contact hospital admin to add you as doctor"}, 400

        if DocModel.find_by_email(data['email']):
            return {"message": "Doctor already exists"}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": "A Patient already use this email"}, 400

        doc = DocModel(**data)
        doc.save_to_db()

        access_token = create_access_token(identity=[doc.id, doc.email], fresh=False)

        return {"message": "User created successfully.",
                "accountType": doc.accountType,
                'username': doc.username,
                "access_token": access_token
                }, 201


class Doctor(Resource):
    @classmethod
    def get(cls, user_id):
        user = DocModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = DocModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}

        
