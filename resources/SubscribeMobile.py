from flask_restful import Resource, reqparse
from flask_restful.representations import json
from jinja2.nodes import Pair
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from libs.strings import gettext
from models.user_db_api import user_db_api
from models.theme_db_api import theme_db_api
from models.report_db_api import report_db_api, ObjectId
import logging
from flask import render_template, make_response, request, session, redirect, jsonify

report_api = report_db_api()
theme_api = theme_db_api()
user_api = user_db_api()

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# test_uid = "5d8eda3ee1b75277bae9e187"


def arrayOf(param, param1):
    pass


class SubscribeMobile(Resource):
    def __init__(self):
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    def get(self):
        u_id = session.get()
        subscribedTheme = user_api.get_subscribed_theme_by_id(u_id)
        # test_uid = '5daf8d2f72eb94efe98bd904'
        # subscribedTheme = user_api.get_subscribed_theme_by_id(test_uid)
        reports = []
        for theme in subscribedTheme:
            # item = {"themeName": theme}
            newReports = list(report_api.get_report_by_tname(r_tname=theme))
            reports.extend(newReports)

        for i in range(len(reports)):
            user = user_api.get_user_by_uid(u_id=reports[i]['r_uid'])

            if user is None:
                username = "None"
            else:
                username = user['u_username']

            if 'r_title' in reports[i].keys():
                pass
            else:
                reports[i]['r_title'] = "None"

            if 'r_like_list' in reports[i].keys():
                pass
            else:
                reports[i]['r_like_list'] = []

            reports[i]['_id'] = str(reports[i]['_id'])
            reports[i]['r_uid'] = str(reports[i]['r_uid'])
            reports[i]['r_time'] = str(reports[i]['r_time'])
            reports[i]['r_tag_list'] = str(reports[i]['r_tag_list'])
            reports[i]['r_tag_list'] = reports[i]['r_tag_list'].replace('\'' ,'')
            reports[i]['r_tag_list'] = reports[i]['r_tag_list'].strip('[]')
            # print(reports[i]['r_tag_list'])
            reports[i]['r_username'] = username

            reports[i]['r_username'] = str(reports[i]['r_username'])
            reports[i]['r_like_list'] = reports[i]['r_like_list']
            reports[i]['r_like_num'] = str(len(reports[i]['r_like_list']))

        return make_response(jsonify({'lists': reports}), 200)



    def post(self):
        data = request.get_json()

        user_id = data['uid']
        # self.log.debug("post request in subscribe, uid %s" % user_id)
        test_uid = '5dbefa7d35a29737ccffd80e'

        if data is not None:
            subscribedTheme = user_api.get_subscribed_theme_by_id(user_id)
        else:
            subscribedTheme = user_api.get_subscribed_theme_by_id(test_uid)

        reports = []
        for theme in subscribedTheme:
            # item = {"themeName": theme}
            newReports = list(report_api.get_report_by_tname(r_tname=theme))
            reports.extend(newReports)

        for i in range(len(reports)):
            user = user_api.get_user_by_uid(u_id=reports[i]['r_uid'])
            # check wether username in dict
            if user is None:
                username = "None"
            else:
                username = user['u_username']

            if 'r_like_list' in reports[i].keys():
                pass
            else:
                reports[i]['r_like_list'] = []

            # check whether r_title in the dict
            if 'r_title' in reports[i].keys():
                pass
            else:
                reports[i]['r_title'] = "None"



            reports[i]['_id'] = str(reports[i]['_id'])
            reports[i]['r_uid'] = str(reports[i]['r_uid'])
            reports[i]['r_time'] = str(reports[i]['r_time'])
            reports[i]['r_tag_list'] = str(reports[i]['r_tag_list'])
            reports[i]['r_tag_list'] = reports[i]['r_tag_list'].replace('\'', '')
            reports[i]['r_tag_list'] = reports[i]['r_tag_list'].strip('[]')

            reports[i]['r_username'] = username

            reports[i]['r_username'] = str(reports[i]['r_username'])
            reports[i]['r_like_list'] = reports[i]['r_like_list']
            reports[i]['r_like_num'] = str(len(reports[i]['r_like_list'])) + " likes"
            #like = data['like_clicked'][i]
            #if like == "1":
            #    report_api.add_like(user_id, str(reports[i]['_id']))
            #else:
            #    report_api.drop_like(user_id, str(reports[i]['_id']))


        self.log.debug("get %s reports" % len(reports))



        return make_response(jsonify({'lists': reports}), 200)


class SubscribeOneMobile(Resource):
    def post(self):
        data = request.get_json()
        user_id = data['uid']
        test_uid = '5daf8d2f72eb94efe98bd904'

        if data is None:
            return make_response(jsonify({'message': "who are you"}), 404)
        else:
            like = data['like_clicked']
            if like is True:
                report_api.add_like(user_id, str(data['r_id']))
            else:
                report_api.drop_like(user_id, str(data['r_id']))
            return make_response(jsonify({'like_clicked': 'true'}), 200)
