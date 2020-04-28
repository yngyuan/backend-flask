from pymongo import MongoClient
import logging
import datetime
import time
import re
from bson.objectid import ObjectId
from models.user_db_api import user_db_api
from db import db

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


class report_db_api(object):
    """
    A class contains all interfaces to manipulate report data in Mongodb
    TODO:
    Attributes
    ----

    Methods
    ----

    """

    def __init__(self):
        """
        Init and connect to db.
        """
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
        # client = MongoClient(
        #     "mongodb+srv://zed:yy9826@cluster0-uaytj.mongodb.net/" \
        #     "test?retryWrites=true&w=majority")
        # db = client.apt
        self.collection = db.report
        self.user_db_api = user_db_api()

        server_status_result = db.command("serverStatus")
        self.log.debug(server_status_result)

    def add_report(self, r_uid, r_title, r_url, r_time, r_tname, r_location="Mars",
                   r_description="None", r_tag_list=[], r_like_list=[]):
        """
        Add a new report to the report collection.
        :param r_uid: Report id
        :type r_uid: str or ObjectID
        :param r_title: Report title
        :type r_title: str
        :param r_url: Url of the report's image. At present, the number of
        image is 1 per report
        :type r_url: str
        :param r_time: Time that the report is created
        :type r_time: datetime.datetime
        :param r_tname: Theme name of the report
        :type r_tname: str
        :param r_location: Location tagged on this report. Default is "Mars"
        :type r_location: str
        :param r_description: Description of this report. Default is "None"
        :type r_description: str
        :param r_tag_list: List of tags(str) of this report
        :type r_tag_list: list[str]
        :return: _id of the inserted report in the "report" collection
        :rtype: ObjectId
        :param r_like_list: List of liked user id(str) of this report
        :type r_like_list: list[ObjectId]
        """
        self.log.debug("adding report")
        assert type(r_uid) == str or type(r_uid) == ObjectId
        if type(r_uid) == str:
            r_uid = ObjectId(r_uid)
        assert type(r_title) == str
        # assert self.user_db_api.exists_uid(r_uid)
        assert type(r_url) == str
        # TODO: r_url should fit some kind of regex...
        assert type(r_time) == datetime.datetime
        # I don't think we need to check whether a theme exist here,
        # since it is not a value that can be edited by users.
        assert type(r_tname) == str
        assert type(r_location) == str
        assert type(r_description) == str
        assert isinstance(r_tag_list, list)
        for _tag in r_tag_list:
            assert type(_tag) == str
        for _like in r_like_list:
            assert type(_like) == str

        one_report = {"r_uid": r_uid,
                      "r_title": r_title,
                      "r_url": r_url,
                      "r_time": r_time,
                      "r_tname": r_tname,
                      "r_location": r_location,
                      "r_description": r_description,
                      "r_tag_list": r_tag_list,
                      "r_like_list": r_like_list}
        result = self.collection.insert_one(one_report)
        self.log.debug("New report inserted. New report id: %s"
                       % result.inserted_id)
        return result.inserted_id

    def get_report_by_rid(self, r_id):
        """
        Get a report by report id(r_id).
        :param r_id: The _id of the report you want to get
        :type r_id: ObjectId
        :return: result of the get method
        :rtype: dict
        """

        assert type(r_id) == ObjectId
        result = self.collection.find_one({"_id": r_id})
        if result:
            self.log.debug("Get report %s." % r_id)
        else:
            self.log.warn("Get report %s failed. " % r_id)
        return result

    def get_report_by_uid(self, u_id):
        """
        Get a report by user id(u_id).
        :param u_id: The _id of the report you want to get
        :type u_id: ObjectId
        :return: result of the get method
        :rtype: list[dict]
        """

        assert type(u_id) == ObjectId
        result = list(self.collection.find({"r_uid": u_id}).sort("r_time", -1))
        if result:
            self.log.debug("Get %d report(s) from user %s."
                           % (len(result), str(u_id)))
        else:
            self.log.warning("Get report from user:%s failed. "
                             % str(u_id))
        return result

    def get_all_reports(self):
        """
        Get all reports.
        :return: result of the get method
        :rtype: list[dict]
        """
        result = list(self.collection.find().sort("r_time", -1))
        if result:
            self.log.debug("Get %d report(s)."
                           % len(result))
        else:
            self.log.warning("Get all reports failed. ")
        return result

    def fast_get_report_by_rid(self, r_id):
        """
        TODO
        :param r_id: The _id of the report you want to get
        :type r_id: str
        :return: result of the get method
        :rtype: dict
        """

        assert type(r_id) == ObjectId

        result = self.collection.find_one({"_id": r_id})
        self.log.debug("Get report %s" % r_id)
        return result

    def search_report_by_tag(self, r_tag_list=[]):
        """
        Search report by the given tag list.
        If the tag list of the report and the target tag list have at least
        one same tag, then recall this report.
        :param r_tag_list: Target tags
        :type r_tag_list: list[str]
        :return: target reports
        :rtype: list[dict]
        """
        assert isinstance(r_tag_list, list)
        for _tag in r_tag_list:
            assert type(_tag) == str

        report_list = []
        for _report in self.collection.find().sort("r_time", -1):
            if set(_report["r_tag_list"]) & set(r_tag_list):
                self.log.debug("Find report with tag(s) \"%s\": _id:%s"
                               % (str(set(r_tag_list)), _report["_id"]))
                report_list.append(_report)

        if report_list:
            self.log.debug("Find %d report(s) with tag(s) \"%s\"."
                           % (len(report_list), str(set(r_tag_list))))
        else:
            self.log.warning("Unable to find report with tag(s) \"%s\"."
                             % str(set(r_tag_list)))

        return report_list

    def search_report_by_location(self, r_location="Mars"):
        """
        Recall reports that have the same location as the target location
        :param r_location: Target location
        :type r_location: str
        :return: target reports
        :rtype: list[dict]
        """
        assert type(r_location) == str

        report_list = []
        for _report in self.collection.find().sort("r_time", -1):
            if _report["r_location"] == r_location:
                report_list.append(_report)
                self.log.debug("Find report with r_location \"%s\": _id:%s"
                               % (r_location, _report["_id"]))
        if report_list:
            self.log.debug("Find %d report(s) with location \"%s\"."
                           % (len(report_list), r_location))
        else:
            self.log.warning("Unable to find report with location \"%s\"."
                             % r_location)
        return report_list

    def search_report_by_geo_location(self, r_location="0,0"):
        """
        Recall reports that have the same location as the target location
        :param r_location: Target location, "latitude,longitude"
        :type r_location: str
        :return: target reports
        :rtype: list[dict]
        """
        assert type(r_location) == str
        report_list = []

        option = 1# 0 is exact found, 1 is coarse found
        latitude_precison = 0.5
        longitude_precison = 0.5

        # location_pair = re.findall("[\w]+", r_location)
        location_pair = r_location.split(',')
        self.log.debug(str(location_pair))
        if len(location_pair) == 2:
            location_pair[0] = round(float(location_pair[0]), 2)
            location_pair[1] = round(float(location_pair[1]), 2)
        else:
            return report_list

        for _report in self.collection.find().sort("r_time", -1):
            # result_pair = re.findall("[\w]+", _report["r_location"])
            result_pair =re.findall("[-\w.]+", _report["r_location"])
            if (len(result_pair) == 2):
                self.log.debug("result_pair " + result_pair[0] + " " + result_pair[1] + " origin : " + _report["r_location"])
                result_pair[0] = round(float(result_pair[0]), 2)
                result_pair[1] = round(float(result_pair[1]), 2)
            else:
                continue

            if option == 0 and \
                    location_pair[0] == result_pair[0] and location_pair[1] == result_pair[1] or\
                option == 1 and \
                    -latitude_precison <= location_pair[0] - result_pair[0] <= latitude_precison and \
                    -longitude_precison <= location_pair[1] - result_pair[1] <= longitude_precison:
                report_list.append(_report)
                self.log.debug("Find report with r_location \"%s\": _id:%s"
                               % (r_location, _report["_id"]))

        if report_list:
            self.log.debug("Find %d report(s) with location \"%s\"."
                           % (len(report_list), r_location))
        else:
            self.log.warning("Unable to find report with location \"%s\"."
                             % r_location)
        return report_list

    def delete_report_by_id(self, r_id):
        """
        Delete one report according to report id(r_id)
        :param r_id: Id of the report you wish to delete
        :type r_id: ObjectId
        """
        assert type(r_id) == ObjectId

        result = self.collection.delete_one({"_id": r_id})
        if result.deleted_count:
            self.log.debug("Report deleted. ID: %s" % r_id)
        else:
            self.log.warning("Report deletion failed: %s" % result.raw_result)

    def get_report_by_tname(self, r_tname):
        # result = self.collection.find({"r_tname": r_tname}).sort("r_time", -1)
        # self.log.debug("Get all reports under r_tname %s" % r_tname)
        # return result

        # assert type(r_tname) == str

        report_list = []
        for _report in self.collection.find().sort("r_time", -1):
            if _report["r_tname"] == r_tname:
                report_list.append(_report)
                self.log.debug("Get all reports under r_tname %s" % r_tname)
        return report_list

    def get_like_list(self, r_id):
        return self.get_report_by_rid(ObjectId(r_id))['r_like_list']

    def add_like(self, u_id, r_id):
        if u_id in self.get_like_list(r_id):
            self.log.info("Already liked")
        else:
            myquery = {"_id": ObjectId(r_id)}
            newvalues = {"$push": {"r_like_list": u_id}}
            self.collection.update_one(myquery, newvalues)
            self.log.info("User %s liked %s" % (u_id, r_id))
            return {"message": "User %s liked %s" % (u_id, r_id)}

    def drop_like(self, u_id, r_id):
        if u_id in self.get_like_list(r_id):
            myquery = {"_id": ObjectId(r_id)}
            newvalues = {"$pull": {"r_like_list": u_id}}
            self.collection.update_one(myquery, newvalues)
            self.log.info("User %s unliked %s" % (u_id, r_id))
            return {"message": "User %s unliked %s" % (u_id, r_id)}

        else:
            self.log.info("Never liked")



# Below is the test part.
if __name__ == "__main__":
    print("Test1: init a report_db_api object and connect to db.")
    report = report_db_api()
    test_id = ObjectId("5da733a794196bf0ff5f06db")
    print(report.get_report_by_uid(u_id=test_id))
    print(report.get_all_reports())
    now = datetime.datetime.now()
    time.sleep(1)
    print("Test2: add a new report with user id(u_id), target url and time. ")
    # test_id = report.add_report("5da733a794196bf0ff5f06db", "url", now, "Portrait")
    # test_id1 = report.add_report("5da733a794196bf0ff5f06db", "url", now, "Portrait")
    # test_id2 = report.add_report("5da733a794196bf0ff5f06db", "url", now, "Portrait")
    # test_id3 = report.add_report("5da733a794196bf0ff5f06db", "url", now, "Portrait")
    # time.sleep(1)
    print("Test3: get a detailed report by report id(r_id). ")
    # print("Detailed report: ", report.get_report_by_rid(test_id))
    # time.sleep(1)
    print("Test4: get a detailed report by location of the report. ")
    print("Detailed report: ", report.search_report_by_location("Mars"))
    # time.sleep(1)
    # print("Test5: delete a report by id. ")
    # report.delete_report_by_id(test_id)
    # time.sleep(1)
    # print("Test6: delete a report which is not exist in the db. ")
    # report.delete_report_by_id(test_id)
    cursor = report.get_report_by_tname('Portrait')
    for document in cursor:
        print(document)

# from pymongo import MongoClient
# import logging
# import datetime
# import time
# from bson.objectid import ObjectId
# from models.user_db_api import user_db_api
# from db import db
# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
#
#
# class report_db_api(object):
#     """
#     A class contains all interfaces to manipulate report data in Mongodb
#     TODO:
#     Attributes
#     ----
#
#     Methods
#     ----
#
#     """
#     def __init__(self):
#         """
#         Init and connect to db.
#         """
#         self.log = logging
#         self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
#         # client = MongoClient(
#         #     "mongodb+srv://zed:yy9826@cluster0-uaytj.mongodb.net/" \
#         #     "test?retryWrites=true&w=majority")
#         # db = client.apt
#         self.collection = db.report
#         self.user_db_api = user_db_api()
#
#         server_status_result = db.command("serverStatus")
#         self.log.debug(server_status_result)
#
#     def add_report(self, r_uid, r_title, r_url, r_time, r_tname, r_location="Mars",
#                    r_description="None", r_tag_list=[]):
#         """
#         Add a new report to the report collection.
#         :param r_uid: Report id
#         :type r_uid: str or ObjectID
#         :param r_title: Report title
#         :type r_title: str
#         :param r_url: Url of the report's image. At present, the number of
#         image is 1 per report
#         :type r_url: str
#         :param r_time: Time that the report is created
#         :type r_time: datetime.datetime
#         :param r_tname: Theme name of the report
#         :type r_tname: str
#         :param r_location: Location tagged on this report. Default is "Mars"
#         :type r_location: str
#         :param r_description: Description of this report. Default is "None"
#         :type r_description: str
#         :param r_tag_list: List of tags(str) of this report
#         :type r_tag_list: list[str]
#         :return: _id of the inserted report in the "report" collection
#         :rtype: ObjectId
#         """
#
#         assert type(r_uid) == str or type(r_uid) == ObjectId
#         if type(r_uid) == str:
#             r_uid = ObjectId(r_uid)
#         assert type(r_title) == str
#         # assert self.user_db_api.exists_uid(r_uid)
#         assert type(r_url) == str
#         # TODO: r_url should fit some kind of regex...
#         assert type(r_time) == datetime.datetime
#         # I don't think we need to check whether a theme exist here,
#         # since it is not a value that can be edited by users.
#         assert type(r_tname) == str
#         assert type(r_location) == str
#         assert type(r_description) == str
#         assert isinstance(r_tag_list, list)
#         for _tag in r_tag_list:
#             assert type(_tag) == str
#
#         one_report = {"r_uid": r_uid,
#                       "r_title": r_title,
#                       "r_url": r_url,
#                       "r_time": r_time,
#                       "r_tname": r_tname,
#                       "r_location": r_location,
#                       "r_description": r_description,
#                       "r_tag_list": r_tag_list}
#         result = self.collection.insert_one(one_report)
#         self.log.debug("New report inserted. New report id: %s"
#                        % result.inserted_id)
#         return result.inserted_id
#
#     def get_report_by_rid(self, r_id):
#         """
#         Get a report by report id(r_id).
#         :param r_id: The _id of the report you want to get
#         :type r_id: ObjectId
#         :return: result of the get method
#         :rtype: dict
#         """
#
#         assert type(r_id) == ObjectId
#         result = self.collection.find_one({"_id": r_id})
#         if result:
#             self.log.debug("Get report %s." % r_id)
#         else:
#             self.log.warn("Get report %s failed. " % r_id)
#         return result
#
#     def get_report_by_uid(self, u_id):
#         """
#         Get a report by user id(u_id).
#         :param u_id: The _id of the report you want to get
#         :type u_id: ObjectId
#         :return: result of the get method
#         :rtype: list[dict]
#         """
#
#         assert type(u_id) == ObjectId
#         result = list(self.collection.find({"r_uid": u_id}).sort("r_time", -1))
#         if result:
#             self.log.debug("Get %d report(s) from user %s."
#                            % (len(result), str(u_id)))
#         else:
#             self.log.warning("Get report from user:%s failed. "
#                              % str(u_id))
#         return result
#
#     def get_all_reports(self):
#         """
#         Get all reports.
#         :return: result of the get method
#         :rtype: list[dict]
#         """
#         result = list(self.collection.find().sort("r_time", -1))
#         if result:
#             self.log.debug("Get %d report(s)."
#                            % len(result))
#         else:
#             self.log.warning("Get all reports failed. ")
#         return result
#
#     def fast_get_report_by_rid(self, r_id):
#         """
#         TODO
#         :param r_id: The _id of the report you want to get
#         :type r_id: str
#         :return: result of the get method
#         :rtype: dict
#         """
#
#         assert type(r_id) == ObjectId
#
#         result = self.collection.find_one({"_id": r_id})
#         self.log.debug("Get report %s" % r_id)
#         return result
#
#     def search_report_by_tag(self, r_tag_list=[]):
#         """
#         Search report by the given tag list.
#         If the tag list of the report and the target tag list have at least
#         one same tag, then recall this report.
#         :param r_tag_list: Target tags
#         :type r_tag_list: list[str]
#         :return: target reports
#         :rtype: list[dict]
#         """
#         assert isinstance(r_tag_list, list)
#         for _tag in r_tag_list:
#             assert type(_tag) == str
#
#         report_list = []
#         for _report in self.collection.find().sort("r_time", -1):
#             if set(_report["r_tag_list"]) & set(r_tag_list):
#                 self.log.debug("Find report with tag(s) \"%s\": _id:%s"
#                                % (str(set(r_tag_list)), _report["_id"]))
#                 report_list.append(_report)
#
#         if report_list:
#             self.log.debug("Find %d report(s) with tag(s) \"%s\"."
#                            % (len(report_list), str(set(r_tag_list))))
#         else:
#             self.log.warning("Unable to find report with tag(s) \"%s\"."
#                              % str(set(r_tag_list)))
#
#         return report_list
#
#     def search_report_by_location(self, r_location="Mars"):
#         """
#         Recall reports that have the same location as the target location
#         :param r_location: Target location
#         :type r_location: str
#         :return: target reports
#         :rtype: list[dict]
#         """
#         assert type(r_location) == str
#
#         report_list = []
#         for _report in self.collection.find().sort("r_time", -1):
#             if _report["r_location"] == r_location:
#                 report_list.append(_report)
#                 self.log.debug("Find report with r_location \"%s\": _id:%s"
#                                % (r_location, _report["_id"]))
#         if report_list:
#             self.log.debug("Find %d report(s) with location \"%s\"."
#                            % (len(report_list), r_location))
#         else:
#             self.log.warning("Unable to find report with location \"%s\"."
#                              % r_location)
#         return report_list
#
#     def delete_report_by_id(self, r_id):
#         """
#         Delete one report according to report id(r_id)
#         :param r_id: Id of the report you wish to delete
#         :type r_id: ObjectId
#         """
#         assert type(r_id) == ObjectId
#
#         result = self.collection.delete_one({"_id": r_id})
#         if result.deleted_count:
#             self.log.debug("Report deleted. ID: %s" % r_id)
#         else:
#             self.log.warning("Report deletion failed: %s" % result.raw_result)
#
#     def get_report_by_tname(self, r_tname):
#         #result = self.collection.find({"r_tname": r_tname}).sort("r_time", -1)
#         #self.log.debug("Get all reports under r_tname %s" % r_tname)
#         #return result
#
#         #assert type(r_tname) == str
#
#         report_list = []
#         for _report in self.collection.find().sort("r_time", -1):
#             if _report["r_tname"] == r_tname:
#                 report_list.append(_report)
#                 self.log.debug("Get all reports under r_tname %s" % r_tname)
#         return report_list
#
# # Below is the test part.
# if __name__ == "__main__":
#     print("Test1: init a report_db_api object and connect to db.")
#     report = report_db_api()
#     test_id = ObjectId("5da733a794196bf0ff5f06db")
#     print(report.get_report_by_uid(u_id=test_id))
#     print(report.get_all_reports())
#     now = datetime.datetime.now()
#     time.sleep(1)
#     print("Test2: add a new report with user id(u_id), target url and time. ")
#     #test_id = report.add_report("5da733a794196bf0ff5f06db", "url", now, "Portrait")
#     #test_id1 = report.add_report("5da733a794196bf0ff5f06db", "url", now, "Portrait")
#     #test_id2 = report.add_report("5da733a794196bf0ff5f06db", "url", now, "Portrait")
#     #test_id3 = report.add_report("5da733a794196bf0ff5f06db", "url", now, "Portrait")
#     #time.sleep(1)
#     print("Test3: get a detailed report by report id(r_id). ")
#     #print("Detailed report: ", report.get_report_by_rid(test_id))
#     #time.sleep(1)
#     print("Test4: get a detailed report by location of the report. ")
#     print("Detailed report: ", report.search_report_by_location("Mars"))
#     # time.sleep(1)
#     # print("Test5: delete a report by id. ")
#     # report.delete_report_by_id(test_id)
#     # time.sleep(1)
#     # print("Test6: delete a report which is not exist in the db. ")
#     # report.delete_report_by_id(test_id)
#     cursor = report.get_report_by_tname('Portrait')
#     for document in cursor:
#         print(document)
