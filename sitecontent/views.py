from django.conf import settings
from django.shortcuts import redirect, render


def home(request):
    return render(request, 'wedding/index.html')


def site_login(request):
    error = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        if password == settings.SITE_PASSWORD:
            request.session['site_unlocked'] = True
            next_url = request.POST.get('next') or '/'
            return redirect(next_url)
        error = 'Falsches Passwort.'
    next_url = request.GET.get('next', '/')
    return render(request, 'wedding/login.html', {'error': error, 'next': next_url})
