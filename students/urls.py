from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('list/', views.student_list, name='student_list'),
    path('detail/<str:student_id>/', views.student_detail, name='student_detail'),
]
