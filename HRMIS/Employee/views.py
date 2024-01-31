from django.shortcuts import render

def employee_dashboard(request, user_role):
    user_role = request.session.get('role', 'Guest')
    return render(request, 'Employee/Employee.html', {'user_role': user_role})