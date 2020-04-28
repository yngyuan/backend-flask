from flask_restful import Resource
from flask import request, render_template, make_response, session, redirect
from models.user_db_api import user_db_api
from models.report_db_api import report_db_api, ObjectId
from models.theme_db_api import theme_db_api
from models.user_db_api import user_db_api
from flask_jwt_extended import jwt_required
import logging
report_api = report_db_api()
theme_api = theme_db_api()
# user_api = report_api.user_db_api
user_api = user_db_api()
rindex = 0

user = {}
themes = []
report = []
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

def find_report(u_id):
    user = user_api.get_user_by_uid(ObjectId(u_id))
    report = []
    if user is not None:
        global themes
        themes = []
        for theme in user['u_subscribed_themes']:
            themes.append(theme_api.get_theme_by_name(theme))
        report = report_api.get_report_by_uid(user['_id'])
    return report
class Management(Resource):
    def __init__(self):
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    def get(self):
        u_id = session.get('u_id')
        #u_id = '5de4a94280db94ba80b2916d' # temporary fake id for testing
        # u_id = request.cookies.get('u_id')
        if u_id is None:
            print(u_id)
            return redirect("/login.html")
        else:
            self.log.debug("management login in as " + u_id)
            global user, themes, report, rindex
            report = find_report(u_id)
            session["rindex"] = rindex
            if len(report) == 0:
                return make_response(render_template('manage.html', report=report, length=len(report), themes=themes), 200)
            rindex = 0
            return make_response(render_template('manage.html', report=report[rindex], length=len(report), themes=themes), 200)

class Managedecr(Resource):

    def get(self):

        # global rindex
        rindex = session.get("rindex")
        u_id  = session.get('u_id')
        #u_id = '5de4a94280db94ba80b2916d' # temporary fake id for testing
        report = find_report(u_id)
        if len(report) == 0:
            return make_response(render_template('manage.html', report=report, length=len(report), themes=themes), 200)

        if rindex == 0:
            rindex = len(report) - 1
        else:
            rindex = rindex - 1

        session['rindex'] = rindex
        return make_response(render_template('manage.html', report=report[rindex], length=len(report), themes=themes), 200)
    
class Manageincr(Resource):

    def get(self):
        rindex = session.get("rindex")
        u_id  = session.get('u_id')
        #u_id = '5de4a94280db94ba80b2916d' # temporary fake id for testing
        report = find_report(u_id)
        if len(report) == 0:
            return make_response(render_template('manage.html', report=report, length=len(report), themes=themes), 200)

        if rindex == len(report) - 1:
            rindex = 0
        else:
            rindex = rindex + 1
        session['rindex'] = rindex
        return make_response(render_template('manage.html', report=report[rindex], length=len(report), themes=themes), 200)

class Managedele(Resource):

    def get(self, index):
        rindex = session.get("rindex")
        u_id = session.get('u_id')
        #u_id = '5de4a94280db94ba80b2916d' # temporary fake id for testing
        report = find_report(u_id)

        report_api.delete_report_by_id(report[rindex]['_id'])
        report = find_report(u_id)

        if len(report) == 0:
            return make_response(render_template('manage.html', report=report, length=len(report), themes=themes), 200)

        rindex = 0
        session['rindex'] = rindex

        return make_response(render_template('manage.html', report=report[rindex], length=len(report), themes=themes), 200)
                    
    def post(self, index):
        rindex = session.get("rindex")
        u_id = session.get('u_id')
        #u_id = '5de4a94280db94ba80b2916d' # temporary fake id for testing
        report = find_report(u_id)
        report_api.delete_report_by_id(report[rindex]['_id'])

        report = find_report(u_id)

        if len(report) == 0:
            return make_response(render_template('manage.html', report=report, length=len(report), themes=themes), 200)

        rindex = 0
        session['rindex'] = rindex

        return make_response(render_template('manage.html', report=report[rindex], length=len(report), themes=themes), 200)

