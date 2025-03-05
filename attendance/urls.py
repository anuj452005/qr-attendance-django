from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('list/', views.attendance_list, name='attendance_list'),
    path('take/', views.take_attendance, name='take_attendance'),
    path('scan/', views.scan_qr_code, name='scan_qr_code'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('generate-direct-qr/', views.generate_direct_qr, name='generate_direct_qr'),
    path('direct-mark/<str:token>/', views.direct_mark_attendance, name='direct_mark_attendance'),
]
