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

    # Get or create admin user
    admin_user = CustomUser.objects.filter(username='admin1').first()
    if admin_user:
        login(request, admin_user)
        messages.success(request, f"You are now logged in as Admin: {admin_user.username}")
        return redirect('core:home')
    else:
        messages.error(request, "Admin user not found. Please use regular login.")
        return redirect('accounts:login')

def direct_login_teacher(request):
    """Direct login as teacher without password"""
    if request.user.is_authenticated:
        logout(request)

    # Get or create teacher user
    teacher_user = CustomUser.objects.filter(username='teacher1').first()
    if teacher_user:
        login(request, teacher_user)
        messages.success(request, f"You are now logged in as Teacher: {teacher_user.username}")
        return redirect('core:home')
    else:
        messages.error(request, "Teacher user not found. Please use regular login.")
        return redirect('accounts:login')

def direct_login_student(request):
    """Direct login as student without password"""
    if request.user.is_authenticated:
        logout(request)

    # Get or create student user
    student_user = CustomUser.objects.filter(username='student1').first()
    if student_user:
        login(request, student_user)
        messages.success(request, f"You are now logged in as Student: {student_user.username}")
        return redirect('core:home')
    else:
        messages.error(request, "Student user not found. Please use regular login.")
        return redirect('accounts:login')
