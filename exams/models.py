from django.db import models

from users.models import CustomUser


class Room(models.Model):
    """
    Represents an examination room.
    Used for automatic seat allocation based on capacity and location.
    """
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    building = models.CharField(max_length=50)
    floor = models.IntegerField()

    def __str__(self):
        return f"Room {self.room_number} ({self.building}, Floor {self.floor})"


class Course(models.Model):
    """
    Academic course.
    Used for exam grouping and seating rules.
    """
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    credits = models.IntegerField()

    def __str__(self):
        return f"{self.code} - {self.name}"


class Student(models.Model):
    """
    Student details.
    """
    enrollment_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.enrollment_id} - {self.name}"


class Exam(models.Model):
    """
    Examination event.
    """
    name = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StudentExam(models.Model):
    """
    Mapping table: which student is registered for which exam.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'exam')
        verbose_name = "Student Exam"
        verbose_name_plural = "Student Exams"

    def __str__(self):
        return f"{self.student} → {self.exam}"
    


class InvigilatorAssignment(models.Model):

    DUTY_CHOICES = [
        ('chief', 'Chief Invigilator'),
        ('assistant', 'Assistant Invigilator'),
    ]

    invigilator = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'invigilator'}
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    duty_type = models.CharField(max_length=20, choices=DUTY_CHOICES)

    class Meta:
        unique_together = [
            ('invigilator', 'exam'),   # ❌ no double rooms for same exam
            ('exam', 'room', 'duty_type')  # ❌ no duplicate duty in room
        ]
        ordering = ('exam', 'room', 'duty_type')
        verbose_name = "Invigilator Assignment"
        verbose_name_plural = "Invigilator Assignments"

    def __str__(self):
        return (
            f"{self.invigilator} | "
            f"{self.exam} | "
            f"{self.room} | "
            f"{self.get_duty_type_display()}"
        )
    



