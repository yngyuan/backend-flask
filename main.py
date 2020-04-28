import datetime
from flask import Flask, render_template, request
from models.theme_db_api import theme_db_api
from models.report_db_api import report_db_api
from models.user_db_api import user_db_api
from flask_restful import Api
from resources.view import ViewMain, ViewOne
from resources.user import User, UserRegister, UserLogin, UserLogout
from resources.userMobile import UserLoginMoblie,UserRegisterMobile
from resources.search import Search
from resources.create import CreateTheme, CreateReport
from resources.management import Management, Managedecr, Manageincr, Managedele
from resources.managemobile import ManageMobile
from flask_jwt_extended import JWTManager
from image.flask_imgur import Imgur
from resources.viewMobile import ViewMobile, ViewOneMobile
from resources.SubscribeMobile import SubscribeMobile, SubscribeOneMobile
from resources.searchMobile import SearchMobile
from resources.createMobile import CreateReportMobile
from resources.shareMobile import ShareMobile
from resources.notification import Notification
app = Flask(__name__)
app.secret_key = 'team14'  # could do app.config['JWT_SECRET_KEY'] if we prefer
api = Api(app)
jwt = JWTManager(app)
app.config["SECRET_KEY"] = "dafdsagewag.wea(-+zsvz?"#for encrypt session into cookie
app.config["IMGUR_ID"] = "dc66eb244b26224"
imgur_handler = Imgur(app)

# access mongodb

_user_server = user_db_api()
_report_server = report_db_api()
_theme_server = theme_db_api()

_report = _report_server.search_report_by_location()

# need api for getting report by user id to get a list of report of specified user
# report = report_server.search_report_by_location()
rIndex = 0


def get_all_themes():
    user = _report_server.user_db_api.get_user_by_username("modified_admin1")
    themes = []
    if user is not None:
        for theme in user['u_subscribed_themes']:
            themes.append(_theme_server.get_theme_by_name(theme))
    return themes


def get_all_report():
    return _report_server.search_report_by_location()


@app.route('/')
def root():
    themes = list(_theme_server.get_all_theme())
    return render_template('view.html', theme=themes, length=len(themes))


api.add_resource(CreateReport, '/createReport.html',
                 resource_class_kwargs={'imgur_handler': imgur_handler})
api.add_resource(CreateTheme, '/createTheme.html',
                 resource_class_kwargs={'imgur_handler': imgur_handler})
api.add_resource(ViewMain, '/view.html')
api.add_resource(ViewOne, '/viewone/<string:t_name>')
api.add_resource(User, '/user/<string:user_name>')
api.add_resource(UserLogin, '/login.html')
api.add_resource(UserRegister, '/register.html')
api.add_resource(UserLogout, '/logout.html')
api.add_resource(Search, '/search.html',
                 resource_class_kwargs={
                     'userdb': _user_server, 'reportdb': _report_server})
api.add_resource(Management, '/manage.html')
api.add_resource(Managedecr, '/managedecr')
api.add_resource(Manageincr, '/manageincr')
api.add_resource(Managedele, '/managedele/<int:index>')

api.add_resource(ManageMobile, '/manageMobile')

api.add_resource(UserLoginMoblie, '/userLoginMobile')
api.add_resource(UserRegisterMobile, '/registerMobile')

api.add_resource(ViewMobile, '/viewMobile')
api.add_resource(ViewOneMobile, '/viewOneMobile')

api.add_resource(SubscribeMobile, '/subscribeMobile')
api.add_resource(SubscribeOneMobile, '/subscribeOneMobile')
api.add_resource(SearchMobile, '/searchMobile')
api.add_resource(CreateReportMobile, '/createReportMobile.html')
api.add_resource(ShareMobile, '/shareMobile')
api.add_resource(Notification, '/notification')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
