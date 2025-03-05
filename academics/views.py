from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department, Subject

# Create your views here.

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'academics/department_list.html', {'departments': departments})

@login_required
def department_detail(request, code):
    department = get_object_or_404(Department, code=code)
    subjects = Subject.objects.filter(department=department)
    return render(request, 'academics/department_detail.html', {'department': department, 'subjects': subjects})

@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'academics/subject_list.html', {'subjects': subjects})

@login_required
def subject_detail(request, code):
    subject = get_object_or_404(Subject, code=code)
    return render(request, 'academics/subject_detail.html', {'subject': subject})
