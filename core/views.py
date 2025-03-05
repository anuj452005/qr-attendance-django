from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def home(request):
    if request.user.is_admin:
        # Admin dashboard
        return render(request, 'core/admin_dashboard.html')
    elif request.user.is_teacher:
        # Teacher dashboard
        return render(request, 'core/teacher_dashboard.html')
    elif request.user.is_student:
        # Student dashboard
        return render(request, 'core/student_dashboard.html')
    else:
        # Default dashboard
        messages.warning(request, "Your account doesn't have a specific role assigned. Please contact the administrator.")
        return redirect('accounts:login')

def handler404(request, exception):
    return render(request, 'core/404.html', status=404)

def handler500(request):
    return render(request, 'core/500.html', status=500)
