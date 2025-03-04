from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PayerForm
from .models import Payer

@login_required
def list_payers(request):
    payers = Payer.objects.all()
    return render(request, 'payers/list_payers.html', {'payers': payers})

@login_required
def add_payer(request):
    if request.method == 'POST':
        form = PayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_payers')
    else:
        form = PayerForm()
    return render(request, 'payers/form_payer.html', {'form': form})

@login_required
def edit_payer(request, id):
    payer = get_object_or_404(Payer, id=id)
    if request.method == 'POST':
        form = PayerForm(request.POST, instance=payer)
        if form.is_valid():
            form.save()
            return redirect('list_payers')
    else:
        if payer.der:
            payer.der = payer.der.strftime('%Y-%m-%d')

        form = PayerForm(instance=payer)
    return render(request, 'payers/form_payer.html', {'form': form})

@login_required
def delete_payer(request, id):
    payer = get_object_or_404(Payer, id=id)
    if request.method == 'POST':
        payer.delete()
        return redirect('list_payers')
    return render(request, 'payers/confirm_exclusion.html', {'payer': payer})