from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    # Direct login paths
    path('login/admin/', views.direct_login_admin, name='direct_login_admin'),
    path('login/teacher/', views.direct_login_teacher, name='direct_login_teacher'),
    path('login/student/', views.direct_login_student, name='direct_login_student'),
]
