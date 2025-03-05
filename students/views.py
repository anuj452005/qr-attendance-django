from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student
from accounts.models import CustomUser

# Create your views here.

@login_required
def student_list(request):
    if not request.user.is_admin and not request.user.is_teacher:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('core:home')
    
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def student_detail(request, student_id):
    if not request.user.is_admin and not request.user.is_teacher and not (request.user.is_student and request.user.student_profile.student_id == student_id):
        messages.error(request, "You don't have permission to view this page.")
        return redirect('core:home')
    
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'students/student_detail.html', {'student': student})
