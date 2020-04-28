from flask_restful import Resource
from flask import render_template, make_response, request
from models.report_db_api import report_db_api
from models.user_db_api import user_db_api
from datetime import datetime


class Search(Resource):
    def __init__(self, userdb, reportdb):
        self.user_db = userdb
        self.report_db = reportdb

    # Return the original page for search
    def get(self):
        return make_response(render_template("search.html",
                             keyword="Search keyword"),
                             200)

    # When receiving a post search request(form),
    # return the search result.
    def post(self):
        # report_obj = report_db_api()
        # user_obj = user_db_api()
        if request.method == 'POST':
            keyword = request.form['keyword']
            field = request.form['field']

            # To see if the user wants to search by tag / location
            # or tag & location.
            if field == 'Tag':
                report_list = self.report_db.search_report_by_tag([keyword])
            elif field == 'Location':
                report_list = self.report_db.search_report_by_location(
                    keyword)

            # If the user wants to search by tag and location,
            # we need to remove duplicated reports.
            elif field == "All fields":
                report_list_temp = self.report_db.search_report_by_tag([
                    keyword])
                report_list_temp += \
                    self.report_db.search_report_by_location(
                    keyword)
                # Remove duplicated reports.
                # Yeah... it's a duplicated process
                _repo = []
                report_list = []
                for _report in report_list_temp:
                    if _report["_id"] not in _repo:
                        report_list.append(_report)
                        _repo.append(_report["_id"])

            # Tell the user nickname for each report.
            for _idx, _report in enumerate(report_list):
                try:
                    r_title = report_list[_idx]["r_title"]
                    if not r_title:
                        report_list[_idx]["r_title"] = "My Report"
                except:
                    report_list[_idx]["r_title"] = "My Report"
                # Convert datetime to date
                try:
                    report_list[_idx]["r_time"] = report_list[_idx]["r_time"]. \
                        date()
                # if date is not set
                except:
                    report_list[_idx]["r_time"] = datetime.now().date()

                try:
                    _username = self.user_db.get_user_by_uid(_report[
                                                                  "r_uid"])[
                        "u_username"]
                    report_list[_idx]["r_username"] = _username
                except TypeError:
                    report_list[_idx]["r_username"] = "Anonymous"

            return make_response(render_template("search.html",
                                                 reports=report_list,
                                                 keyword=keyword,
                                                 field=field), 200)
