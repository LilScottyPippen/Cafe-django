from django.utils.deprecation import MiddlewareMixin
from utils.constants import ERROR_MESSAGES
from utils.response import error_response
from django_ratelimit.exceptions import Ratelimited


class RatelimitMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, Ratelimited):
            return error_response(ERROR_MESSAGES['error_too_many_requests'], 429)
        return None
