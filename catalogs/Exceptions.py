from rest_framework.exceptions import APIException


class APIException202(APIException):
    status_code = 202


class BadRequest(APIException):
    status_code = 404
