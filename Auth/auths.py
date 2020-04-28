# # from flask_jwt import JWT, jwt_required
# # from app.users.model import Users
#
# import time
# from models import user_db_api
# user_server = user_db_api()
# class Auth():
#     def error_handler(self, e):
#         print(e)
#         return "Something bad happened", 400
#
#
#     def authenticate(self, username, password):
#         userInfo = user_server.
#         if (userInfo is None):
#             self.error_handler('找不到用户')
#         else:
#             if (Users.check_password(Users, userInfo.password, password)):
#                 login_time = int(time.time())
#                 userInfo.login_time = login_time
#                 Users.update(Users)
#                 return userInfo
#             else:
#                 self.error_handler('密码不正确')
#
#
#     def identity(self, payload):
#         id = payload['identity']
#         return Users.get(Users, id)