from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Config


@login_required
def config_view(request):
    config = Config.objects.first()

    if request.method == "POST":

        execution_period = request.POST.get("execution_period")
        autenticado = request.POST.get("autenticado") == "on"
        if execution_period:
            config.execution_period = int(execution_period)
        config.autenticado = autenticado
        config.save()

    return render(request, 'config/config.html', {'user': request.user, 'config': config})