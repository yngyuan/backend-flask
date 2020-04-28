from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
def send_push_message(token, message, extra=None):
    try:
        bodyContent = {'message' : "hello"}
        response = PushClient().publish(
            PushMessage(to=token,

                        body='hello',

                        data=extra))
        print(response.is_success())
    except PushServerError as exc:
        print(exc.errors)
        print("---")
        print(exc.response_data)
    except (ConnectionError, HTTPError) as exc:
        print(exc.errors)
        print("---")

if __name__ == '__main__':
    send_push_message("ExponentPushToken[Pq42ZIAz7ptZerwIu4Yduw]", "you have a new message", {'title': 'Message received!'})