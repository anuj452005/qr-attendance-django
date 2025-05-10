from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'core:home')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('accounts:login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.username}. You can now log in.")
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def direct_login_admin(request):
    """Direct login as admin without password"""
    if request.user.is_authenticated:
        logout(request)

    # Get admin user
    admin_user = CustomUser.objects.filter(user_type='ADMIN').first()
    if admin_user:
        login(request, admin_user)
        messages.success(request, f"You are now logged in as Admin: {admin_user.username}")
        return redirect('core:home')
    else:
        # Create admin user if not exists
        admin_user = CustomUser.objects.create_user(
            username='admin1',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            user_type='ADMIN',
            is_staff=True,
            is_superuser=True
        )
        login(request, admin_user)
        messages.success(request, f"Admin user created and logged in: {admin_user.username}")
        return redirect('core:home')

def direct_login_teacher(request):
    """Direct login as teacher without password"""
    if request.user.is_authenticated:
        logout(request)

    # Get teacher user
    teacher_user = CustomUser.objects.filter(user_type='TEACHER').first()
    if teacher_user:
        login(request, teacher_user)
        messages.success(request, f"You are now logged in as Teacher: {teacher_user.username}")
        return redirect('core:home')
    else:
        # Create teacher user if not exists
        teacher_user = CustomUser.objects.create_user(
            username='teacher1',
            email='teacher@example.com',
            password='teacher123',
            first_name='Teacher',
            last_name='User',
            user_type='TEACHER'
        )
        login(request, teacher_user)
        messages.success(request, f"Teacher user created and logged in: {teacher_user.username}")
        return redirect('core:home')

def direct_login_student(request):
    """Direct login as student without password"""
    if request.user.is_authenticated:
        logout(request)

    # Get student user
    student_user = CustomUser.objects.filter(user_type='STUDENT').first()
    if student_user:
        login(request, student_user)
        messages.success(request, f"You are now logged in as Student: {student_user.username}")
        return redirect('core:home')
    else:
        # Create student user if not exists
        student_user = CustomUser.objects.create_user(
            username='student1',
            email='student@example.com',
            password='student123',
            first_name='Student',
            last_name='User',
            user_type='STUDENT'
        )
        login(request, student_user)
        messages.success(request, f"Student user created and logged in: {student_user.username}")
        return redirect('core:home')
