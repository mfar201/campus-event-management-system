from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from events.models import EventCategory, Event
from .forms import LoginForm
from .forms import UserRegistrationForm
from events.models import UserProfile
from django.http import HttpResponseForbidden

@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to view this page.")
    user = User.objects.count()
    event_ctg = EventCategory.objects.count()
    event = Event.objects.count()
    complete_event = Event.objects.filter(status='completed').count()
    events = Event.objects.all()
    context = {
        'user': user,
        'event_ctg': event_ctg,
        'event': event,
        'complete_event': complete_event,
        'events': events,
        'username': request.user.username  # Add the username to the context
    }
    return render(request, 'dashboard.html', context)

def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.role == 'club_president':
                    return redirect('event-list')
                elif user_profile.role in ['student', 'faculty']:
                    return redirect('event-list')
                else:
                    return redirect('dashboard')
    context = {
        'form': forms
    }
    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            role = form.cleaned_data['role']
            UserProfile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})