from django.db import models
from exams.models import Room

# Create your models here.
class Seat(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE  )
    seat_number = models.IntegerField()
    is_occupied = models.BooleanField(default = False)

    