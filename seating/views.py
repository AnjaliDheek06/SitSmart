from django.shortcuts import  render,redirect, get_object_or_404
from django.contrib import messages
from exams.models import Exam, Room, StudentExam
from exams.models import Student
from .models import SeatingAllocation


def allocate_seats(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # Step 1: Get all students registered for this exam
    student_exams = StudentExam.objects.filter(
        exam=exam
    ).order_by('student__enrollment_id')

    students = [se.student for se in student_exams]

    # Step 2: Get all available rooms
    rooms = Room.objects.all().order_by('room_number')

    # Step 3: Clear old allocations
    SeatingAllocation.objects.filter(exam=exam).delete()

    # Step 4: Allocate seats
    student_index = 0

    for room in rooms:
        seat_number = 1
        while seat_number <= room.capacity and student_index < len(students):
            SeatingAllocation.objects.create(
                student=students[student_index],
                exam=exam,
                room=room,
                seat_number=seat_number
            )
            student_index += 1
            seat_number += 2  # Alternate seating

    messages.success(
        request,
        f'{student_index} students allocated successfully!'
    )

    return redirect('exam_detail', exam_id=exam_id)




def seating_chart(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    allocations = SeatingAllocation.objects.filter(
        exam=exam
    ).order_by('room__room_number', 'seat_number')

    # Group allocations by room
    rooms_data = {}
    for allocation in allocations:
        room_number = allocation.room.room_number
        rooms_data.setdefault(room_number, []).append(allocation)

    context = {
        'exam': exam,
        'rooms_data': rooms_data
    }

    return render(request, 'seating/seating_chart.html', context)




def search_seat(request):
    enrollment_id = request.GET.get('enrollment_id')

    if not enrollment_id:
        messages.error(request, "Please enter enrollment ID")
        return redirect('student_dashboard')

    try:
        student = Student.objects.get(enrollment_id=enrollment_id)

        allocations = SeatingAllocation.objects.filter(
            student=student
        ).select_related('exam', 'room').order_by('-exam__date')

        context = {
            'student': student,
            'allocations': allocations,
        }
        return render(request, 'seating/seat_result.html', context)

    except Student.DoesNotExist:
        messages.error(request, "Student not found!")
        return redirect('student_dashboard')



def download_slip(request, allocation_id): 
    allocation = SeatingAllocation.objects.get(id=allocation_id) 
    context = {'allocation': allocation} 
    return render(request, 'seating/seating_slip.html', context)