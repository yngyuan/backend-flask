import datetime
from flask_restful import Resource, reqparse
from flask import render_template, make_response, request, redirect, session, jsonify
import logging
from urllib.error import HTTPError
from libs.strings import gettext
from models.theme_db_api import theme_db_api
from models.report_db_api import report_db_api
from models.user_db_api import user_db_api
from flask_jwt_extended import jwt_required
from bson.objectid import ObjectId
from resources.notification import send_notifications

theme_server = theme_db_api()
report_server = report_db_api()
user_server = user_db_api()
test_user_id = "5da733a794196bf0ff5f06db"
#
# _report_parser = reqparse.RequestParser()
# _report_parser.add_argument('user_id', type=str, required=True,
#                             help="this field cannot be left blank")
# _report_parser.add_argument('report_title', type=str, required=True,
#                             help="this field cannot be left blank")
# _report_parser.add_argument('report_image', type=str, required=True,
#                             help="this field cannot be left blank")
# _report_parser.add_argument('report_time', type=str, required=True,
#                             help="this field cannot be left blank")
# _report_parser.add_argument('report_theme', type=str, required=True,
#                             help="this field cannot be left blank")
# _report_parser.add_argument('report_location', type=str, required=True,
#                             help="this field cannot be left blank")
# _report_parser.add_argument('report_description', type=str, required=True,
#                             help="this field cannot be left blank")
# _report_parser.add_argument('report_tags', type=list, required=True,
#                             help="this field cannot be left blank")
#
# _theme_parse = reqparse.RequestParser()
# _theme_parse.add_argument('theme_name', type=str, required=True,
#                           help="this field cannot be left blank")
# _theme_parse.add_argument('theme_coverimage', type=str, required=True,
#                           help="this field cannot be left blank")
# _theme_parse.add_argument('theme_description', type=str, required=True,
#                           help="this field cannot be left blank")
# _theme_parse.add_argument('theme_image_list', type=list, required=True,
#                           help="this field cannot be left blank")
#
# _result_parser = reqparse.RequestParser()
# _result_parser.add_argument('ThemeName', type=str, required=True,
#                             help="this field cannot be left blank")
# _result_parser.add_argument('ReportTitle', type=str, required=True,
#                             help="this field cannot be left blank")
# _result_parser.add_argument('ReportDescription', type=str, required=True,
#                             help="this field cannot be left blank")
# _result_parser.add_argument('theme_image_list', type=list, required=True,
#                             help="this field cannot be left blank")
#import numpy as np
import re, json

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

class CreateReportMobile(Resource):

    def __init__(self):
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    def post(self):
        # u_id = session.get('u_id')

        try:
            # 18: 58:20, 284 - DEBUG - {"r_uid": "5dbefa7d35a29737ccffd80e", "uid": "5dbefa7d35a29737ccffd80e",
            #                           "r_title": "Ehbsbdvd", "r_location": "30.28665703505937,-97.73657687652326",
            #                           "r_tag_list": "Xbxhhdd", "r_tname": null, "r_description": "Shdvgsbs",
            #                           "r_img_url": "https://firebasestorage.googleapis.com/v0/b/aptphase3-74124.appspot.com/o/images%2F1574038697149.jpg?alt=media&token=400541d5-f6d0-42a3-a3c3-f8ce7e1f7cbc"}

            data = request.get_json()
            self.log.debug("receive create report request : ")
            self.log.debug(json.dumps(data));
            u_id = data["uid"]
            # self.log.debug("user id : " + u_id)
            report_url = data["r_img_url"]
            report_title = data["r_title"]
            # report_loc = np.array(re.findall(r"[\d.]+", data["r_location"])).astype(np.float)
            report_loc = data["r_location"]
            report_theme = data["r_tname"]
            report_describe = data["r_description"]
            report_tag_list = re.findall(r"[\w]+", data["r_tag_list"])

            try:
                # self.log.debug(str([u_id, report_title, report_url, report_theme, report_loc, report_describe, report_tag_list]))
                report_server.add_report(u_id, report_title,
                                      report_url, datetime.datetime.now(),
                                      report_theme, report_loc,
                                      report_describe, report_tag_list)
                self.log.debug("createMobile post successfully add into")
                #trigger notification here
                all_users = user_server.get_all_users()
                users_to_send_notification = []
                for user in all_users:
                    if user_server.is_subscribe(str(user['_id']), report_theme):
                        users_to_send_notification.append(user)
                user_name = user_server.get_user_by_uid(u_id)['u_username']
                message = user_name + " publish report with theme " + report_theme
                send_notifications(users_to_send_notification, message)


                return make_response(jsonify({"mes" : "success"}), 200)
            except Exception as err:
                self.log.debug("createMobiel post fail in following reason:")
                self.log.debug(str(err))
                return make_response(jsonify({"mes": "report para error: " + str(err)}), 200)

            # return make_response(render_template('result.html'))

        # except HTTPError:
        except Exception as e:
            self.log.debug("fail in adding report" + str(e))
            make_response(jsonify({"mes": "fail in adding report " + str(e)}), 200)

class CreateTheme(Resource):
    def __init__(self, imgur_handler):
        self.imgur_handler = imgur_handler

    def post(self):
        try:
            theme_name = request.form['ThemeName']
            # coverImage = request.form['CoverImage']
            theme_description = request.form['ThemeDescription']
            image = request.files['CoverImage']
            image_data = self.imgur_handler.send_image(image)
            cover_image = image_data["data"][
                "link"]
            theme_server.add_theme(theme_name, cover_image, theme_description)
            # result = request.form
            # return make_response(render_template('result.html'))
            return redirect("/manage.html")
        # except HTTPError:
        except Exception:
            return make_response(render_template("/CreateTheme.html",
                                                 failinfo="Fail to add new "
                                                          "theme"), 200)
