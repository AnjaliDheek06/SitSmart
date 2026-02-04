# 🎓 SitSmart – Exam Seating Allocation System

SitSmart is a web-based **Exam Seating Allocation System** built using **Django**.  
It automates the process of managing exams, allocating seats to students, assigning invigilators, and generating seating slips and reports in a structured and secure manner.

The system is designed with **role-based workflows** and follows real-world examination processes.

## 🚀 Features

### 👤 Role-Based Access
- **Superuser**: Full system-level access via Django Admin
- **Admin**: Exam setup, student upload, room management, seat allocation
- **Invigilator**: View assigned exams and duties
- **Student**: Search seat and download seating slip

### 🛠️ Admin Capabilities
- Upload student list using **Excel**
- Manage exam rooms and capacities
- Create and manage exams
- Assign invigilators to exams
- Trigger automatic seat allocation
- View exam-wise seating reports

### 🪑 Automatic Seat Allocation
- Capacity-based room allocation
- Alternate seating logic for fairness
- Exam-specific seat assignment
- Prevents duplicate seat allocation

### 🎓 Student Services
- Search seat using enrollment ID
- View exam, room, and seat number
- Print or download seating slip

### 📊 Reports & Analytics
- Total registered students
- Total allocated seats
- Room-wise utilization
- Capacity usage analysis

## 🧩 Project Modules

1. **User & Role Management**
2. **Admin & Exam Management**
3. **Student Seating Management**
4. **Student & Invigilator Services**
5. **Reports & Output Generation**

---

## ⚙️ Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS
- **Database**: SQLite
- **Authentication**: Django Authentication System
- **Architecture**: MVC (Model–View–Template)

> ⚠️ JavaScript is intentionally not used for core logic.  
> All critical operations are handled securely on the server side.

### ▶️ Run the Project Locally

Follow the steps below to run the project on your local machine:

```bash
# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser (admin access)
python manage.py createsuperuser

# 6. Start the Django development server
python manage.py runserver
If the server starts successfully, open your web browser and access the application using the URLs below:

Application URL:
http://127.0.0.1:8000/

Django Admin Panel:
http://127.0.0.1:8000/admin/


