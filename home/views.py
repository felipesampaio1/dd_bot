from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from config.models import Config


@login_required
def home_view(request):
    config = Config.objects.first()
    return render(request, 'home/home.html', {'user': request.user, 'config': config})