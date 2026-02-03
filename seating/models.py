from django.db import models
from exams.models import Student,Exam,Room

# Create your models here.
class Seat(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE  )
    seat_number = models.IntegerField()
    is_occupied = models.BooleanField(default = False)


from django.db import models
from exams.models import Student, Exam, Room

class SeatingAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    allocated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'exam']

    def __str__(self):
        return f"{self.student} - {self.exam} - Seat {self.seat_number}"


    