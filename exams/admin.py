from django.contrib import admin

# Register your models here.
from .models import Room,Course ,Student, Exam                 #why?  To instantly add rooms,courses,edit/delete records

class RoomAdmin(admin.ModelAdmin):
    list_display =['room_number','capacity','building','floor']
    search_fields = ['room_number','building']


class StudentAdmin(admin.ModelAdmin):
    list_display =['enrollment_id','name','semester','email']
    search_fields = ['enrollment_id','name']
    list_filter = ['semester']


admin.site.register(Room, RoomAdmin) 
admin.site.register(Course) 
admin.site.register(Student, StudentAdmin) 
admin.site.register(Exam)