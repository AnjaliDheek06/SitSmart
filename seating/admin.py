from django.contrib import admin
from .models import Seat, SeatingAllocation
from exams.models import StudentExam, Room


@admin.action(description="Allocate seats for selected exams")
def allocate_seats_for_exam(modeladmin, request, queryset):
    for exam in queryset:
        # Delete old allocations for safety
        SeatingAllocation.objects.filter(exam=exam).delete()

        student_exams = StudentExam.objects.filter(
            exam=exam
        ).order_by('student__enrollment_id')

        rooms = Room.objects.all().order_by('room_number')

        student_index = 0
        total_students = student_exams.count()

        for room in rooms:
            seat_number = 1

            for _ in range(room.capacity):
                if student_index >= total_students:
                    return

                SeatingAllocation.objects.create(
                    student=student_exams[student_index].student,
                    exam=exam,
                    room=room,
                    seat_number=seat_number
                )

                seat_number += 2  # alternate seating: 1,3,5,7
                student_index += 1


@admin.register(SeatingAllocation)
class SeatingAllocationAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'room', 'seat_number', 'allocated_at')
    list_filter = ('exam', 'room')
    search_fields = ('student__enrollment_id', 'student__name')
    ordering = ('room__room_number', 'seat_number')


admin.site.register(Seat)
