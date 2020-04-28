from flask_restful import Resource
from flask import render_template, make_response, request,jsonify
from models.report_db_api import report_db_api
from models.user_db_api import user_db_api
from datetime import datetime
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
user_db = user_db_api()
report_db = report_db_api()
class SearchMobile(Resource):
    def __init__(self):
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    # When receiving a post search request(form),
    # return the search result.
    def post(self):
        # report_obj = report_db_api()
        # user_obj = user_db_api()

        data = request.get_json()
        self.log.debug(str(data.keys()))
        keyword = data['keyword']
        field = data['field']
        self.log.debug("receive keyword :" + keyword + " field : " + field)

        # To see if the user wants to search by tag / location
        # or tag & location.
        if field == 'Tag':
            report_list = report_db.search_report_by_tag([keyword])
        elif field == 'Location':
            report_list = report_db.search_report_by_geo_location(
                keyword)
            self.log.debug("search by location, find " + str(len(report_list)) + " results")

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
                _username = user_db.get_user_by_uid(_report[
                                                              "r_uid"])[
                    "u_username"]
                report_list[_idx]["r_username"] = _username
            except TypeError:
                report_list[_idx]["r_username"] = "Anonymous"
        for i in range(len(report_list)):
            report_list[i]['_id'] = str(report_list[i]['_id'])
            report_list[i]['r_uid'] = str(report_list[i]['r_uid'])
            report_list[i]['r_tag_list'] = ','.join(report_list[i]['r_tag_list'])
        self.log.debug("return reports :" + str(len(report_list)))
        return make_response(jsonify({"lists":report_list}), 200)
