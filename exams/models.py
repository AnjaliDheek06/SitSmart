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



class Student(models.Model):
    enrollment_id = models.CharField(max_length=20,unique=True)                 #Acts as Primary identification,unique ensures no duplicate enrollement number,enrollemenent id is marked as unique = True  because no 2 students can have same enrollement no 
    name = models.CharField(max_length=100)                                                 
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    semester = models.IntegerField()



class  Exam(models.Model):                                                                             #Here we are modeling examination event
    name = models.CharField(max_length=200)                                               #why doing this?  seating depends on which exam is happening and exam belongs to courses
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField()  #in minutes
    course = models.ForeignKey( Course, on_delete = models.CASCADE)           #creates many to one relationship ,1 course ->many exams, each exam -> exactly one course
                                                                                                                          #on_delete=models.CASCADE means: If a course is deleted all exams of that course are also deleted.It will presesrve data integrity
                                                                                                                          #why? Because each student/exam/subject record must belong to one specific course, while one course can have many students/exams.

