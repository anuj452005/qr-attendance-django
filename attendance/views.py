from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from .models import Attendance, QRCode, AttendanceToken
from timetable.models import Timetable
from students.models import Student
import json
import qrcode
import base64
from io import BytesIO

# Create your views here.

@login_required
def attendance_list(request):
    if request.user.is_admin or request.user.is_teacher:
        attendances = Attendance.objects.all()
    elif request.user.is_student:
        try:
            student = request.user.student_profile
            attendances = Attendance.objects.filter(student=student)
        except:
            messages.error(request, "Student profile not found.")
            return redirect('core:home')
    else:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('core:home')
    
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

@login_required
def take_attendance(request):
    if not request.user.is_teacher:
        messages.error(request, "Only teachers can take attendance.")
        return redirect('core:home')
    
    try:
        teacher = request.user.teacher_profile
        timetables = Timetable.objects.filter(teacher=teacher)
    except:
        messages.error(request, "Teacher profile not found.")
        return redirect('core:home')
    
    if request.method == 'POST':
        timetable_id = request.POST.get('timetable_id')
        timetable = get_object_or_404(Timetable, id=timetable_id, teacher=teacher)
        
        # Create QR code
        qr_code = QRCode.objects.create(
            timetable=timetable,
            expires_at=timezone.now() + timezone.timedelta(minutes=5)
        )
        
        # Generate QR code image
        qr_data = {
            'code': str(qr_code.code),
            'timetable_id': timetable_id,
            'timestamp': timezone.now().isoformat()
        }
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        qr_image = base64.b64encode(buffer.getvalue()).decode()
        
        return render(request, 'attendance/qr_display.html', {
            'qr_code': qr_code,
            'qr_image': qr_image,
            'timetable': timetable
        })
    
    return render(request, 'attendance/take_attendance.html', {'timetables': timetables})

@login_required
def generate_direct_qr(request):
    if not request.user.is_teacher:
        messages.error(request, "Only teachers can generate attendance QR codes.")
        return redirect('core:home')
    
    try:
        teacher = request.user.teacher_profile
        timetables = Timetable.objects.filter(teacher=teacher)
    except:
        messages.error(request, "Teacher profile not found.")
        return redirect('core:home')
    
    if request.method == 'POST':
        timetable_id = request.POST.get('timetable_id')
        timetable = get_object_or_404(Timetable, id=timetable_id, teacher=teacher)
        
        # Create attendance token
        attendance_token = AttendanceToken.generate_token(timetable, teacher)
        
        # Get the server's IP address
        host = request.get_host()
        
        # Check if we're using HTTPS
        protocol = 'https' if request.is_secure() else 'http'
        
        # Generate direct URL for QR code
        direct_url = f"{protocol}://{host}{reverse('attendance:direct_mark_attendance', args=[attendance_token.token])}"
        
        # Generate QR code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(direct_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        qr_image = base64.b64encode(buffer.getvalue()).decode()
        
        return render(request, 'attendance/direct_qr_display.html', {
            'token': attendance_token,
            'qr_image': qr_image,
            'timetable': timetable,
            'direct_url': direct_url
        })
    
    return render(request, 'attendance/generate_direct_qr.html', {'timetables': timetables})

@login_required
def scan_qr_code(request):
    if not request.user.is_student:
        messages.error(request, "Only students can mark attendance.")
        return redirect('core:home')
    
    return render(request, 'attendance/scan_qr.html')

@login_required
def mark_attendance(request):
    if not request.user.is_student:
        return JsonResponse({'status': 'error', 'message': 'Only students can mark attendance'})
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_code_uuid = data.get('code')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            qr_code = get_object_or_404(QRCode, code=qr_code_uuid, is_active=True)
            
            if qr_code.is_expired():
                return JsonResponse({'status': 'error', 'message': 'QR code has expired'})
            
            # Check if student profile exists
            try:
                student = request.user.student_profile
            except:
                # Create student profile if it doesn't exist
                student = Student.objects.create(
                    user=request.user,
                    student_id=f"S{request.user.id:03d}",
                    department="Auto Generated",
                    batch="Auto Generated"
                )
                return JsonResponse({
                    'status': 'warning', 
                    'message': 'Student profile was missing and has been auto-created. Please update your profile information.'
                })
            
            timetable = qr_code.timetable
            
            # Check if attendance already exists
            if Attendance.objects.filter(student=student, timetable=timetable, date=timezone.now().date()).exists():
                return JsonResponse({'status': 'error', 'message': 'Attendance already marked for this class today'})
            
            # Create attendance record
            attendance = Attendance.objects.create(
                student=student,
                timetable=timetable,
                qr_code=qr_code,
                date=timezone.now().date(),
                is_present=True,
                ip_address=request.META.get('REMOTE_ADDR'),
                location_latitude=latitude,
                location_longitude=longitude,
                device_info=request.META.get('HTTP_USER_AGENT')
            )
            
            return JsonResponse({'status': 'success', 'message': 'Attendance marked successfully'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def direct_mark_attendance(request, token):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # Save the token in the session for redirect after login
        request.session['attendance_token'] = token
        messages.info(request, "Please log in to mark your attendance")
        return redirect(f"{reverse('accounts:login')}?next={reverse('attendance:direct_mark_attendance', args=[token])}")
    
    # Check if user is a student
    if not request.user.is_student:
        messages.error(request, "Only students can mark attendance")
        return redirect('core:home')
    
    # Get the token
    attendance_token = get_object_or_404(AttendanceToken, token=token)
    
    # Check if token is valid
    if not attendance_token.is_valid():
        if attendance_token.is_used:
            messages.error(request, "This QR code has already been used")
        else:
            messages.error(request, "This QR code has expired")
        return redirect('core:home')
    
    try:
        # Get student profile
        try:
            student = request.user.student_profile
        except:
            # Create student profile if it doesn't exist
            student = Student.objects.create(
                user=request.user,
                student_id=f"S{request.user.id:03d}",
                department="Auto Generated",
                batch="Auto Generated"
            )
            messages.warning(request, "Your student profile was missing and has been auto-created. Please update your profile information.")
        
        timetable = attendance_token.timetable
        
        # Check if attendance already exists
        if Attendance.objects.filter(student=student, timetable=timetable, date=timezone.now().date()).exists():
            messages.warning(request, "You have already marked attendance for this class today")
            return render(request, 'attendance/attendance_confirmation.html', {
                'status': 'warning',
                'message': 'Attendance already marked for this class today',
                'timetable': timetable
            })
        
        # Create attendance record
        attendance = Attendance.objects.create(
            student=student,
            timetable=timetable,
            date=timezone.now().date(),
            is_present=True,
            ip_address=request.META.get('REMOTE_ADDR'),
            device_info=request.META.get('HTTP_USER_AGENT')
        )
        
        # Mark token as used
        attendance_token.is_used = True
        attendance_token.save()
        
        messages.success(request, "Attendance marked successfully")
        return render(request, 'attendance/attendance_confirmation.html', {
            'status': 'success',
            'message': 'Attendance marked successfully',
            'timetable': timetable,
            'attendance': attendance
        })
        
    except Exception as e:
        messages.error(request, f"Error marking attendance: {str(e)}")
        return render(request, 'attendance/attendance_confirmation.html', {
            'status': 'error',
            'message': f'Error: {str(e)}'
        })
