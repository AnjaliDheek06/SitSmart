from django.db import models

# Create your models here.
class Room(models.Model):                                                            #why?  To create DB table Room
    room_number = models.CharField(max_length=10)                                # sitsmart needs room
    capacity = models.IntegerField()                                                              #This model will allow atomatic allocation based on capacity
    building = models.CharField(max_length=50)                                          #Prevents over crowding and logical of rooms  (building/floor)
    floor = models.IntegerField()                                                                    #Without this model automation is impossible



class Course(models.Model):                                                          #why?  In seating exam system, course is required
    code = models.CharField(max_length=10)                                             #Rules depend upon: same course student should not sit together , course-wise room distribution
    name = models.CharField(max_length=100)                                           # will later be connected with student, exam ,seating algorithm                               
    credits = models. IntegerField()                                                             



