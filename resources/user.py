from flask import request
from datetime import date
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from models.admin import AdminModel
from models.doctor import DocModel
from models.user import UserModel
import time

        # this.toastr.error(err.error.message)


class UserRegister(Resource):

    def post(self):
        data = request.get_json()
        data['username'] = ((data['firstname']).replace(" ", '')).lower() + ((data['lastname']).replace(" ", '')).lower()
        data['regDate'] = str(date.today())
        data['accountType'] = 'user'
        data['dob'] = 'None'
        data['pob'] = 'None'
        data['tel'] = 'None'
        data['bloodgrp'] = 'None'
        data['bloodpres'] = 'None'
        data['weight'] = 'None'
        data['height'] = 'None'

        if UserModel.find_by_email(data['email']):
            return {"message": "User already exists"}, 400

        if DocModel.find_by_email(data['email']):
            return {"message": "A Doctor already use this email"}, 400

        user = UserModel(**data)
        user.save_to_db()

        access_token = create_access_token(identity=[user.id, user.email], fresh=False)


        return {"message": "User created successfully.",
                "accountType": user.accountType,
                'username': user.username,
                "access_token": access_token
                }, 201


class UserByEmail(Resource):
    @classmethod
    def get(cls, email):
        user = UserModel.find_by_email(email)
        doc = DocModel.find_by_email(email)
        if not user and not doc:
            return {'message': 'User not found'}, 404

        if doc :
            return doc.jsonAll()

        return user.jsonAll()

    @classmethod
    def delete(cls, email):
        user = UserModel.find_by_email(email)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}


class UserByToken(Resource):
     @jwt_required
     def get(self):
        user_id = get_jwt_identity()[0]
        user_email = get_jwt_identity()[1]

        user_e = UserModel.find_by_email(user_email)
        doc_e = DocModel.find_by_email(user_email)

        user = UserModel.find_by_id(user_id)
        doc = DocModel.find_by_id(user_id)
        if not user and not doc:
           return {'message': 'User not found'}, 404

        if doc and doc_e :
            return doc.jsonAll()

        return user.jsonAll()
        

class UserLogin(Resource):
    @classmethod
    def post(cls):
        #get data from parser
        data = request.get_json()

        #find user in database
        user = UserModel.find_by_email(data['email'])
        doc = DocModel.find_by_email(data['email'])
        admin = AdminModel.find_by_email(data['email'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=[user.id, user.email], fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "accountType": user.accountType,
                'username': user.username,
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        if doc and safe_str_cmp(doc.password, data['password']):
            access_token = create_access_token(identity=[doc.id, doc.email], fresh=True)
            refresh_token = create_refresh_token([doc.id, doc.email])
            return {
                "accountType": doc.accountType,
                'username': doc.username,
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        if admin and safe_str_cmp(admin.password, data['password']):
            access_token = create_access_token(identity=[admin.id, admin.email], fresh=True)
            refresh_token = create_refresh_token([admin.id, admin.email])
            return {
                "accountType": admin.accountType,
                'username': admin.username,
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        return {'message': 'Invalid credentials'}, 401 


class GetAllUsers(Resource):
    @classmethod
    def get(cls):
        users = [x.json() for x in UserModel.all_users()]
        doctors = [x.json() for x in DocModel.all_doctors()]

        return {
            "users":users,
            "doctors": doctors
            }
        
class UpdateUserDetails(Resource):
    @jwt_required
    def put(self):
        data = request.get_json()

        user_id = get_jwt_identity()[0]
        user_email = get_jwt_identity()[1]

        user_e = UserModel.find_by_email(user_email)
        doc_e = DocModel.find_by_email(user_email)

        user = UserModel.find_by_id(user_id)
        doc = DocModel.find_by_id(user_id)

        if user and user_e:
            UserModel.updateDetails(user, data)
            user.save_to_db()
            return {"message": "User Details Updated"}

        if doc and doc_e:
            DocModel.updateDetails(doc, data)
            doc.save_to_db()
            return {"message": "User Details Updated"}


        return {"message": "User Does not Exist"}, 404


class UpdateUserPassword(Resource):
    @jwt_required
    def put(self):
        data = request.get_json()

        user_id = get_jwt_identity()[0]
        user_email = get_jwt_identity()[1]

        user_e = UserModel.find_by_email(user_email)
        doc_e = DocModel.find_by_email(user_email)

        user = UserModel.find_by_id(user_id)
        doc = DocModel.find_by_id(user_id)

        if user and user_e:
            if user.password != data['oldPassword']:
                return {'message': 'Old Password Incorrect'}, 401

            user.password = data['newPassword']
            user.cpassword = data['newPassword']

            user.save_to_db()
            return {"message": "User Password Udated"}

        if doc and doc_e:
            if doc.password != data['oldPassword']:
                return {'message': 'Old Password Incorrect'}, 401

            doc.password = data['newPassword']
            doc.cpassword = data['newPassword']

            doc.save_to_db()
            return {"message": "User Password Udated"}


        return {"message: An error occured during update"}, 500


class GetAllPatient(Resource):
    @jwt_required
    def get(self):
        users = [x.json() for x in UserModel.all_users()]

        page = request.args.get("page", 0, type=int)

        if page > 0 :
            users = UserModel.paginate(page)
            user = [x.json() for x in users.items]
            
            return{
                # 'id': self.id,
                'patients': user,
                'pagination':{
                    "current": users.page,
                    "total": users.total,
                    "next": users.next_num,
                    "prev": users.prev_num
                }
            }

        return {"patients":users}

class GetAllDoctor(Resource):
    @jwt_required
    def get(self):
        doctors = [x.json() for x in DocModel.all_doctors()]

        page = request.args.get("page", 0, type=int)

        if page > 0 :
            doctors = DocModel.paginate(page)
            doc = [x.json() for x in doctors.items]
            
            return{
                # 'id': self.id,
                'doctors': doc,
                'pagination':{
                    "current": doctors.page,
                    "total": doctors.total,
                    "next": doctors.next_num,
                    "prev": doctors.prev_num
                }
            }

        return {"doctors":doctors}