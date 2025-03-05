from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Settings

# Create your views here.

@login_required
def settings_view(request):
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('core:home')
    
    settings, created = Settings.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        settings.site_name = request.POST.get('site_name', settings.site_name)
        settings.site_description = request.POST.get('site_description', settings.site_description)
        settings.qr_code_expiry_time = int(request.POST.get('qr_code_expiry_time', settings.qr_code_expiry_time))
        settings.attendance_location_required = request.POST.get('attendance_location_required') == 'on'
        settings.save()
        
        messages.success(request, "Settings updated successfully.")
        return redirect('administration:settings')
    
    return render(request, 'administration/settings.html', {'settings': settings})
