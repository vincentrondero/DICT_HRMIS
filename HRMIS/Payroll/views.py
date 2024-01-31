from django.shortcuts import render
from Authentication.models import User

def dashboard_views(request, user_role):
    user_role = request.session.get('role', 'Guest')
    return render(request, 'HR/dashboard.html', {'user_role': user_role})

def manage_payroll(request, user_role):
    return render(request, 'HR/manage_payroll.html', {'user_role': user_role})

def manage_employee(request, user_role):
    users = User.objects.all()
    return render(request, 'HR/manage_employee.html' , {'users': users, 'user_role': user_role})

