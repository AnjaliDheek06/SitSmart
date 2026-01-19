from django.contrib import admin

# Register your models here.
from .models import Room,Course                  #why?  To instantly add rooms,courses,edit/delete records
admin .site.register(Room)                                           #Without this we need forms,views,templates just to insert data
admin .site.register(Course)