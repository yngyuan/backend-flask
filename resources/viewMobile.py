# from flask_restful import Resource, reqparse
# from flask import request, render_template, make_response, session, redirect, jsonify
# from models.user_db_api import user_db_api
# from models.theme_db_api import theme_db_api
# from models.report_db_api import report_db_api
# from flask_jwt_extended import jwt_required
# from bson.objectid import ObjectId
# import logging
# theme_api = theme_db_api()
# user_api = user_db_api()
#
# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
#
# class ViewMobile(Resource):
#     def __init__(self):
#         self.log = logging
#         self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
#     def get(self):
#         # can obtain data if refreshing page
#         themes = list(theme_api.get_all_theme())
#         jsonstring = '['
#         for i in range(len(themes)):
#             themes[i]['_id'] = str(themes[i]['_id'])
#             themes[i]['t_name'] = str(themes[i]['t_name'])
#             themes[i]['t_coverimage'] = str(themes[i]['t_coverimage'])
#             themes[i]['t_description'] = str(themes[i]['t_description'])
#             jsonstring += '{'
#             jsonstring += '\'t_name\': \'' + themes[i]['t_name']+ '\', '
#             jsonstring += '\'t_coverimage\': \'' + themes[i]['t_coverimage'] + '\', '
#             jsonstring += '\'t_description\': \'' + themes[i]['t_description'] + '\', '
#             jsonstring = jsonstring + '}'
#             if i<len(themes)-1:
#                 jsonstring = jsonstring + ', '
#         jsonstring += ']'
#         # return make_response(jsonify({'lists':jsonstring}), 200)
#         return make_response(jsonify({'lists': themes}), 200)
#     def post(self):
#         data = request.get_json()
#         if data is not None:
#             subscribedTheme = user_api.get_subscribed_theme_by_id(ObjectId(data['uid']))
#         else:
#             subscribedTheme = list()
#         themes = list(theme_api.get_all_theme())
#         for i in range(len(themes)):
#             themes[i]['_id'] = str(themes[i]['_id'])
#             themes[i]['t_name'] = str(themes[i]['t_name'])
#             themes[i]['t_coverimage'] = str(themes[i]['t_coverimage'])
#             themes[i]['t_description'] = str(themes[i]['t_description'])
#
#         return make_response(jsonify({'lists': themes}), 200)
#
#
# class ViewOneMobile(Resource):
#     def __init__(self):
#         self.log = logging
#         self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
#     def get(self, t_name):
#         server1 = report_db_api()
#         report = list(server1.get_report_by_tname(r_tname=t_name))
#         return make_response(jsonify(report=report, length=len(report)), 200)
#
#     def post(self):
#         # u_id = session.get('u_id')
#         data = request.get_json()
#         u_id = data["uid"]
#         t_name= data["t_name"]
#         print(u_id)
#         if (u_id == None or not user_api.exists_uid(u_id)):
#             self.log.debug("user not exist : " + u_id)
#             return make_response(jsonify({"mes" : "missing curr user"}), 200)
#         else:
#             subscribe = data['subscribe']
#             if subscribe == "1":
#                 user_api.add_subscription(u_id, t_name=t_name)
#             else:
#                 user_api.drop_subscription(u_id, t_name=t_name)
#             server1 = report_db_api()
#             report = list(server1.get_report_by_tname(r_tname=t_name))
#             self.log.debug("subscribe " + str(subscribe))
#             return make_response(jsonify({"report" : report,
#                                          "length" : len(report),
#                                          "subscribe" : subscribe}), 200)

from flask_restful import Resource, reqparse
from flask import request, render_template, make_response, session, redirect, jsonify
from models.user_db_api import user_db_api
from models.theme_db_api import theme_db_api, ObjectId
from models.report_db_api import report_db_api
from flask_jwt_extended import jwt_required
from flask_restful.representations import json

theme_api = theme_db_api()
user_api = user_db_api()


class ViewMobile(Resource):

    def get(self):
        # can obtain data if refreshing page
        themes = list(theme_api.get_all_theme())
        for i in range(len(themes)):
            themes[i]['_id'] = str(themes[i]['_id'])
            themes[i]['t_name'] = str(themes[i]['t_name'])
            themes[i]['t_coverimage'] = str(themes[i]['t_coverimage'])
            themes[i]['t_description'] = str(themes[i]['t_description'])

        return make_response(jsonify({'lists': themes}), 200)

    def post(self):
        data = request.get_json()
        if data is not None:
            subscribedTheme = user_api.get_subscribed_theme_by_id(ObjectId(data['uid']))
        else:
            subscribedTheme = list()
        themes = list(theme_api.get_all_theme())
        for i in range(len(themes)):
            themes[i]['_id'] = str(themes[i]['_id'])
            themes[i]['t_name'] = str(themes[i]['t_name'])
            themes[i]['t_coverimage'] = str(themes[i]['t_coverimage'])
            themes[i]['t_description'] = str(themes[i]['t_description'])

        return make_response(jsonify({'lists': themes}), 200)


class ViewOneMobile(Resource):
    def get(self):
        # can obtain data if refreshing page
        themes = list(theme_api.get_all_theme())
        for i in range(len(themes)):
            themes[i]['_id'] = str(themes[i]['_id'])
            themes[i]['t_name'] = str(themes[i]['t_name'])
            themes[i]['t_coverimage'] = str(themes[i]['t_coverimage'])
            themes[i]['t_description'] = str(themes[i]['t_description'])

        return make_response(jsonify({'lists': themes}), 200)


    # receive a json ,with current uid, theme name to be subscribed: t_name
    def post(self):
        data = request.get_json()
        u_id = data['uid']
        # u_id = '5daf8d2f72eb94efe98bd904'
        if data is None:
            return make_response(jsonify({'message': "who are you"}),404)
        else:
            subscribe = data['subscribe_clicked']
            if subscribe == "1":
                user_api.add_subscription(u_id, t_name=data['t_name'])
            else:
                user_api.drop_subscription(u_id, t_name=data['t_name'])
            return make_response(jsonify({'subscribe_clicked': "1" }), 200)