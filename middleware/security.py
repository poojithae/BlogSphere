import re
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin


class SecurityMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.sts_seconds = settings.SECURE_HSTS_SECONDS
        self.sts_include_subdomains = settings.SECURE_HSTS_INCLUDE_SUBDOMAINS
        self.sts_preload = settings.SECURE_HSTS_PRELOAD
        self.content_type_nosniff = settings.SECURE_CONTENT_TYPE_NOSNIFF
        self.redirect = settings.SECURE_SSL_REDIRECT
        self.redirect_exempt = [re.compile(r) for r in settings.SECURE_REDIRECT_EXEMPT]
        self.redirect_host = settings.SECURE_SSL_HOST
        self.referrer_policy = settings.SECURE_REFERRER_POLICY
        self.cross_origin_opener_policy = settings.SECURE_CROSS_ORIGIN_OPENER_POLICY

    def process_request(self, request):
        path = request.path.lstrip("/")
        print(f"Processing request for path: {path}")
        if (
            self.redirect
            and not request.is_secure()
            and not any(pattern.search(path) for pattern in self.redirect_exempt)
        ):
            host = self.redirect_host or request.get_host()
            redirect_url = f"http://{host}{request.get_full_path()}"
            print(f"Redirecting to HTTP: {redirect_url}")
            return HttpResponsePermanentRedirect(redirect_url)

    def process_response(self, request, response):
        print(f"Processing response for path: {request.path}")
        if (
            self.sts_seconds
            and request.is_secure()
            and "Strict-Transport-Security" not in response
        ):
            sts_header = f"max-age={self.sts_seconds}"
            if self.sts_include_subdomains:
                sts_header += "; includeSubDomains"
            if self.sts_preload:
                sts_header += "; preload"
            response["Strict-Transport-Security"] = sts_header
            print(f"Setting Strict-Transport-Security header: {sts_header}")

        if self.content_type_nosniff:
            response.setdefault("X-Content-Type-Options", "nosniff")
            print("Setting X-Content-Type-Options: nosniff")

        if self.referrer_policy:
            response.setdefault(
                "Referrer-Policy",
                ",".join(
                    v.strip() for v in self.referrer_policy.split(",")
                ),
            )
            print(f"Setting Referrer-Policy: {self.referrer_policy}")

        if self.cross_origin_opener_policy:
            response.setdefault(
                "Cross-Origin-Opener-Policy",
                self.cross_origin_opener_policy,
            )
            print(f"Setting Cross-Origin-Opener-Policy: {self.cross_origin_opener_policy}")

        response.setdefault("X-Frame-Options", "DENY")
        print("Setting X-Frame-Options: DENY")
        response.setdefault("X-XSS-Protection", "1; mode=block")
        print("Setting X-XSS-Protection: 1; mode=block")

        return response
