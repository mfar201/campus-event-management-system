from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from .models import UserProfile

def admin_or_club_president_required(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            # Ensure UserProfile exists for the user
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            if user_profile.role in ['admin', 'club_president']:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You are not authorized to perform this action.")
        else:
            return HttpResponseForbidden("You are not authorized to perform this action.")
    return wrap

def admin_or_club_president_required_cbv(view_class):
    class WrappedView(view_class):
        def dispatch(self, request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                # Ensure UserProfile exists for the user
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                if user_profile.role in ['admin', 'club_president']:
                    return super().dispatch(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("You are not authorized to perform this action.")
            else:
                return HttpResponseForbidden("You are not authorized to perform this action.")
    return WrappedView
