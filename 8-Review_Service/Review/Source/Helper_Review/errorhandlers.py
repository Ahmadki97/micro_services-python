class customError(Exception):
    status_code = None
    status = None

    def __init__(self, message, coming_from):
        super().__init__(message)
        self.coming_from = coming_from

    def serializeErrors(self):
        return {
            'message': str(self),
            'status_code': self.status_code,
            'status': self.status,
            'coming_from': self.coming_from
        }
    



class BadRequestError(customError):
        status_code = 400
        status = 'Bad Request Error'


class NotFoundError(customError):
     status_code = 404
     status = 'Resource Not Found Error'


class NotAuthorizedError(customError):
     status_code = 401
     status = 'Not Authorized To access the Resource'


class FileTooLargeError(customError):
     status_code = 413
     status = 'File Too Large'


class ServerError(customError):
     status_code = 503
     status = 'Server Error'
