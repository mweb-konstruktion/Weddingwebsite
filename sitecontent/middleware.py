from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class SitePasswordMiddleware:
    """Requires visitors to enter a shared site password before seeing any page."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_path = reverse('site_login')
        if (
            request.session.get('site_unlocked')
            or request.path == login_path
            or request.path.startswith(settings.STATIC_URL)
        ):
            return self.get_response(request)
        return redirect(f"{login_path}?next={request.path}")
