from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('list/', views.timetable_list, name='timetable_list'),
    path('detail/<int:id>/', views.timetable_detail, name='timetable_detail'),
]
