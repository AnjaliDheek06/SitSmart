from django.utils import timezone
from exams.models import Student, Room, Exam
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.middleware.csrf import rotate_token
from django.views.decorators.csrf import csrf_protect
from exams.models import InvigilatorAssignment

def home_view(request):
    return render(request, 'users/landing.html')


@csrf_protect   
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            rotate_token(request)

            # SUPERUSER
            if user.is_superuser:
                return redirect('/admin/')   # Django superuser panel

            # ADMIN USER (role-based)
            if user.role == 'admin':
                return redirect('admin_dashboard')

            elif user.role == 'invigilator':
                return redirect('invigilator_dashboard')

            elif user.role == 'student':
                return redirect('student_dashboard')

        return render(request, 'users/login.html', {'error': 'Invalid credentials'})

    return render(request, 'users/login.html')


@login_required
@user_passes_test(lambda u: u.role == 'admin')
def admin_dashboard(request):
    context = {
        'total_students': Student.objects.count(),
        'total_rooms': Room.objects.count(),
        'upcoming_exams': Exam.objects.filter(
            date__gte=timezone.now().date()
        ).count(),
    }
    return render(request, 'users/admin_dashboard.html', context)


def is_invigilator(user):
    return user.role == 'invigilator'


@login_required
@user_passes_test(is_invigilator)
def invigilator_dashboard(request):
    assignments = InvigilatorAssignment.objects.filter(
        invigilator=request.user
    )
    return render(request, 'users/invigilator_dashboard.html', {'assignments': assignments})


@login_required
def student_dashboard(request):
    return render(request, 'users/student_dashboard.html')
