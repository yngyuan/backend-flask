from flask_restful import Resource, reqparse
from flask import request, render_template, make_response
from libs.strings import gettext
from models.user_db_api import user_db_api
from models.theme_db_api import theme_db_api
from models.report_db_api import report_db_api

theme_api = theme_db_api()
from libs import JSONEncoder


class ViewMain(Resource):

    def get(self):
        # can obtain data if refreshing page
        theme = list(theme_api.get_all_theme())
        if len(theme) == 0:
            # when theme list is empty; 'length' is needed in html
            return make_response(render_template('view.html', theme=theme, length=len(theme)), 200)

        return make_response(render_template(
                'view.html', theme=theme, length=len(theme)
            ), 200)
    # def get(self, t_name):
    #     curr_theme = theme_api.get_theme_by_name(t_name)
    #     if not curr_theme:
    #         return {"message": gettext("theme_not_found")}, 404
    #
    #     return {'theme name': str(curr_theme['t_name'])}, 200

class ViewOne(Resource):
    def get(self, t_name):
        server1 = report_db_api()
        report = list(server1.get_report_by_tname(r_tname=t_name))
        return make_response(render_template(
            "view_one.html", report=report, length=len(report)
        ), 200)