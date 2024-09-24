from django.conf import settings
from django.contrib import auth
from django.contrib.auth.middleware import MiddlewareMixin
from django.core.cache import cache
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject
import logging

logger = logging.getLogger('blog_manager.middleware')

def get_user(request):
    if not hasattr(request, "_cached_user"):
        request._cached_user = auth.get_user(request)
    return request._cached_user

class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, "session"):
            raise ImproperlyConfigured(
                "The Django authentication middleware requires session middleware to be installed."
            )
        logger.debug("Processing request in AuthenticationMiddleware")
        request.user = SimpleLazyObject(lambda: get_user(request))
        logger.debug(f"User set to: {request.user}")

class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            logger.debug("User is authenticated")
            return None
        logger.warning("User is not authenticated, redirecting to login")
        return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)

class RemoteUserMiddleware(MiddlewareMixin):
    header = "REMOTE_USER"

    def process_request(self, request):
        if not hasattr(request, "user"):
            raise ImproperlyConfigured("Authentication middleware is required.")
        username = request.META.get(self.header)
        if username:
            user = auth.authenticate(request, remote_user=username)
            if user:
                auth.login(request, user)
                logger.debug(f"User {username} authenticated and logged in.")

class PersistentRemoteUserMiddleware(RemoteUserMiddleware):
    force_logout_if_no_header = False

# class CsrfViewMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.method in ('GET', 'HEAD', 'OPTIONS'):
#             return None
        
#         csrf_token = request.META.get('HTTP_X_CSRFTOKEN') or request.POST.get('csrfmiddlewaretoken')
        
#         if not csrf_token or csrf_token != request.session.get('csrf_token'):
#             logger.warning("CSRF token missing or incorrect.")
#             return JsonResponse({'error': 'CSRF token missing or incorrect.'}, status=403)
        
#         return None

#     def process_response(self, request, response):
#         if 'csrf_token' not in request.session:
#             request.session['csrf_token'] = secrets.token_urlsafe(32)
        
#         response['X-CSRFToken'] = request.session['csrf_token']
#         return response