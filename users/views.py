from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse


def login_view(request):
    print('login view hit')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            print("USERNAME:", user.username)
            print("ROLE (repr):", repr(user.role))

            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'invigilator':
                return redirect('invigilator_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
            else:
                # 🚨 THIS LINE IS THE TRUTH SERUM
                return HttpResponse(f"ROLE MISMATCH → '{user.role}'")

        else:
            return HttpResponse("AUTH FAILED")

    return render(request, 'users/login.html')



def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')


def invigilator_dashboard(request):
    return render(request, 'users/invigilator_dashboard.html')


def student_dashboard(request):
    return render(request, 'users/student_dashboard.html')
