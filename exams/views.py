# exams/views.py

import pandas as pd
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from exams.forms import InvigilatorAssignmentForm
from exams.models import InvigilatorAssignment, Exam, StudentExam
from seating.models import SeatingAllocation

from .forms import StudentUploadForm, RoomForm, ExamForm
from .models import Student, Room, Exam


def home(request):
    return render(request, 'exams/home.html')


def upload_students(request):
    if request.method == 'POST':
        form = StudentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                excel_file = request.FILES['excel_file']

                # READ EXCEL
                df = pd.read_excel(excel_file)

                created_count = 0

                for _, row in df.iterrows():
                    student, created = Student.objects.get_or_create(
                        enrollment_id=row['enrollment_id'],
                        defaults={
                            'name': row['name'],
                            'email': row['email'],
                            'phone': row['phone'],
                            'semester': row['semester'],
                        }
                    )
                    if created:
                        created_count += 1

                messages.success(
                    request,
                    f'{created_count} students uploaded successfully!'
                )
                return redirect('admin_dashboard')

            except Exception as e:
                messages.error(request, f'Upload failed: {str(e)}')

    else:
        form = StudentUploadForm()

    return render(request, 'exams/upload_students.html', {'form': form})


def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room added successfully!')
            return redirect('manage_rooms')
    else:
        form = RoomForm()

    return render(request, 'exams/add_room.html', {'form': form})


def manage_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'exams/manage_rooms.html', {'rooms': rooms})


def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated!')
            return redirect('manage_rooms')
    else:
        form = RoomForm(instance=room)

    return render(request, 'exams/add_room.html', {'form': form})


def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted!')
        return redirect('manage_rooms')

    return render(request, 'exams/confirm_delete.html', {'object': room})


def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam added successfully!')
            return redirect('manage_exams')
    else:
        form = ExamForm()

    return render(request, 'exams/add_exam.html', {'form': form})


def manage_exams(request):
    exams = Exam.objects.all().order_by('date', 'start_time')
    return render(request, 'exams/manage_exams.html', {'exams': exams})


def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam updated successfully!')
            return redirect('manage_exams')
    else:
        form = ExamForm(instance=exam)

    return render(request, 'exams/add_exam.html', {'form': form})


def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted!')
        return redirect('manage_exams')

    return render(request, 'exams/confirm_delete.html', {'object': exam})


def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    assignments = InvigilatorAssignment.objects.filter(exam=exam)

    return render(
        request,
        'exams/exam_detail.html',
        {'exam': exam, 'assignments': assignments}
    )


def is_admin(user):
    return user.role == 'admin'


@login_required
@user_passes_test(is_admin)
def assign_invigilator(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        form = InvigilatorAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.exam = exam
            assignment.save()
            messages.success(request, 'Invigilator assigned successfully!')
            return redirect('exam_detail', exam_id=exam.id)
    else:
        form = InvigilatorAssignmentForm(initial={'exam': exam})

    return render(
        request,
        'exams/assign_invigilator.html',
        {'form': form, 'exam': exam}
    )


@login_required
def search_seat(request):
    enrollment_id = request.GET.get('enrollment_id')

    allocation = SeatingAllocation.objects.filter(
        student__enrollment_id=enrollment_id
    ).select_related('room', 'exam').first()

    return render(
        request,
        'exams/search_result.html',
        {'allocation': allocation, 'enrollment_id': enrollment_id}
    )


@login_required
def print_seating_slip(request, allocation_id):
    allocation = get_object_or_404(SeatingAllocation, id=allocation_id)

    return render(
        request,
        'seating/seating_slip.html',
        {'allocation': allocation}
    )


@login_required
def download_seating_slip(request, allocation_id):
    allocation = get_object_or_404(SeatingAllocation, id=allocation_id)

    content = f"""
SEATING SLIP

Enrollment ID: {allocation.student.enrollment_id}
Student Name: {allocation.student.name}
Exam: {allocation.exam.name}
Room: {allocation.room.room_number}
Seat Number: {allocation.seat_number}
"""

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=seating_slip.txt'
    return response


def exam_report(request, exam_id):
    exam = Exam.objects.get(id=exam_id)

    total_registered = StudentExam.objects.filter(exam=exam).count()
    total_allocated = SeatingAllocation.objects.filter(exam=exam).count()
    total_rooms = SeatingAllocation.objects.filter(exam=exam).values('room').distinct().count()

    from django.db.models import Count

    room_stats = SeatingAllocation.objects.filter(exam=exam).values(
        'room__room_number',
        'room__capacity'
    ).annotate(
        students_allocated=Count('id')
    ).order_by('room__room_number')

    for stat in room_stats:
        stat['utilization'] = (stat['students_allocated'] / stat['room__capacity']) * 100

    return render(
        request,
        'exams/exam_report.html',
        {
            'exam': exam,
            'total_registered': total_registered,
            'total_allocated': total_allocated,
            'total_rooms': total_rooms,
            'room_stats': room_stats,
        }
    )
