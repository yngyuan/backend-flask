from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from flask import jsonify, request
from flask_restful import Resource
import logging
from datetime import datetime
from models.user_db_api import user_db_api

user_server = user_db_api()
# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.

def send_notifications(users, message, extra=None):
    curr_time = datetime.now()
    tokens_to_send = []
    for user in users:
        keys = user.keys()
        if 'u_token' in keys and 'u_token_expire_time' in keys:
            # check if time expire
            expire_time = datetime.strptime(user['u_token_expire_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            if (expire_time > curr_time):
                tokens_to_send.append(user['u_token'])

    for token in tokens_to_send:
        print("send notification to token : " + token)
        print(type(token))
        print(type(message))
        send_push_message(token, message)


    # except PushServerError as exc:
    #     # Encountered some likely formatting/validation error.
    #     rollbar.report_exc_info(
    #         extra_data={
    #             'token': token,
    #             'message': message,
    #             'extra': extra,
    #             'errors': exc.errors,
    #             'response_data': exc.response_data,
    #         })
    #     raise
    # except (ConnectionError, HTTPError) as exc:
    #     # Encountered some Connection or HTTP error - retry a few times in
    #     # case it is transient.
    #     rollbar.report_exc_info(
    #         extra_data={'token': token, 'message': message, 'extra': extra})
    #     raise self.retry(exc=exc)
    #
    # try:
    #     # We got a response back, but we don't know whether it's an error yet.
    #     # This call raises errors so we can handle them with normal exception
    #     # flows.
    #     response.validate_response()
    # except DeviceNotRegisteredError:
    #     # Mark the push token as inactive
    #     from notifications.models import PushToken
    #     PushToken.objects.filter(token=token).update(active=False)
    # except PushResponseError as exc:
    #     # Encountered some other per-notification error.
    #     rollbar.report_exc_info(
    #         extra_data={
    #             'token': token,
    #             'message': message,
    #             'extra': extra,
    #             'push_response': exc.push_response._asdict(),
    #         })
    #     raise self.retry(exc=exc)
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
class Notification(Resource):
    def __init__(self):
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    def post(self):
        data = request.get_json()
        user_id = data['uid']
        token = data['token']
        expire_time = data['expire_time']
        test_uid = '5daf8d2f72eb94efe98bd904'
        self.log.debug(user_id + " send token " + token + " with expire time : " + expire_time)

        #add as user property
        user_server.add_token(user_id, token, expire_time)


def send_push_message(token, message):
    try:
        extra = {"title": message}
        response = PushClient().publish(
            PushMessage(to=token,

                        body="notification",

                        data=extra))
        print(response.is_success())
    except PushServerError as exc:
        print(exc.errors)
        print(exc.response_data)
    except (ConnectionError, HTTPError) as exc:
        print(exc.errors)

