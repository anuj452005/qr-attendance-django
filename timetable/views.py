from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Timetable
from teachers.models import Teacher
from students.models import Student

# Create your views here.

@login_required
def timetable_list(request):
    if request.user.is_admin:
        timetables = Timetable.objects.all()
    elif request.user.is_teacher:
        try:
            teacher = request.user.teacher_profile
            timetables = Timetable.objects.filter(teacher=teacher)
        except Teacher.DoesNotExist:
            messages.error(request, "Teacher profile not found.")
            return redirect('core:home')
    elif request.user.is_student:
        try:
            student = request.user.student_profile
            timetables = Timetable.objects.filter(department=student.department)
        except Student.DoesNotExist:
            messages.error(request, "Student profile not found.")
            return redirect('core:home')
    else:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('core:home')
    
    return render(request, 'timetable/timetable_list.html', {'timetables': timetables})

@login_required
def timetable_detail(request, id):
    timetable = get_object_or_404(Timetable, id=id)
    
    if request.user.is_admin:
        pass  # Admin can view all timetables
    elif request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        if timetable.teacher != request.user.teacher_profile:
            messages.error(request, "You don't have permission to view this timetable.")
            return redirect('timetable:timetable_list')
    elif request.user.is_student and hasattr(request.user, 'student_profile'):
        if timetable.department != request.user.student_profile.department:
            messages.error(request, "You don't have permission to view this timetable.")
            return redirect('timetable:timetable_list')
    else:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('core:home')
    
    return render(request, 'timetable/timetable_detail.html', {'timetable': timetable})
