from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details


class ApiValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, extras=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _get_error_details(detail, code)
        if extras:
            self.extras = _get_error_details(extras, code)
