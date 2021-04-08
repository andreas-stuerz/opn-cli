class APIException(Exception):
    def __init__(self, status_code=None, resp_body=None, *args, **kwargs):
        self.resp_body = resp_body
        self.status_code = status_code
        message = kwargs.get('message', resp_body)
        super(APIException, self).__init__(message, *args, **kwargs)
