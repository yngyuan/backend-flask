from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from libs.strings import gettext
from models.user_db_api import user_db_api
import logging
from flask import render_template, make_response, request, session, redirect, jsonify

user_api = user_db_api()
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
_logger = logging
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('user_email', type=str, required=False, help="this field cannot be left blank")
_user_parser.add_argument('user_password', type=str, required=True, help="this field cannot be left blank")
_user_parser.add_argument('user_name', type=str, required=True, help="this field cannot be left blank")
class UserMobile(Resource):

    def get(self, user_name):
        curr_user = user_api.get_user_by_username(user_name)
        if not curr_user:
            return {"message": gettext("user_not_found")}, 404

        return {'user_id' : str(curr_user['_id'])}, 200

    # @classmethod
    def delete(self, user_name):
        user = user_api.get_user_by_username(user_name)

        if not user:
            return {"message": gettext("user_not_found")}, 404
        # res = copy.deepcopy(user)
        # _logger.debug("tyep of user id %s" % str(type(user["_id"])))
        result = user_api.delete_user_by_id(user['_id'])

        return result, 200

class UserRegisterMobile(Resource):

    def __init__(self):
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    def post(self):
        # data = _user_parser.parse_args()
        data = request.get_json()
        # print(data)

        user_name = data['name'].strip()
        user_email = data['email'].strip()
        user_password = data['password'].strip()
        if (len(user_name) == 0 or len(user_email) == 0 or len(user_password) == 0):
            return make_response(jsonify({"mes": "Email or Name pr Password is empty"}), 200)

        inserted_id = user_api.add_user(user_email, user_name, user_password)
        self.log.debug("inserted_id is :" + str(inserted_id))
        if (inserted_id is None):
            # return {'message' : gettext("fail in adding user")}, 404
            return make_response(jsonify({"mes":"Email or Name already exists"}),200)

        else:
            user_id = str(user_api.get_user_by_email(user_email))
            session['u_id'] = user_id
            # return {'inserted_id': str(inserted_id)}, 200
            return make_response(jsonify({"uid": session['u_id'], "mes": "success"}), 200)

class UserLoginMoblie(Resource):
    def post(self):
        data = request.get_json()
        logging.debug("receive post request, processing , details: " + data["email"] + " " + data["password"])
        if (len(data["email"]) == 0 or len(data["password"]) == 0):
            return make_response(jsonify({"mes": "email and password can't be empty"}), 400)
        user = user_api.get_user_by_email(data['email'])

        # this is what the `authenticate()` function did in security.py
        if user is not None:

            if safe_str_cmp(user["u_password"], data['password']):
                # identity= is what the identity() function did in security.py—now stored in the JWT
                user_id = str(user["_id"])
                access_token = create_access_token(identity=user_id, fresh=True)
                refresh_token = create_refresh_token(user_id)

                session['u_id'] = user_id
                # return make_response(render_template('result.html', result=data), 200)
                # return redirect("/manage.html")
                logging.debug("sucess")
                return make_response(jsonify({"uid":user_id, "mes": "success"}), 200)

            else:
                # make_response(render_template("login.html",
                #                               error_message="password incorecct"), 200)
                logging.debug("password incorrect")
                return make_response(jsonify({"mes": "password incorrect"}), 200)

        # return {"message": "Invalid Credentials!"}, 401

        return make_response(jsonify({"mes" : "user does not exist"}), 200)