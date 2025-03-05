from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher
from accounts.models import CustomUser

# Create your views here.

@login_required
def teacher_list(request):
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('core:home')
    
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

@login_required
def teacher_detail(request, teacher_id):
    if not request.user.is_admin and not (request.user.is_teacher and request.user.teacher_profile.teacher_id == teacher_id):
        messages.error(request, "You don't have permission to view this page.")
        return redirect('core:home')
    
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})
