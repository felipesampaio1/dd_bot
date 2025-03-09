from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def config_view(request):
    return render(request, 'config/config.html', {'user': request.user})