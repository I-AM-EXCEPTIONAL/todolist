# middleware.py

from django.core.exceptions import DisallowedHost

class OriginVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_ORIGIN" in request.META:
            request_origin = request.META["HTTP_ORIGIN"]
            try:
                good_host = request.get_host()
            except DisallowedHost:
                pass
            else:
                good_origin = "%s://%s" % (
                    "https" if request.is_secure() else "http",
                    good_host,
                )
                if request_origin == good_origin:
                    request._origin_verified = True
                else:
                    request._origin_verified = False
        response = self.get_response(request)
        return response
