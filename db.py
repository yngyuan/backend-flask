from pymongo import MongoClient
import logging
client = MongoClient(
            "mongodb+srv://zed:yy9826@cluster0-uaytj.mongodb.net/" \
            "test?retryWrites=true&w=majority")
db = client.apt
# class Db:
#     def __init__(self):
#         self.log = logging
#         self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
#         client = MongoClient(
#             "mongodb+srv://zed:yy9826@cluster0-uaytj.mongodb.net/" \
#             "test?retryWrites=true&w=majority")
#         self.db = client.apt
#     def getDb(self):
#         return self.db