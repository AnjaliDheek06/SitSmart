from django.urls import path 
from . import views 
urlpatterns = [ 
    path('allocate/<int:exam_id>/', views.allocate_seats, name='allocate_seats'), 
    path( 'chart/<int:exam_id>/', views.seating_chart, name='seating_chart'),
    path('search/', views.search_seat, name='search_seat'),
    path('slip/<int:allocation_id>/', views.download_slip, name='download_slip'),
] 
