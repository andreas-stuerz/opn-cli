from click.exceptions import ClickException


class APIException(ClickException):
    def __init__(self, *args, status_code=None, resp_body=None, url=None, **kwargs):
        self.resp_body = resp_body
        self.status_code = status_code
        self.url = url
        message = {
            "API client": kwargs.get('message', resp_body),
        }
        if url:
            message['url'] = url
        super(APIException, self).__init__(message, *args)
