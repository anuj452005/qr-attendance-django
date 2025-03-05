from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('departments/', views.department_list, name='department_list'),
    path('departments/<str:code>/', views.department_detail, name='department_detail'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/<str:code>/', views.subject_detail, name='subject_detail'),
]
