from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('invigilator-dashboard/', views.invigilator_dashboard, name='invigilator_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
]
