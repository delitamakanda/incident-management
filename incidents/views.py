from django.shortcuts import render
from .models import Host, Service


def dashboard(request):
    hosts = Host.objects.all()
    services = Service.objects.all()
    return render(request, 'dashboard.html', {'hosts': hosts, 'services': services})
