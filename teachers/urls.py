from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('list/', views.teacher_list, name='teacher_list'),
    path('detail/<str:teacher_id>/', views.teacher_detail, name='teacher_detail'),
]
