
from flask_restful import Resource
from flask import request, render_template, make_response, session, redirect, jsonify
from models.user_db_api import user_db_api
from models.report_db_api import report_db_api, ObjectId
from models.theme_db_api import theme_db_api
from flask_jwt_extended import jwt_required
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
report_api = report_db_api()
theme_api = theme_db_api()
user_api = report_api.user_db_api


class ManageMobile(Resource):

    def __init__(self):
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    def get(self):
        # reports = report_api.get_all_reports();
        reports = report_api.get_report_by_uid(ObjectId('5d8eda3ee1b75277bae9e187'))
        for i in range(len(reports)):
            reports[i]['_id'] = str(reports[i]['_id'])
            reports[i]['r_uid'] = str(reports[i]['r_uid'])
            reports[i]['r_time'] = str(reports[i]['r_time'])
            reports[i]['r_tag_list'] = str(reports[i]['r_tag_list'])

        # return {'title1': reports[0]['r_title'], 'title2': reports[1]['r_title'], 'size': str(len(reports))}, 200
        # return make_response(jsonify({'title1': reports[0]['r_title'], 'title2': reports[1]['r_title'], 'size': str(len(reports))}), 200)
        return make_response(jsonify({'lists': reports, 'title1': reports[0]['r_title']}), 200)

    def post(self):
        data = request.get_json()
        fake_uid = '5da733a794196bf0ff5f06db'
        themes = []
        if data is not None:
            reports = report_api.get_report_by_uid(ObjectId(data['uid']))
            user_logged = user_api.get_user_by_uid(ObjectId(data['uid']))
        else:
            reports = report_api.get_report_by_uid(ObjectId(fake_uid))
            user_logged = user_api.get_user_by_uid(fake_uid)
        # user_logged = user_api.get_user_by_uid('5da8f781452582db447fb59d')
        if user_logged is not None:
            for theme_name in user_logged['u_subscribed_themes']:
                theme = theme_api.get_theme_by_name(theme_name)
                theme['_id'] = str(theme['_id'])
                theme['t_image_list'] = str(theme['t_image_list'])
                themes.append(theme)

        for i in range(len(reports)):
            user_each = user_api.get_user_by_uid(u_id=reports[i]['r_uid'])
            if user_each is None:
                username = "None"
            else:
                username = user_each['u_username']
            reports[i]['_id'] = str(reports[i]['_id'])
            reports[i]['r_uid'] = str(reports[i]['r_uid'])
            reports[i]['r_time'] = str(reports[i]['r_time'])
            reports[i]['r_tag_list'] = str(reports[i]['r_tag_list'])
            reports[i]['r_username'] = username
        self.log.debug(str(len(themes)) + " themes " + str(len(reports)) + " reports")
        return make_response(jsonify({'themes': themes, 'lists': reports, 'length': len(reports)}), 200)