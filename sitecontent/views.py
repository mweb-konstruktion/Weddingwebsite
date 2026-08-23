from django.conf import settings
from django.shortcuts import redirect, render

from .forms import RSVPForm
from .models import RSVPGuest, RSVPSubmission


def home(request):
    return render(request, 'wedding/index.html')


def rsvp(request):
    submitted = False

    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            no_of_guests = int(form.cleaned_data['no_of_guests'])
            submission = RSVPSubmission.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                no_of_guests=no_of_guests,
                message=form.cleaned_data['message'],
            )
            RSVPGuest.objects.bulk_create([
                RSVPGuest(
                    submission=submission,
                    name=form.cleaned_data[f'guest_name_{i}'],
                    meal=form.cleaned_data[f'guest_meal_{i}'],
                    allergies=form.cleaned_data[f'guest_allergies_{i}'],
                )
                for i in range(1, no_of_guests + 1)
            ])
            submitted = True
            form = RSVPForm()
    else:
        form = RSVPForm()

    return render(request, 'wedding/rsvp.html', {'form': form, 'submitted': submitted})


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
