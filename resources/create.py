import datetime
from flask_restful import Resource, reqparse
from flask import render_template, make_response, request, redirect, session
from urllib.error import HTTPError
from libs.strings import gettext
from models.theme_db_api import theme_db_api
from models.report_db_api import report_db_api
from flask_jwt_extended import jwt_required

theme_server = theme_db_api()
report_server = report_db_api()
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


class CreateReport(Resource):
    def __init__(self, imgur_handler):
        self.imgur_handler = imgur_handler

    # @jwt_required
    def get(self):
        u_id = session.get('u_id')
        if u_id is None:
            print(u_id)
            return redirect("/login.html")
        else:
            theme_list = theme_server.get_all_theme_name()
            return make_response(
                render_template("CreateReport.html", theme_list=theme_list), 200)

    def post(self):
        u_id = session.get('u_id')
        try:
            reportTheme = request.form['ThemeName']
            reportTitle = request.form['ReportTitle']
            reportDescription = request.form['ReportDescription']
            #reportTags = request.form['ReportTags']
            reportTags_list = []
            reportTags_list.append(request.form['BookName'])
            reportTags_list.append(request.form['Author'])
            reportTags_list.append(request.form['BookProperty'])
            print(reportTags_list)
            image = request.files['ReportImage']
            image_data = self.imgur_handler.send_image(image)
            reportImage = image_data["data"][
                "link"]  # "http://imgur.com/SbBGk.jpg"

            reportLocation = request.form['ReportLocation']
            #reportTags_list = [x.strip() for x in reportTags.split(',')]
            # insert the report information to the database(report_db)
            report_server.add_report(u_id, reportTitle,
                                      reportImage, datetime.datetime.now(),
                                      reportTheme, reportLocation,
                                      reportDescription, reportTags_list)
            # return make_response(render_template('result.html'))
            return redirect("/view.html")
        # except HTTPError:
        except Exception:
            return make_response(render_template("/CreateReport.html",
                                                 failinfo="Fail to add new "
                                                          "report"), 200)

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

    def get(self):
        u_id = session.get('u_id')
        if u_id is None:
            print(u_id)
            return redirect("/login.html")
        else:
            return make_response(render_template("CreateTheme.html"), 200)
    #
    # def post(self):
    #     data = theme_server.parse_args()
    #     # print(data)
    #     theme_name = data['theme_name']
    #     theme_coverimage = data['theme_coverimage']
    #     theme_description = data['theme_description']
    #     theme_image_list = data['theme_image_list']
    #
    #     inserted_id = theme_server.add_theme(theme_name, theme_coverimage,
    #                                          theme_description,
    #                                          theme_image_list)
    #     if inserted_id is None:
    #         return {'message': gettext("fail in adding theme")}, 404
    #     else:
    #         return {'inserted_id': str(inserted_id)}, 200


# class ReportResult(Resource):
#
#     # @app.route('/createReport/result', methods=['GET', 'POST'])
#     def post(self):
#
#         reportTheme = request.form['ThemeName']
#         reportTitle = request.form['ReportTitle']
#         reportDescription = request.form['ReportDescription']
#         reportTags = request.form['ReportTags']
#         #reportImage = request.form['ReportImage']
#
#         image = request.files['ReportImage']
#         image_data = imgur_handler.send_image(image)
#         reportImage = image_data["data"]["link"]  # "http://imgur.com/SbBGk.jpg"
#
#         reportLocation = request.form['ReportLocation']
#         reportTags_list = [x.strip() for x in reportTags.split(',')]
#         # insert the report information to the database(report_db)
#         report.add_report("5d8eda3ee1b75277bae9e187", reportTitle, reportImage, datetime.datetime.now(),
#                               reportTheme, reportLocation,
#                               reportDescription, reportTags_list)
#         return make_response(render_template('result.html', result=request.form), 200)

# class ReportAddThemeResult(Resource):
#     def __init__(self, imgur_handler):
#         self.imgur_handler = imgur_handler
#
#     def post(self):
#         if request.method == 'POST':
#             theme_name = request.form['ThemeName']
#             # coverImage = request.form['CoverImage']
#             theme_description = request.form['ThemeDescription']
#             image = request.files['CoverImage']
#             image_data = self.imgur_handler.send_image(image)
#             cover_image = image_data["data"][
#                 "link"]
#             theme_server.add_theme(theme_name, cover_image, theme_description)
#         result = request.form
#         return render_template('result.html', result=result)
