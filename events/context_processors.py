from django.conf import settings

def add_username(request):
    return {'username': request.user.username if request.user.is_authenticated else 'Guest'}