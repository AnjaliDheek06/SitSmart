# exams/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('upload-students/', views.upload_students, name='upload_students'),

    # ROOM CRUD
    path('add-room/', views.add_room, name='add_room'),
    path('manage-rooms/', views.manage_rooms, name='manage_rooms'),
    path('edit-room/<int:room_id>/', views.edit_room, name='edit_room'),
    path('delete-room/<int:room_id>/', views.delete_room, name='delete_room'),

    # EXAM CRUD
    path('add-exam/', views.add_exam, name='add_exam'),
    path('manage-exams/', views.manage_exams, name='manage_exams'),
    path('edit-exam/<int:exam_id>/', views.edit_exam, name='edit_exam'),
    path('delete-exam/<int:exam_id>/', views.delete_exam, name='delete_exam'),

    path('exam/<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('exam/<int:exam_id>/assign-invigilator/', views.assign_invigilator, name='assign_invigilator'),

    # SEAT SEARCH
    path('search-seat/', views.search_seat, name='search_seat'),

    # DOWNLOAD SEATING SLIP
    path(
        'download-seating-slip/<int:allocation_id>/',
        views.download_seating_slip,
        name='download_seating_slip'
    ),

    # ✅ PRINT SEATING SLIP (THIS WAS MISSING)
    path(
        'print-seating-slip/<int:allocation_id>/',
        views.print_seating_slip,
        name='print_seating_slip'
    ),

    path('exam/<int:exam_id>/report/', views.exam_report, name='exam_report'),
]
