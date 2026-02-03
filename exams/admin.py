from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

import pandas as pd

from .models import Room, Course, Student, Exam, StudentExam, InvigilatorAssignment
from seating.admin import allocate_seats_for_exam


# ---------- ADMIN ACTION ----------
@admin.action(description="Register all students for selected exams")
def register_all_students(modeladmin, request, queryset):
    students = Student.objects.all()

    for exam in queryset:
        student_exams = []

        for student in students:
            if not StudentExam.objects.filter(student=student, exam=exam).exists():
                student_exams.append(
                    StudentExam(student=student, exam=exam)
                )

        StudentExam.objects.bulk_create(student_exams)


# ---------- ROOM ADMIN ----------
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'capacity', 'building', 'floor')
    search_fields = ('room_number', 'building')


# ---------- STUDENT ADMIN (EXCEL UPLOAD ADDED HERE) ----------
class StudentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_id', 'name', 'semester', 'email')
    ordering = ('enrollment_id',)
    search_fields = ('enrollment_id', 'name')
    list_filter = ('semester',)

    change_list_template = "admin/student_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.upload_excel),
            path('download-sample/', self.download_sample_excel),
        ]
        return custom_urls + urls

    def download_sample_excel(self, request):
        df = pd.DataFrame(columns=[
            'enrollment_id',
            'name',
            'semester',
            'email'
        ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=student_sample.xlsx'
        df.to_excel(response, index=False)

        return response

    def upload_excel(self, request):
        if request.method == "POST":
            file = request.FILES.get('file')

            if not file:
                messages.error(request, "No file uploaded")
                return redirect("..")

            df = pd.read_excel(file)

            students = []
            for _, row in df.iterrows():
                students.append(
                    Student(
                        enrollment_id=row['enrollment_id'],
                        name=row['name'],
                        semester=row['semester'],
                        email=row['email'],
                    )
                )

            Student.objects.bulk_create(students, ignore_conflicts=True)
            messages.success(request, "Students uploaded successfully")

            return redirect("..")

        return render(request, "admin/upload_excel.html")


# ---------- EXAM ADMIN ----------
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'start_time', 'course')
    list_filter = ('date', 'course')
    search_fields = ('name', 'course')
    actions = [
        register_all_students,
        allocate_seats_for_exam,
    ]


# ---------- STUDENT EXAM ADMIN ----------
@admin.register(StudentExam)
class StudentExamAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'registered_at')
    list_filter = ('exam',)
    search_fields = ('student__name', 'student__enrollment_id')
    ordering = ('student__enrollment_id',)


# ---------- OTHER REGISTRATIONS ----------
admin.site.register(Room, RoomAdmin)
admin.site.register(Course)
admin.site.register(Student, StudentAdmin)
admin.site.register(InvigilatorAssignment)
